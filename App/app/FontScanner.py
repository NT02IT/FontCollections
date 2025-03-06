import os
import json
from utils.log import log_message, new_logger

# Định nghĩa thứ tự ưu tiên của các định dạng font

class FontScanner:
    FONT_PRIORITY = [".otf", ".ttf", ".woff2", ".woff", ".eot"]

    def __init__(self, font_dir, output_file, log_file):
        self.font_dir = font_dir
        self.output_file = output_file
        self.log_file = log_file

    def scan_fonts(self):
        font_map = {}
        new_logger("Bắt đầu quét font...")
        
        # Duyệt qua tất cả các thư mục và file trong font_dir
        for root, _, files in os.walk(self.font_dir):
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in self.FONT_PRIORITY:
                    font_name = os.path.splitext(file)[0]
                    file_path = os.path.join(root, file)
                    
                    # Nếu font_name chưa có hoặc file có độ ưu tiên cao hơn thì cập nhật
                    if font_name not in font_map or self.FONT_PRIORITY.index(ext) < self.FONT_PRIORITY.index(font_map[font_name]["extension"]):
                        font_map[font_name] = {"name": file, "path": file_path, "extension": ext}
        
        # Lưu kết quả vào fontlist.json
        with open(self.output_file, "w", encoding="utf-8") as f:
            json.dump(list(font_map.values()), f, indent=4, ensure_ascii=False)
        
        log_message(f"Đã lưu danh sách font vào {self.output_file}")
