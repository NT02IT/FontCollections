import os
import shutil
import json
from collections import defaultdict
from fontTools.ttLib import TTFont, TTCollection
from utils.metadata_handler import get_file_properties
from utils.log import log_message, new_logger

class MergeFonts:
    def __init__(self, OUTPUT_FILE):
        self.OUTPUT_FILE = OUTPUT_FILE
        with open(self.OUTPUT_FILE, "r", encoding="utf-8") as f:
            self.fontlist = json.load(f)

        base_dir = os.path.dirname(os.path.abspath(__file__))  
        self.EXPORT_FOLDER = os.path.join(base_dir, "../fonts/merged")          
        os.makedirs(self.EXPORT_FOLDER, exist_ok=True) # Tạo thư mục nếu nó chưa tồn tại

    def run(self):
        new_logger("🔍 Đang quét thư mục fonts...")
        ttf_files, non_ttf_files = self.classify_fonts()

        grouped_fonts = []  # Mảng chứa các nhóm font hợp lệ
        ttcName = [] 
        ttcIndex = 0
        while ttf_files:
            current_font = ttf_files.pop(0)
            fonts_merge_name = f'{current_font["name"]}'
            fonts_to_merge = [current_font]            

            for other_font in ttf_files[:]:  # Duyệt danh sách font còn lại
                if self.can_merge_fonts(current_font, other_font):
                    fonts_to_merge.append(other_font)
                    ttf_files.remove(other_font)   
                else:
                    for i in range(0, len(fonts_to_merge)):
                        fonts_merge_name = self.get_last_common_index(fonts_merge_name, fonts_to_merge[i]["name"])
                        if(fonts_merge_name == ""):
                            ttf_files = fonts_to_merge[i:] + ttf_files
                            break                    

                    log_message(f"✅ Đã gộp font: {fonts_merge_name}")
                    break

            grouped_fonts.append(fonts_to_merge)
            ttcName.append(fonts_merge_name)

        print(len(grouped_fonts))
        print(len(ttcName))

        # Gộp nhóm thành TTC hoặc copy nếu không thể gộp
        for i, font_paths in enumerate(grouped_fonts):
            if len(font_paths) == 1:
                dest_path = os.path.join(self.EXPORT_FOLDER, font_paths[0]["name"])
                try:
                    if not os.path.exists(dest_path):
                        shutil.copy2(font_paths[0]["path"], self.EXPORT_FOLDER)
                        fontname = font_paths[0]["name"]
                        log_message(f"✅ Đã copy {fontname} vào {self.EXPORT_FOLDER}")
                except Exception as e:
                    log_message(f"Lỗi khi copy {fontname}: {e}")

            else: self.merge_fonts_to_ttc(font_paths, ttcName[i])                

        log_message("🎉 Hoàn thành!")

    # Phân loại và copy các file font thành hai nhóm: .ttf và không phải .ttf.
    def classify_fonts(self):
        # Tạo hai danh sách để phân loại
        ttf_files = []
        non_ttf_files = []
        
        # Phân loại file dựa trên phần mở rộng
        for font in self.fontlist:
            if font["extension"] == ".ttf":
                ttf_files.append(font)
            else:
                non_ttf_files.append(font)
        
        # Copy file không phải .ttf vào thư mục non_ttf_folder
        for non_ttf_file in non_ttf_files:
            dest_path = os.path.join(self.EXPORT_FOLDER, non_ttf_file["name"])
            try:
                if not os.path.exists(dest_path):
                    shutil.copy2(non_ttf_file["path"], self.EXPORT_FOLDER)
                    fontname = non_ttf_file["name"]
                    log_message(f"✅ Đã copy {fontname} vào {self.EXPORT_FOLDER}")
            except Exception as e:
                log_message(f"Lỗi khi copy {fontname}: {e}")
        return ttf_files, non_ttf_files

    # Kiểm tra xem hai file .ttf có thể gộp hay không bằng cách so sánh sfntVersion và tables.
    def can_merge_fonts(self, font1, font2):
        font1_metadata = get_file_properties(font1["path"])
        font2_metadata = get_file_properties(font2["path"])

        if font1_metadata.get("Authors") != font2_metadata.get("Authors"):
            return False
        
        if font1_metadata.get("Copyright") == font2_metadata.get("Copyright"):
            return False

        try:
            ttf1 = TTFont(font1["path"])
            ttf2 = TTFont(font2["path"])
            
            # Kiểm tra sfntVersion
            if ttf1.sfntVersion != ttf2.sfntVersion:
                return False
            
            # Kiểm tra danh sách các bảng (tables)
            if set(ttf1.keys()) != set(ttf2.keys()):
                return False
            
            return True
        except Exception as e:
            log_message(f"Lỗi khi kiểm tra font: {e}")
            return False

    # Gộp font thành TTC
    def merge_fonts_to_ttc(self, font_paths, font_name):
        fonts = [] 
        for font in font_paths:
            try:
                fonts.append(TTFont(font["path"]))
            except Exception as e:
                log_message(f"Lỗi khi mở font {font['name']}: {e}")
        collection = TTCollection()
        collection.fonts = fonts  

        # Lấy tên chung cho 1 ttc
        output_path= os.path.join(self.EXPORT_FOLDER, f"{font_name}.ttc")
        try:
            collection.save(output_path)
            log_message(f"🎉 Đã tạo thành công file {output_path}")
            log_message(f"   Tổng số font trong collection: {len(fonts)}")
            return True
        except Exception as e:
            log_message(f"Lỗi khi lưu file .ttc: {e}")
            return False
        
    def get_last_common_index(self, name1, name2):
        words1 = name1.split()  # Tách thành danh sách từ
        words2 = name2.split()
        
        min_length = min(len(words1), len(words2))  # Độ dài nhỏ nhất của hai danh sách
        last_common_index = -1  # Mặc định không có phần trùng
        
        for i in range(min_length):
            if words1[i] == words2[i]:
                last_common_index = i  # Cập nhật index cuối cùng trùng nhau
            else:
                break  # Dừng nếu gặp khác nhau

        return " ".join(words1[:last_common_index + 1]).strip() if last_common_index != -1 else ""