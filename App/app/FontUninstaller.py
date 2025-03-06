import os
import json
from utils.log import log_message, new_logger

class FontUninstaller:
    # Thư mục cài đặt font trên Windows
    FONT_INSTALL_DIR = "C:\\Windows\\Fonts"

    def __init__(self, output_file):
        self.output_file = output_file

    def uninstall_fonts(self):
        new_logger("Bắt đầu gỡ bỏ font...")
        
        if not os.path.exists(self.output_file):
            log_message("Không tìm thấy file fontlist.json, không có gì để gỡ bỏ.")
            return
        
        with open(self.output_file, "r", encoding="utf-8") as f:
            font_list = json.load(f)
        
        for font in font_list:
            font_path = os.path.join(self.FONT_INSTALL_DIR, font["name"])
            
            if os.path.exists(font_path):
                try:
                    os.remove(font_path)
                    log_message(f"Đã gỡ bỏ: {font['name']}")
                except Exception as e:
                    log_message(f"Lỗi khi gỡ bỏ {font['name']}: {e}")
            else:
                log_message(f"Bỏ qua {font['name']}, không tìm thấy trong hệ thống.")
        
        log_message("Hoàn tất gỡ bỏ font.")