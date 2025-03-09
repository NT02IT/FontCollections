import requests
import json

class CheckGGFont:
    def __init__(self):
        with open("./configs/apikey.json", "r", encoding="utf-8") as file:
                apikey = json.load(file) 
        self.GOOGLE_FONTS_APIKEY = apikey["GOOGLE_FONTS_APIKEY"]
        self.url = f"https://www.googleapis.com/webfonts/v1/webfonts?key={self.GOOGLE_FONTS_APIKEY}"

    def check_google_fonts(self, font_name):
        
        response = requests.get(self.url)
        
        if response.status_code == 200:
            fonts = response.json().get("items", [])
            for font in fonts:
                if font["family"].lower() == font_name.lower():
                    return {
                        "name": font["family"],
                        "tags": {
                            "font-type": ["sans-serif" if "Sans" in font["family"] else "serif"],
                            "design-style": ["modern"],
                            "usage": ["web", "print"],
                            "emotion": ["clean", "professional"],
                            "license": ["free"]
                        },
                        "source": font["files"].get("regular", None)  # Link tải font
                    }
        return None
