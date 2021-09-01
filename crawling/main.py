## 작성 2021-06-30  - 이유인 



from crawling.coupang_crawler import coupangCrawler
print(__name__)
if __name__ =='__main__':
    cc = coupangCrawler()
    cc.search_listup()
    cc.item_search()
    cc.item_review()