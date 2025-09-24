from tuan1.review.product import Product
from tuan1.review.products import ListProduct

lp=ListProduct()
lp.add_product(Product(100, "Product 1", 200, 10))
lp.add_product(Product(200, "Product 2", 300, 10))
lp.add_product(Product(100, "Product 3", 400, 10))
lp.add_product(Product(100, "Product 4", 500, 10))
lp.add_product(Product(100, "Product 5", 600, 10))
print("List of Prducts:")
lp.print_products()
#Bổ sung thêm hàm sắp xếp sản phẩm theo đơn giá giảm dần: dùng 2 vòng lặp lồng nhàu, ...
lp.desc_sort_products()
print("List of Products after decending sort:")
lp.print_products()


