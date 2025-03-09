import os
import json
import shutil
from utils.log import log_message, new_logger

class FontCollector:
    # Thư mục cài đặt font trên Windows
    FONT_COLLECTION_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..\\fonts"))

    def __init__(self, output_file):
        self.output_file = output_file

    def collect_fonts(self):
        if not os.path.exists(self.output_file):
            log_message("Không tìm thấy file fontlist.json, vui lòng chạy scan trước.")
            return
        
        with open(self.output_file, "r", encoding="utf-8") as f:
            font_list = json.load(f)
        
        for font in font_list:
            src_path = font["path"]
            dest_path = os.path.join(self.FONT_COLLECTION_DIR, font["name"])
            
            if os.path.exists(dest_path):
                log_message(f"{font['name']} - đã tồn tại.")
            else:
                shutil.copy2(src_path, dest_path)
                log_message(f"Collected: {font['name']}")