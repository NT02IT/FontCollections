import win32com.client

def get_file_properties(file_path):
    """Lấy tất cả properties của một file trên Windows"""
    properties = {}
    
    try:
        shell = win32com.client.Dispatch("Shell.Application")
        folder = shell.Namespace(file_path.rsplit("\\", 1)[0])  # Thư mục chứa file
        file_item = folder.ParseName(file_path.split("\\")[-1])  # Tên file
        
        # Lặp qua tất cả properties có thể lấy
        for i in range(0, 100):
            key = folder.GetDetailsOf(None, i)
            value = folder.GetDetailsOf(file_item, i)
            if key and value:
                properties[key] = value

    except Exception as e:
        print(f"❌ Lỗi khi lấy properties: {e}")

    return properties

# # 🛠 Test thử với một file bất kỳ
# file_path = r"D:\PublicZone\FontCollections\App\fonts\Phudu-SemiBold.ttf"
# properties = get_file_properties(file_path)

# # In ra danh sách properties
# for key, value in properties.items():
#     print(f"{key}: {value}")
