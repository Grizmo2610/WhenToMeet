import re

def check_password(password: str) -> bool:
    if len(password) < 8:
        return False
    if password.isalpha():
        return False  # chỉ toàn chữ
    if password.isdigit():
        return False  # chỉ toàn số
    if not re.search(r"[A-Z]", password):
        return False  # không có chữ in hoa
    if not re.search(r"[a-z]", password):
        return False  # không có chữ thường
    if not re.search(r"[0-9]", password):
        return False  # không có số
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False  # không có ký tự đặc biệt
    return True
