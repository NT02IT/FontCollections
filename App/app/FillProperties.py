# import json
# from utils.metadata_handler import get_file_properties, set_custom_property
# from app.SearchFontOnline import SearchFontOnline

# # Bước 1: Tìm link tải font đó
# # Bước 2: Nếu là google font thì lấy thông tin về category, subsets, license = Open Source
# # Bước 3: Tổng hợp 2 bước trên và sửa đổi lại file fontlist.json
# # Bước 4: Tạo file đổi thông tin font dựa trên file fontlist.json

# class FillProperties:
#     def __init__(self):
#         self.fontlist_path = ".\\fontlist.json"

#         try:
#             with open(self.fontlist_path, "r", encoding="utf-8") as f:
#                 self.fonts = json.load(f)
#         except FileNotFoundError:
#             print("❌ Không tìm thấy file fontlist.json!")
#         except json.JSONDecodeError:
#             print("❌ Lỗi đọc file fontlist.json!")
        
#         self.searchFontOnline = SearchFontOnline()

#     def addFontURL(self, font):
#         font_name = font["name"]

#         search_result = self.searchFontOnline.search_font_online(font_name)
#         first_link = search_result.get("items", [{}])[0].get("link", "Not Found")
#         font["information"] = {"URL": first_link}

#         set_custom_property(font["path"], "URL", first_link)
#         return first_link

#     def run(self):
#         for font in self.fonts:
#             font_path = font["path"]
#             font_name = font["name"]

#             # Lấy thông tin properties của file font
#             properties = get_file_properties(font_path)
#             if "URL" in properties:
#                 print(f"✅ Bỏ qua {font_name}: Đã có url trong properties")
#             else:
#                 if "information" in font and "URL" in font["information"] and font["information"]["URL"] != "Not Found":
#                     pass
#                 else:
#                     self.addFontURL(font)

#         # Lưu danh sách font đã cập nhật vào file JSON
#         with open(self.fontlist_path, "w", encoding="utf-8") as f:
#             json.dump(self.fonts, f, indent=4, ensure_ascii=False)
#         print("✅ Đã cập nhật fontlist.json thành công!")
