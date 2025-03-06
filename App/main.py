import os
import sys
import ctypes

# from utils.request_access import request_admin
from app.FontScanner import FontScanner
from app.FontCollector import FontCollector
from app.FontInstaller import FontInstaller
from app.FontUninstaller import FontUninstaller
from utils.log import log_message, new_logger

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def request_admin():
    if not is_admin():
        # Xây dựng lại tham số đúng cách
        params = " ".join(f'"{arg}"' for arg in sys.argv)
        print(f"DEBUG: Chạy lại với quyền admin: {sys.executable} {params}")  # Debug

        # Gọi lại chương trình với quyền admin
        result = ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)

        if result > 32:  # Nếu trả về > 32, nghĩa là lệnh đã được thực thi
            print("DEBUG: Đã yêu cầu quyền admin, thoát chương trình gốc.")
            exit(0)  # Thoát chương trình hiện tại, chương trình mới sẽ chạy tiếp
        else:
            print("Không thể yêu cầu quyền admin.")
            exit(1)  # Thoát với lỗi

FONT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "fontlist.json")
LOG_FILE = os.path.join(os.path.dirname(__file__), "log.txt")

def main():
    if len(sys.argv) < 2:
        log_message("Sử dụng: font [scan|collect|install|uninstall|showlog]")
        return

    command = sys.argv[1].lower()

    # Yêu cầu quyền admin trước khi thực hiện cài đặt hoặc gỡ bỏ font
    if command in ["install", "uninstall"]:
        request_admin()

    if command == "scan":
        scanner = FontScanner(FONT_DIR, OUTPUT_FILE, LOG_FILE)
        scanner.scan_fonts()
    elif command == "collect":
        collector = FontCollector(OUTPUT_FILE)
        collector.collect_fonts()
    elif command == "install":
        installer = FontInstaller(OUTPUT_FILE)
        installer.install_fonts()
    elif command == "uninstall":
        uninstaller = FontUninstaller(OUTPUT_FILE)
        uninstaller.uninstall_fonts()
    elif command == "showlog":
        with open(LOG_FILE, 'r', encoding='utf-8') as file:
            content = file.read()
            print(content)
    else:
        log_message("Lệnh không hợp lệ! Sử dụng: font [scan|collect|install|uninstall]")

if __name__ == "__main__":
    main()