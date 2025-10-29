from tkinter import *

# Danh sách các tùy chọn cho Dropdown Menu
OPTIONS = [
    "model 1",
    "model 2",
    "model 3"
]

# Tạo cửa sổ chính
root = Tk()

# Biến để lưu trữ giá trị được chọn
variable = StringVar(root)
# Đặt giá trị mặc định là phần tử đầu tiên trong OPTIONS
variable.set(OPTIONS[0]) # default value

# Tạo Dropdown Menu (OptionMenu)
w = OptionMenu(root, variable, *OPTIONS)
w.pack()

# Định nghĩa hàm được gọi khi nhấn nút "OK"
def ok():
    # In ra giá trị hiện tại của biến (giá trị đã chọn)
    print("value is:" + variable.get())

# Tạo nút "OK" và gán hàm ok() vào lệnh
button = Button(root, text="OK", command=ok)
button.pack()

# Khởi chạy vòng lặp sự kiện chính của Tkinter
mainloop()