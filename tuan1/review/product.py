class Product:
#__init__ là phương thức khởi tạo (constructor) của lớp, được gọi tự động khi một đối tượng của lớp product được tạo.
    def __init__(self, id=None, name=None, quantity=None, price=None):
        self.id = id
        self.name = name
        self.quantity = quantity
        self.price = price
#__str__ là một phương thức đặc biệt trong Python, được gọi khi bạn sử dụng hàm print() hoặc str() trên một đối tượng của lớp.
    def __str__(self):
        return f"{self.id}\t{self.name} {self.quantity} {self.price}"
