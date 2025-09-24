class ListProduct:
    def __init__(self):
        self.products=[]
    def add_product(self,p):
        self.products.append(p)
#Sử dụng phương thức append của danh sách để thêm p vào cuối danh sách self.products.
    def print_products(self):
        for p in self.products:
            print(p)
    def desc_sort_products(self): #Sắp xếp danh sách self.products theo giá (price) giảm dần (từ lớn đến nhỏ).
        for i in range(0, len(self.products)):
            for j in range(i+1,len(self.products)):
                pi=self.products[i]
                pj=self.products[j]
                #Đổi tham số khác đổi giá trị
                if pi.price < pj.price:
                    self.products[j]=pi
                    self.products[i]=pj