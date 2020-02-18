import os
import requests
import pandas as pd
import numpy as np
import datetime
from bs4 import BeautifulSoup
import re
import time
yes_final_result = pd.DataFrame(columns=['name','address', 'google'])
for i in range(1, 16):
    page = i
    yes_url = 'http://www.yeschain.com.tw/stores.php?page={page}'.format(page=page)

    yes_resp = requests.get(yes_url)
    yes_resp.encoding = 'utf8' # using utf8
    yes_soup = BeautifulSoup(yes_resp.text, 'html5lib')
    temp = yes_final_result
    index=1
    page_result = pd.DataFrame(columns=['name','address', 'google'])
    item_list = yes_soup.find_all("div", class_='stores-list-single-item')
    for item in item_list:
            item_name = item.find("div", class_='wrap').text
            item_add = item.find(text='地址')
            p = item_add.parent
            item_address = p.findNext("div", class_='color-grey-500').text
            item_google = item.find("a", class_='btn-view-more')['href']
            item_dict = {'name':item_name,'address':item_address, 'google':item_google}
            page_result.loc[index] = item_dict
            index = index +1
            yes_final_result = temp.append(page_result)

you_final_result = pd.DataFrame(columns=['name','address', 'google'])
for i in range(1, 5):
    page = i
    you_url = 'http://www.yourchance.com.tw/index.php?option=module&lang=cht&task=showlist&id={page}&index={page}'.format(page=page)

    you_resp = requests.get(you_url)
    you_resp.encoding = 'utf8' # using utf8
    you_soup = BeautifulSoup(you_resp.text, 'html5lib')
    temp = you_final_result
    index=1
    page_result = pd.DataFrame(columns=['name','address', 'google'])
    shops = you_soup.find("div", class_='shoplist')
    item_list = shops.find_all("li")
    for item in item_list:
            item_name = item.find("div", class_='title').text
            item_address = item.find("div", class_='ad').text.replace("地　址：", "")
            item_google = item.find("a")['href']
            item_dict = {'name':item_name,'address':item_address, 'google':item_google}
            page_result.loc[index] = item_dict
            index = index +1
            you_final_result = pd.concat([temp, page_result])

pro_final_result = pd.DataFrame(columns=['name','address', 'google'])
for i in range(26, 31):
    id = i
    pro_url = 'http://www.prohealthcare.com.tw/store.php?cID={id}'.format(id=id)

    pro_resp = requests.get(pro_url)
    pro_resp.encoding = 'utf8' # using utf8
    pro_soup = BeautifulSoup(pro_resp.text, 'html5lib')
    temp = pro_final_result
    index=1
    page_result = pd.DataFrame(columns=['name','address', 'google'])
    shops = pro_soup.find(id='content_2')
    item_list = shops.find_all("div")
    for item in item_list:
        item_name = item.find("div", class_="t13_2")
        item_address = item.find("div", id="store_3")

        if item_name:
                item_dict = {'name':item_name.find("a").text.strip(),'address':item_address.text, 'google':"https://www.google.com.tw/maps/place/"+item_address.text}
                page_result.loc[index] = item_dict
                index = index +1
                pro_final_result = pd.concat([temp, page_result])

cid = 26
page = 2
pro2_url = 'http://www.prohealthcare.com.tw/store.php?cID={cid}&page={page}'.format(cid=cid, page=page)
pro2_final_result = pd.DataFrame(columns=['name','address', 'google'])
pro2_resp = requests.get(pro2_url)
pro2_resp.encoding = 'utf8' # using utf8
pro2_soup = BeautifulSoup(pro2_resp.text, 'html5lib')

index=1
page_result = pd.DataFrame(columns=['name','address', 'google'])
shops2 = pro2_soup.find(id='content_2')
item_list = shops2.find_all("div")
for item in item_list:
    item_name = item.find("div", class_="t13_2")
    item_address = item.find("div", id="store_3")
    
    if item_name:
            item_dict = {'name':item_name.find("a").text.strip(),'address':item_address.text, 'google':"https://www.google.com.tw/maps/place/"+item_address.text}
            page_result.loc[index] = item_dict
            index = index +1
            result = pd.concat([pro2_final_result, page_result])
pro_final_result = result.append(pro_final_result)

tree_final_result = pd.DataFrame(columns=['name','address', 'google'])

tree_url = 'https://www.greattree.com.tw/stores'
tree_resp = requests.get(tree_url)
tree_resp.encoding = 'utf8' # using utf8
tree_soup = BeautifulSoup(tree_resp.text, 'html5lib')
temp = tree_final_result
index=1
page_result = pd.DataFrame(columns=['name','address', 'google'])
shops = tree_soup.find(class_="page-search-resault")
item_list = shops.find_all("li", class_='address')
for item in item_list:
        item_name = item.find("div", class_='rd fcolor-main fwb').text
        item_address = item.find("div", class_='rd rd-line').find("span").text
        item_google = item.find("a")['href']
        item_dict = {'name':item_name,'address':item_address, 'google':item_google}
        page_result.loc[index] = item_dict
        index = index +1
        tree_final_result = pd.concat([temp, page_result])

writer = pd.ExcelWriter('med_shops.xlsx',options={'strings_to_urls': False})
yes_final_result.reset_index().to_excel(writer,'躍獅')
you_final_result.reset_index().to_excel(writer,'佑全')
pro_final_result.reset_index().to_excel(writer,'博登')
tree_final_result.reset_index().to_excel(writer,'大樹')
writer.save()