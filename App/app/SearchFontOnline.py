import requests
import json

class SearchFontOnline:
    def __init__(self):
        with open("./configs/apikey.json", "r", encoding="utf-8") as file:
            self.apikey = json.load(file)["GOOGLE_SEARCH_APIKEY"]

        self.url = "https://www.googleapis.com/customsearch/v1"

    def search_font_online(self, font_name):
        params = {
            "key": self.apikey,
            "cx": '6092debefa13b4b28',
            "q": f"download-font-{font_name}",
            "num": 3  # Số kết quả muốn lấy (tối đa 10)
        }
        response = requests.get(self.url, params=params).json()
        
        # for index, item in enumerate(response.get("items", []), start=1):
        #     print(f"{index}. {item['title']}")
        #     print(f"   {item['link']}\n")
        
        return response
