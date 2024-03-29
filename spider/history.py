from bs4 import BeautifulSoup
# import asyncio
import requests
import json
# import time
# import datetime
# import base64
# import aiohttp
import re
from bs4 import element as el
# vim test.py
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# options = Options()
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# driver.get("https://www.wenku8.net/modules/article/reader.php?aid=1787&cid=61149")
# print(driver.page_source)
# driver.close()


url = 'https://www.wenku8.net/modules/article/reader.php?aid=1787'
url2 = 'https://www.wenku8.net/modules/article/articleinfo.php?&id=1787'
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cache-Control": "max-age=0",
    "Sec-Ch-Ua": "\"Google Chrome\";v=\"119\", \"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}
def res_article(url, headers):
    
    res = requests.get(url , headers=headers)
    res.encoding = 'GB18030'
    soup = BeautifulSoup(res.text, 'html.parser')
        
    content = soup.find(id="content")
    first_div = content.find('div')
    second_table = first_div.find_all('table')[2]
    book_titleimg = second_table.find('img')['src']
    brief_content_html = second_table.find_all('span' , {'style':"font-size:14px;"})
    brief_contents = brief_content_html[-1].find_all(text=True)
    brief_content = "\n".join(Content.strip() for Content in brief_contents)
    # print(book_titleimg)
    # print(brief_content)
    return {'img':book_titleimg, 'brife_content':brief_content}


def res_reader(url , headers):
    dic = {}
    res = requests.get(url , headers=headers)
    res.encoding = 'GB18030'
    soup = BeautifulSoup(res.text, 'html.parser')
    title = soup.find('div' , {'id':'title'}).text
    body = soup.find('body')
    tb = body.find('table' , {"class":"css", "border":"0" ,"align":"center", "cellpadding":"3", "cellspacing":"1"})
    dic_title =''
    for i in tb.children:
        if not (type(i) is el.Tag):
            continue
        
        if i.find('td' , {"class" : "vcss"}):
            dic_title = i.find('td' , {"class" : "vcss"}).text
            dic[dic_title] = []
        elif i.find('td', {"class" : "ccss"}):
            find_all_td = i.find_all('td', {"class" : "ccss"})
            print(find_all_td)
            for j in find_all_td:
                if j.find('a'):
                    dic_subtitle = j.text
                    dic_url = j.find('a')['href']
                    dic[dic_title].append({'subtitle':str(dic_subtitle),'url':str(dic_url)})
    print(dic)
    return [title , dic]
                
                
    
inputUrl = 'https://www.wenku8.net/modules/article/reader.php?aid=1787'
# async def fetch(title ,subtitle , url ,reader_page_url):
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
#         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#         "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
#         "Referer": reader_page_url,
#         "Cookie": "Hm_lvt_d72896ddbf8d27c750e3b365ea2fc902=1678850557; jieqiUserCharset=big5; Hm_lvt_d72896ddbf8d27c750e3b365ea2fc902=; Hm_lvt_acfbfe93830e0272a88e1cc73d4d6d0f=1702118034,1702272435; cf_clearance=e1bJGZHElBAARp1WxhV245MJIRFTNvX3QOs2mMIoO6g-1702278663-0-1-bde4e9ea.5b6c2084.938dbfa-0.2.1702278663; Hm_lvt_b74ae3cad0d17bb613b120c400dcef59=1702279094; Hm_lpvt_acfbfe93830e0272a88e1cc73d4d6d0f=1702287003; Hm_lpvt_b74ae3cad0d17bb613b120c400dcef59=1702287006; Hm_lpvt_d72896ddbf8d27c750e3b365ea2fc902=1702287006"

#     }

#     async with aiohttp.ClientSession(headers=headers) as session:
#         await asyncio.sleep(random.uniform(0.5, 1)) 
#         async with session.get(url) as res:
#             pagehtml = await res.text(encoding="GB18030")
#             with open('wenku8.html', 'w', encoding='utf-8') as f:
#                 f.write(pagehtml)
#             soup = BeautifulSoup(pagehtml, 'html.parser')
#             try:
#                 all_content = soup.find('div' ,{'id':'content'})
#                 contents = all_content.find_all(string=True)
#                 content = "\n".join(Content.strip() for Content in contents)
#                 return [title, subtitle, content]
#             except:
#                 return [title, subtitle, None]
# async def selenium_fetch(title , subtitle , url , driver ,reader_page_url):
#     driver.get(reader_page_url)
#     time.sleep(0.5)
#     driver.get(url)
#     print(url)
#     soup = BeautifulSoup(driver.page_source, 'html.parser')
#     try:
#         all_content = soup.find('div' ,{'id':'content'})
#         contents = all_content.find_all(string=True)
#         content = "\n".join(Content.strip() for Content in contents)
#         return [title, subtitle, content]
#     except:
#         return [title, subtitle, None]
    
    

# async def main(headers):
def main(headers ,  inputUrl ):
    if 'www.wenku8.net' in  inputUrl:
        match = re.search(r'id=(\d+)', inputUrl)
        extracted_id = match.group(1) if match else None
        
        article_page_url = 'https://www.wenku8.net/modules/article/articleinfo.php?id=' + str(extracted_id)
        reader_page_url = 'https://www.wenku8.net/modules/article/reader.php?aid=' + str(extracted_id)
        # print(res_article(article_page_url, headers))
        # print(res_reader(reader_page_url, headers))
        art = res_article(article_page_url, headers)
        tf = res_reader(reader_page_url, headers)
        dic = {
            'title':tf[0],
            'img' : art['img'],
            'brife_content' : art['brife_content'],
            'content' : tf[1],
        }
        return dic 
        with open('wenku8.json', 'w', encoding='utf-8') as f:
            json.dump(dic, f, ensure_ascii=False, indent=4)
        # print(123)
    else:
        print('unknow url')
        
# asyncio.run(main(headers,driver,inputUrl))
def create_catalog(inputUrl):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control": "max-age=0",
        "Sec-Ch-Ua": "\"Google Chrome\";v=\"119\", \"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    return main(headers,inputUrl)

def search_content(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    pattern = r"^(.*?)&"

    # 使用正则表达式搜索
    match = re.search(pattern, url)
    if match:
        result = match.group(1)
        headers['Referer'] = result
    else:
        print("no source url found")
    
    res = requests.get(url, headers=headers)
    res.encoding = 'GB18030'
    soup = BeautifulSoup(res.text, 'html.parser')
    try:
        all_content = soup.find('div' ,{'id':'content'})
        contents = all_content.find_all(string=True)
        content = "\n".join(Content.strip() for Content in contents)
        return content
    except:
        return None

if __name__ == '__main__':
    url = 'https://www.wenku8.net/modules/article/reader.php?aid=1787&cid=61148'
    print(search_content(url))
    print(create_catalog(url))