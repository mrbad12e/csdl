Tải Python tại đây: https://www.python.org/downloads/
Hoặc xem hướng dẫn trên mạng
Khuyến nghị tải bản 3.8, 3.9

Kiểm tra python đã tải thành công chưa, chạy:
pip --version

Tải virtual environment
pip install virtualenv

Kiểm tra virtual environment đã tải thành công chưa, chạy:
virtualenv --version

Clone dir này lại bằng git clone

Chuyển đến thư mục đã clone bằng câu lệnh: cd csdl

Khởi chạy virtual environment bằng câu lệnh:
virtualenv env
Nếu dùng Mac thì có thể chạy pip -m virtualenv env

Câu lệnh sẽ tạo thư mục env
Chạy source env/Scripts/activate trong terminal bash để vào virtual environment

---------------------------------------------------------
Tạo một file .env với nội dung:
DB_PASSWORD = 'password của user postgres'
DB_USER = 'postgres'

// Nếu muốn sử dụng bằng user khác có thể tìm đọc trên mạng

Chạy sh init.sh để khởi tạo database, điền password của user postgres

Chạy sh data.sh nếu cần data, điền password của user postgres
Vì data chưa có nhiều nên có thể bổ sung sau.

Nếu cần sửa đổi database thì sửa trực tiếp vào file create_database rồi lại chạy lại sh init.sh

----------------------------------------------------------
Sau khi vào virtual environment, chạy:
pip install -r requirements.txt

Sau khi tải xong các modules cần thiết thì có thể chạy:
flask run

Câu lệnh sẽ cho ra một link http://127.0.0.1:5000 là trang homepage

----------------------------------------------------------
Quan trọng là code hết các functions, triggers trong file /flask_website/sql

Tối đã demo 1 file