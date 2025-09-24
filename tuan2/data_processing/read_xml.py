from bs4 import BeautifulSoup

with open('../../datasets/SalesTransactions.xml', 'r') as f:
    data = f.read()

bs_data = BeautifulSoup(data, 'xml')

UelSample = bs_data.find_all('UelSample')
print(UelSample)

