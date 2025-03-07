import os
import shutil
import ctypes
from ctypes import wintypes
import json
import threading
import sys
import ntpath
import winreg
from utils.log import log_message, new_logger



class FontInstaller:
    user32 = ctypes.WinDLL('user32', use_last_error=True)
    gdi32 = ctypes.WinDLL('gdi32', use_last_error=True)

    FONTS_REG_PATH = r'Software\Microsoft\Windows NT\CurrentVersion\Fonts'

    HWND_BROADCAST = 0xFFFF
    SMTO_ABORTIFHUNG = 0x0002
    WM_FONTCHANGE = 0x001D
    GFRI_DESCRIPTION = 1
    GFRI_ISTRUETYPE = 3

    if not hasattr(wintypes, 'LPDWORD'):
        wintypes.LPDWORD = ctypes.POINTER(wintypes.DWORD)

    user32.SendMessageTimeoutW.restype = wintypes.LPVOID
    user32.SendMessageTimeoutW.argtypes = (
        wintypes.HWND,   # hWnd
        wintypes.UINT,   # Msg
        wintypes.LPVOID,  # wParam
        wintypes.LPVOID,  # lParam
        wintypes.UINT,   # fuFlags
        wintypes.UINT,   # uTimeout
        wintypes.LPVOID)  # lpdwResult

    gdi32.AddFontResourceW.argtypes = (
        wintypes.LPCWSTR,)  # lpszFilename

    # http://www.undoclog_message.org/winspool/getfontresourceinfo
    gdi32.GetFontResourceInfoW.argtypes = (
        wintypes.LPCWSTR,  # lpszFilename
        wintypes.LPDWORD,  # cbBuffer
        wintypes.LPVOID,  # lpBuffer
        wintypes.DWORD)   # dwQueryType

    def __init__(self, output_file):
        self.output_file = output_file
        self.lock = threading.Lock()

    def install_font(self, src_path):
        # copy the font to the Windows Fonts folder
        dst_path = os.path.join(os.environ['SystemRoot'], 'Fonts',
                                os.path.basename(src_path))
        try:
            # Sao chép font vào thư mục Fonts
            shutil.copy(src_path, dst_path)
        except PermissionError:
            log_message(f"Permission denied: Không thể sao chép {src_path} vào {dst_path}. Vui lòng chạy chương trình với quyền quản trị.")
            return
        except Exception as e:
            log_message(f"Lỗi khi sao chép {src_path}: {e}")
            return

        # load the font in the current session
        if not self.gdi32.AddFontResourceW(dst_path):
            os.remove(dst_path)
            raise WindowsError('AddFontResource failed to load "%s"' % src_path)
        
        # notify running programs
        # self.user32.SendMessageTimeoutW(self.HWND_BROADCAST, self.WM_FONTCHANGE, 0, 0,
        #                         self.SMTO_ABORTIFHUNG, 1000, None)
        
        # store the fontname/filename in the registry
        filename = os.path.basename(dst_path)
        fontname = os.path.splitext(filename)[0]
        
        # try to get the font's real name
        cb = wintypes.DWORD()
        if self.gdi32.GetFontResourceInfoW(filename, ctypes.byref(cb), None,
                                    self.GFRI_DESCRIPTION):
            buf = (ctypes.c_wchar * cb.value)()
            if self.gdi32.GetFontResourceInfoW(filename, ctypes.byref(cb), buf,
                                        self.GFRI_DESCRIPTION):
                fontname = buf.value
        
        is_truetype = wintypes.BOOL()
        cb.value = ctypes.sizeof(is_truetype)
        self.gdi32.GetFontResourceInfoW(filename, ctypes.byref(cb),
                                ctypes.byref(is_truetype), self.GFRI_ISTRUETYPE)
        
        if is_truetype:
            fontname += ' (TrueType)'

        with self.lock:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, self.FONTS_REG_PATH, 0, winreg.KEY_SET_VALUE) as key:
                winreg.SetValueEx(key, fontname, 0, winreg.REG_SZ, filename)

    def install_fonts(self):
        if not os.path.exists(self.output_file):
            log_message("Không tìm thấy file fontlist.json, vui lòng chạy scan trước.")
            return
        
        with open(self.output_file, "r", encoding="utf-8") as f:
            font_list = json.load(f)

        new_logger("Bắt đầu cài đặt font...")
        
        threads = []
        for font in font_list:
            src_path = font["path"]
            dest_path = os.path.join(os.environ['SystemRoot'], 'Fonts',
                                os.path.basename(src_path))

            thread = threading.Thread(target=self.install_font, args=(src_path,))
            threads.append(thread)
            thread.start()
            
            if os.path.exists(dest_path):
                log_message(f"Bỏ qua {font['name']}, đã được cài đặt trong hệ thống.")
            else:
                try:
                    self.install_font(src_path)
                    log_message("{} installed".format(font["name"]))
                except Exception as err:
                    log_message("Error for font: {} - ({})".format(font["name"], err))

        for thread in threads:
            thread.join()

        self.user32.SendMessageTimeoutW(self.HWND_BROADCAST, self.WM_FONTCHANGE, 0, 0, self.SMTO_ABORTIFHUNG, 1000, None)
        
        log_message("Hoàn tất cài đặt font.")