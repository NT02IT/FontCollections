import requests
import os
import json

from utils.log import log_message, new_logger

class FontSearch:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))  
        config_path = os.path.join(base_dir, "../configs/apikey.json")  
        with open(config_path, "r", encoding="utf-8") as file:
            self.apikey = json.load(file) 

    def search(self, keywords):
        new_logger("Bắt đầu tìm kiếm")

        log_message("System:")
        log_message("---\n")
        self.searchInSystem(keywords)

        log_message("Google Font:")
        log_message("---\n")
        self.searchInGoogleFonts(keywords)

        log_message("Google Search:")
        log_message("---\n")
        self.searchInGoogle(keywords)

    def searchInSystem(self, keywords):
        FONT_INSTALL_DIR = "C:\\Windows\\Fonts"
        results = []
        i = 0
        keywords = self.normalize_name(keywords)

        for font in os.listdir(FONT_INSTALL_DIR):
            if keywords in self.normalize_name(font):
                i = i + 1
                results.append(font)
                log_message(f"{i}. {font}")
                log_message(f"   url: {os.path.join(FONT_INSTALL_DIR, font)}\n")

        return results

    def searchInGoogleFonts(self, keywords):        
        GOOGLE_FONTS_APIKEY = self.apikey["GOOGLE_FONTS_APIKEY"]
        url = f"https://www.googleapis.com/webfonts/v1/webfonts?key={GOOGLE_FONTS_APIKEY}"
        
        response = requests.get(url)

        keywords = self.normalize_name(keywords)
        results = []
        i = 0
        
        if response.status_code == 200:
            fonts = response.json().get("items", [])
            for font in fonts:
                dest = self.normalize_name(font["family"]) + self.normalize_name(font["category"])
                if keywords in dest: # thêm category và lang vào
                    i = i + 1

                    name = font["family"]
                    url = "https://fonts.google.com/specimen/" + name.replace(" ", "+")
                    subsets = font["subsets"]
                    category = font["category"]

                    rs = {
                        "name": name,
                        "url": url,
                        "lang": subsets,
                        "category": category,
                    }                    
                    results.append(rs)

                    log_message(f"{i}. {name}")
                    log_message(f"   url: {url}")
                    log_message(f"   lang: {', '.join(subsets)}")
                    log_message(f"   category: {category}\n")

        return results

    def searchInGoogle(self, keywords):
        url = "https://www.googleapis.com/customsearch/v1"

        params = {
            "key": self.apikey["GOOGLE_SEARCH_APIKEY"],
            "cx": '6092debefa13b4b28',
            "q": f"download-font-{keywords}",
            "num": 10  # Số kết quả muốn lấy (tối đa 10)
        }
        response = requests.get(url, params=params).json()
        
        for index, item in enumerate(response.get("items", []), start=1):
            log_message(f"{index}. {item['title']}")
            log_message(f"   {item['link']}\n")
        
        return response
    
    def normalize_name(self, name):
        return name.lower().replace("-", "").replace("_", "").replace(" ", "")