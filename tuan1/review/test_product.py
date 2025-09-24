from tuan1.review.product import Product

p1=Product(100, "Thuốc lào", 14, 20)
#Ô nhớ trên thanh ram tồn tại độc lập với ô nhớ mình cấp phát
# --> p1 thay đổi dữ liệu thì p2 không thay đổi
"""
alias: một ô nhớ có thể có nhìu đứa quản lý _ garbage collectiopn: tự động thu hồi ô nhớ???
---> 1 thằng thay đổi thì thằng kia cũng đổi
"""
#Xuất p1 ra màn hình:
print(p1)
p2=Product(200, "Thuốc trị hôi nách", 5, 30)
p1=p2
print("Thông tin của p1=")
print(p1)
"""
Dòng này không tạo bản sao của đối tượng p2. Thay vào đó, nó làm cho p1 trỏ đến cùng ô nhớ mà p2 đang trỏ tới.
p1 và p2 giờ là alias (bí danh) của cùng một đối tượng. Đối tượng ban đầu của p1 (với id=100, name="Thuốc lào") 
không còn được tham chiếu bởi biến nào và sẽ được garbage collector thu hồi.
"""
p1.nam="Thuốc tăng tự trọng"
print("Thông tin của p2=")
print(p2)