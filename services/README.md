# Phân tích

## Ý nghĩa chuyên môn
+ Tạo vote lịch họp
+ Thời gian cụ thể (Đồng bộ nhiều múi giờ) -> Phù hợp cho cuộc họp online đa quốc gia
+ Xem được khung giờ cụ thể nào nhiều người trống nhất

## Tính năng

### Đăng nhập
* Điền định danh
* Mật khẩu
* Chuyển sang đăng ký
* Đăng nhập

### Đăng ký
* Điền định danh
    1. Kiểm tra sự tồn tại trong db
    2. Lưu trữ và mã hóa
    3. 
* Mật khẩu
* Nhâp lại mật khẩu
* Chuyển sang đăng nhập
* Đăng ký

### Bắt buộc đăng nhập
* Tự động chuyển sang trang đăng nhập
* Bắt buộc đăng nhập

### Tạo cuộc họp

### Quản lý cuộc họp

### Vote cuộc họp

# Thiết kế
## Database
### users
* id (Integer): ID định danh [PRIMARY KEY - AUTOINCREMENT]
* username (varchar): Tài khoản [nn]
* password (varchar): Mật khẩu - Mã hóa [nn]
* createAt (Timestamp): Thời gian tạo tài khoản [nn]
* lastLogin (Timestamp): Lần cuối đăng nhập (Sau 1 tháng không sử dụng -> Xóa Tài khoản) [DEFAULT CURRENT]

### meetings
* id (Integer): ID định danh cuộc họp [PRIMARY KEY - AUTOINCREMENT]
* ownerId (Integer): ID Người tạo [FOREIGN KEY -> users(id)]
* title (Text): Tiêu đề của cuộc họp [optional]
* description (Text): Mô tả cuộc họp [optional]
* createdAt (TIMESTAMP): Thời gian tạo bình chọn [DEFAULT CURRENT]

### Availabilities
> Lưu trữ các thông tin về việc `userId` rảnh ở khung giờ `time` cho cuộc hợp `meetingId` hay không

* id (Integer): Id Định danh [PRIMARY KEY AUTOINCREMENT],
* meetingId (INTEGER): ID của cuộc họp [FOREIGN KEY -> meetings(id)]
* userId (INTEGER): ID của người dùng [FOREIGN KEY -> users(id)]
* date (DATE): Ngày rảnh
* time (TIME): Khung thời gian cụ thể trong ngày (30 phút/ khung)

## Class Python

### User

#### Thuộc tính:

* `id`: ID định danh người dùng (int)
* `username`: Tài khoản đăng nhập (str)
* `password`: Mật khẩu đã mã hóa (str)
* `createAt`: Thời gian tạo tài khoản (datetime)
* `lastLogin`: Thời điểm đăng nhập gần nhất (datetime)

#### Phương thức:

* `register(username, password)`: Đăng ký tài khoản mới (mã hóa, kiểm tra trùng)
* `login(username, password)`: Kiểm tra đăng nhập với mật khẩu đã mã hóa
* `update_last_login()`: Cập nhật thời gian đăng nhập gần nhất
* `is_inactive(threshold_days=30)`: Kiểm tra nếu tài khoản không đăng nhập trong thời gian dài
* `delete_if_inactive()`: Tự động xoá tài khoản nếu không hoạt động theo chính sách

---

### Class: `Meeting`

**Thuộc tính:**

* `id`: `int` – ID cuộc họp
* `owner_id`: `int` – ID người tạo (liên kết với `User.id`)
* `title`: `str | None` – Tiêu đề cuộc họp
* `description`: `str | None` – Mô tả cuộc họp
* `created_at`: `datetime` – Thời gian tạo

**Phương thức:**

* `create(owner_id, title, description)` – Tạo một cuộc họp mới
* `get_by_id(meeting_id)` – Truy xuất cuộc họp theo ID
* `get_all_by_user(user_id)` – Lấy danh sách cuộc họp của người dùng
* `delete(meeting_id)` – Xoá một cuộc họp
* `get_participants(meeting_id)` – Truy xuất danh sách người tham gia
* `get_availability_summary(meeting_id)` – Tổng hợp khung giờ được chọn nhiều nhất

---

### Class: `Availability`

**Thuộc tính:**

* `id`: `int`
* `meeting_id`: `int` – Liên kết với `Meeting.id`
* `user_id`: `int` – Liên kết với `User.id`
* `date`: `date` – Ngày rảnh (dạng `YYYY-MM-DD`)
* `time`: `time` – Giờ rảnh (dạng `HH:MM:SS`, mỗi khung 30 phút)

**Phương thức:**

* `add(meeting_id, user_id, date, time)` – Thêm một khung giờ
* `remove(meeting_id, user_id, date, time)` – Xoá khung giờ
* `get_by_user(user_id, meeting_id)` – Lấy khung giờ người dùng đã chọn
* `get_by_meeting(meeting_id)` – Lấy tất cả khung giờ của cuộc họp
* `get_common_slots(meeting_id)` – Phân tích các khung giờ chung
* `count_votes_for_slot(meeting_id, date, time)` – Đếm số vote cho một khung giờ

---

### Class: `Database`

**Thuộc tính:**

* `db_path`: `str` – Đường dẫn file SQLite
* `conn`: `sqlite3.Connection`
* `cursor`: `sqlite3.Cursor`

**Phương thức:**

* `connect()` – Kết nối tới DB
* `create_tables()` – Tạo bảng `users`, `meetings`, `availabilities`
* `execute(query, params=())` – Thực thi một câu lệnh SQL
* `fetch_one(query, params=())` – Lấy một dòng dữ liệu
* `fetch_all(query, params=())` – Lấy nhiều dòng dữ liệu
* `commit()` – Ghi thay đổi xuống DB
* `close()` – Đóng kết nối
* `reset()` – Xoá toàn bộ dữ liệu (nếu cần)

---

### Class: `EventManager`

**Thuộc tính:**
* `user`
* `db`: `Database` – Thể hiện kết nối cơ sở dữ liệu
* `sessions`: `dict[int, dict]` – Lưu các phiên làm việc đang hoạt động
* `login_time`
* `active`

**Phương thức:**
* `end_session()` – Giải phóng phiên
* get_profile() -> dict
* `is_active() -> bool` – Kiểm tra trạng thái hoạt động
* `get_user_info()` – Truy vấn thông tin người dùng
* get_my_meetings() -> list[dict]
* get_meeting_participants(meeting_id: int) -> list[dict]
* get_availabilities(meeting_id: int) -> list[dict] – Lấy khung giờ người dùng hiện tại đã chọn
* create_meeting
* add_availability
* remove_availability
* update_profile