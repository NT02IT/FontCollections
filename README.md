# Hướng dẫn sử dụng tool

## Yêu cầu:

- Máy tính có cài đặt sẵn Python

## Cài đặt chương trình

- Bước 1: Clone/ Tải project này về
- Bước 2: Phải chuột vào file setup.bat vào bấm run với quyền admin

## Sử dụng

- Mở `cmd` tại bất cứ đâu (phím tắt `Ctrl+R` -> `cmd` -> `Enter`)
- Gõ `font scan` và enter hoặc nháy đúp chuột vào file Scan.bat, tool sẽ scan tất cả các font đang có trong folder Font Collections (Tên gì cũng được, không nhất thiết phải đúng tên là Font Collections)
- Gõ `font collect` và enter, tool sẽ collect tất cả các font file có trong Font Collections và lưu vào file "App\fonts", tool sẽ collect theo thứ tự ưu tiên ".otf" > ".ttf" > ".woff2" > ".woff" > ".eot" đồng nghĩa nếu bộ font đã có bản .otf thì tool chỉ collect bản .otf và bỏ qua các bản có độ ưu tiên thấp hơn để không phải cài tất cả.
- Gõ `font install` và enter, tool sẽ tự động cài tất cả các font đã scan được
- Gõ `font uninstall` và enter, tool sẽ tự động gỡ bỏ tất cả các font có trong collection ra khỏi máy tính
- Gõ `font showlog` và enter sau mỗi bước thực hiện câu lệnh để xem kết quả thực thi (kiểm tra xem font có được cài đủ không, xóa đủ tất cả font ra không)
