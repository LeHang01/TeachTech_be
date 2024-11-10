import itertools

# Danh sách các lựa chọn cho mỗi cột
Date = ['Empty', 'Default', 'Select a date (10/11/2024)']
Pump_type = ['Empty', 'Select a option (ex: LK)', 'Select multiple (ex: LK, MDG,..)']
Status = ['Empty', 'Select a option (ex: Proccessing)', 'Select multiple (ex: Proccessing, Completed)']
Search = ['Empty', 'Duplicate keywords', 'No duplicate keywords']

# Tạo tất cả các tổ hợp
combinations = list(itertools.product(Date, Pump_type, Status, Search))


# Hàm để trả về kết quả mô tả dựa trên mỗi tổ hợp
def get_result(date, pump_type, status, search):
    # Nếu Search là 'No duplicate keywords', trả về "Trả về kết quả rỗng" và không xét các trường hợp khác
    if search == 'No duplicate keywords':
        return "Trả về kết quả rỗng"

    result = []

    # Xử lý cột Date
    if date == 'Empty':
        result.append("Tìm kiếm trong vòng 30 ngày trước")
    elif date == 'Default':
        result.append("Mặc định ngày hiện tại")
    elif date.startswith('Select a date'):
        result.append("Trả về kết quả những package ngày đã chọn")

    # Xử lý cột Pump_type
    if pump_type == 'Empty':
        result.append("Bỏ qua Pump_type, hiển thị các filter khác")
    elif pump_type == 'Select a option (ex: LK)':
        result.append("Hiển thị những package có Pump_type 'LK'")
    elif pump_type == 'Select multiple (ex: LK, MDG,..)':
        result.append("Hiển thị những package có Pump_type 'LK' và 'MDG'")

    # Xử lý cột Status
    if status == 'Empty':
        result.append("Bỏ qua Status")
    elif status == 'Select a option (ex: Proccessing)':
        result.append("Hiển thị những package có Status 'Processing'")
    elif status == 'Select multiple (ex: Proccessing, Completed)':
        result.append("Hiển thị những package có Status 'Processing' và 'Completed'")

    # Xử lý cột Search
    if search == 'Empty':
        result.append("Bỏ qua Search")
    elif search == 'Duplicate keywords':
        result.append("Hiển thị những package trùng với từ khóa")

    return " và ".join(result)


# Lọc và hiển thị các tổ hợp hợp lệ cùng với kết quả
for combo in combinations:
    date, pump_type, status, search = combo
    # Loại bỏ các trường hợp mà tất cả các cột đều là "Empty"
    if date == 'Empty' and pump_type == 'Empty' and status == 'Empty' and search == 'Empty':
        continue  # Bỏ qua tổ hợp không hợp lệ

    result = get_result(date, pump_type, status, search)
    print(f"Combination: {combo} -> Result: {result}")
