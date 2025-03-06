# Hướng dẫn sử dụng tool

## Yêu cầu:

- Máy tính có cài đặt sẵn Python

## Cài đặt chương trình

- Bước 1: Tạo 1 folder để chứa Font Collections
- Bước 2: Đưa tất cả code của tool vào trong chung folder Font Collections này
- Bước 3: Đến thư mục "target" bên trong thư mục "App"
- Bước 4: Bấm `Windows+S` để tìm kiếm, nhập vào "Edit enviroment variables" và bấm vào nó
- Bước 5: Tại bảng "User variable" tìm đến dòng `path`, bấm nút "Edit" sau đó bấm nút "Add" và paste đường dẫn folder "target" vào

## Sử dụng

- Mở `cmd` tại bất cứ đâu (phím tắt `Ctrl+R` -> `cmd` -> `Enter`)
- Gõ `font scan` và enter hoặc nháy đúp chuột vào file Scan.bat, tool sẽ scan tất cả các font đang có trong folder cha - folder Font Collections (Tên gì cũng được, không nhất thiết phải đúng tên là Font Collections)
- Gõ `font collect` và enter, tool sẽ collect tất cả các font file có trong Font Collections và lưu vào file "App\fonts", tool sẽ collect theo thứ tự ưu tiên ".otf" > ".ttf" > ".woff2" > ".woff" > ".eot" đồng nghĩa nếu bộ font đã có bản .otf thì tool chỉ collect bản .otf và bỏ qua các bản có độ ưu tiên thấp hơn để không phải cài tất cả.
- Gõ `font install` và enter, tool sẽ tự động cài tất cả các font đã scan được
- Gõ `font uninstall` và enter, tool sẽ tự động gỡ bỏ tất cả các font có trong collection ra khỏi máy tính
- Gõ `font showlog` và enter sau mỗi bước thực hiện câu lệnh để xem kết quả thực thi (kiểm tra xem font có được cài đủ không, xóa đủ tất cả font ra không)
