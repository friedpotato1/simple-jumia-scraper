import requests,time,sqlite3
from bs4 import BeautifulSoup
def scraper(page):
    site = "https://www.jumia.co.ke/flash-sales/?page="+page+"#catalog-listing"
    site2 = "https://www.jumia.co.ke/catalog/?q=tv&page="+page+"#catalog-listing"
    res = requests.get(site2)
    res.raise_for_status()
    soup = BeautifulSoup(res.text,'lxml')
    items = soup.select('.name')
    prices = soup.select('.prc')

    items_list = []
    prices_list = []

    for i in items:
       items_list.append(i.text)
    for j in prices:
       prices_list.append(j.text)
   
    new_price = []
    newer = []
    
    for x in prices_list:
       x =  x.split('KSh')
       new_price.append([x[-1]])
   
    
    for o in new_price:
       string = o[0].split(',')
       string = ''.join(string)
       newer.append(string)
   
    for it in range(len(items_list)):
       
      conn = sqlite3.connect("sales.sqlite")
      
      curr = conn.cursor()
      
      curr.execute("INSERT INTO Flash(item,price) VALUES(?,?)",(items_list[it],newer[it]))
      
      conn.commit()
      
   
   

    #if len(items_list) == len(prices_list):
       #print("Here Are The Flash Sale Items".center(50,'*'),'\n')
      # for i in range(len(items_list)):
       #   print(f"""{items_list[i]} @ {prices_list[i]}\n""")
    #print("\n\n\n")
conn = sqlite3.connect("sales.sqlite")
    
curr = conn.cursor()
   
curr.execute("DROP TABLE IF EXISTS Flash")

curr.execute("CREATE TABLE Flash(item_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,item TEXT,price INTEGER)")

for i in range(51):
   if i == 0:
      continue
   scraper(str(i))
   # answer = str(input('Would you like to view next page -- yes or no > '))
    #print("\n\n\n")
    #if answer.lower() == "no":
     #   break