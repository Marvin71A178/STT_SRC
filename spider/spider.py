from bs4 import BeautifulSoup
# import asyncio
import requests
import json
import re
from bs4 import element as el

class Novel():
    def __init__(self , url):
        self.url = url
        self.headers = {
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
        self.have_spider = False

    
    def check_website(self):
        website_type = ['wenku8']
        for i in website_type:
            if i in self.url:
                func = 'self.'+ i +'_spider()'
                self.have_spider = True
                try:
                    eval(func)
                except Exception as e:
                    print(e)
                    return
    
    def wenku8_spider(self):
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
                    # print(find_all_td)
                    for j in find_all_td:
                        if j.find('a'):
                            dic_subtitle = j.text
                            dic_url = j.find('a')['href']
                            dic[dic_title].append({'subtitle':str(dic_subtitle),'url':str(dic_url)})
            # print(dic)
            return [title , dic]
        match = re.search(r'id=(\d+)', self.url)
        extracted_id = match.group(1) if match else None
        article_page_url = 'https://www.wenku8.net/modules/article/articleinfo.php?id=' + str(extracted_id)
        reader_page_url = 'https://www.wenku8.net/modules/article/reader.php?aid=' + str(extracted_id)
        
        art = res_article(article_page_url, self.headers)
        tf = res_reader(reader_page_url, self.headers)
        dic = {
            'title':tf[0],
            'img' : art['img'],
            'brife_content' : art['brife_content'],
            'content' : tf[1],
        }
        with open(f'./{extracted_id}.json' , 'w', encoding='utf-8') as f:
            json.dump(dic, f, ensure_ascii=False, indent=4)
        
        self.dic = dic
        return 
    
class Novel_content():
    def __init__(self , url):
        self.url = url
        self.headers = {
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
        self.content = None
        
    def check_website(self):
        website_type = ['wenku8']
        print('finding content in such url')
        print(self.url)
        for i in website_type:
            if i in self.url:
                func = 'self.'+ i +'_spider()'
                self.have_spider = True
                try:
                    eval(func)
                except Exception as e:
                    print(e)
                    return
    def wenku8_spider(self):
        print('runnubg wenku8 content spider')
        pattern = r"^(.*?)&"
        match = re.search(pattern, self.url)
        if match:
            result = match.group(1)
            self.headers['Referer'] = result
        else:
            print("no source url found")
            
        res = requests.get(self.url, headers=self.headers)
        res.encoding = 'GB18030'
        soup = BeautifulSoup(res.text, 'html.parser')
        try:
            all_content = soup.find('div' ,{'id':'content'})
            contents = all_content.find_all(string=True)
            content = "\n\t".join(Content.strip() for Content in contents)
            self.content = content
            return content
        except:
            return None
        
if __name__ == '__main__':
    # test = Novel('https://www.wenku8.net/modules/article/reader.php?aid=1787')
    # print(test.dic)
    test2 = Novel_content('https://www.wenku8.net/modules/article/reader.php?aid=1787&cid=61153')
    print(test2.content)
    