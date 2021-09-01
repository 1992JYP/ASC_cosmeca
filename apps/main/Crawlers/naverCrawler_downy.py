from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.views.generic import TemplateView

from django.views import View
from apps.paradise import models as lpmodels
from apps.main import models
from apps.main.models import NvProduct
from apps.main.models import NvReview

from selenium import webdriver as wb
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pandas as pd
from selenium.webdriver.common.alert import Alert
from openpyxl import load_workbook
import chromedriver_autoinstaller
import operator

class naverCrawler:
    def __init__(self):
        url = 'https://shopping.naver.com/'
        options = wb.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")

        chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]  #크롬드라이버 버전 확인

        try:
            self.driver =  wb.Chrome(f'./{chrome_ver}/chromedriver.exe', chrome_options = self.options)   
        except:
            chromedriver_autoinstaller.install(True)
            self.driver =  wb.Chrome(f'./{chrome_ver}/chromedriver.exe', chrome_options = self.options)

        self.driver.get(url)
        #======================================================================================================
        self.reviewDF = pd.DataFrame(columns=['index', 'serial_number', 'text', 'score', 'option','review_date'])
        self.productDF = pd.DataFrame(columns = ['index', 'keyword', 'seller_name', 'reg_date', 'iis_ad', 'title', 'price', 'review_count', 'serial_number', 'prod', 'link', 'score_avg', 'image'])
        #======================================================================================================
        # 변수
        self.while_count = 0 # while 반복문 제어
        self.othercheck = 1 # 타사체크
        self.this_tem_number = 0 # 상품 태그 페이징
        self.index_number = 0 # 상품 인덱스에 붙는거
        self.re_next_num = 3 # 리뷰 태그 페이징
        self.re_index = 0 # 리뷰 인덱스에 붙는거
        #======================================================================================================
        load_bb = load_workbook("C:/Users/user/Desktop/코스메카코리아 + 생활낙원/매칭키워드_정리_URL 매칭.xlsx", data_only=True)
        load_ws = load_bb['Sheet1']

        list_file = []
        #지정한 셀 값
        get_cells = load_ws['F2' : 'F936']

        for row in get_cells:
            for cell in row:
                list_file.append(cell.value)

        new_list_file = []

        for now_list in list_file:         # 중복제거
            if now_list not in new_list_file:
                new_list_file.append(now_list)
        self.new_list_file = list(filter(None, new_list_file))# None 공백제거

        #======================================================================================================

        list_url = [] # 저거 불러온거 당을 리스트

        #지정한 셀의 값 출력
        get_cells = load_ws['H2' : 'H936']  # 저 안에 공통된것도 있고 빈칸도 있다 그거 걸러내야되

        for row in get_cells:
            for cell in row:
                list_url.append(cell.value) # 리스트에 담음

        new_list_url = []

        for now_list_url in list_url:
            if now_list_url not in new_list_url:
                new_list_url.append(now_list_url)
        self.new_list_url = list(filter(None, new_list_url))
        # 요거 url임 지들이 갖고있던건데 똑같으면 긁고 아니면 안긁을거임
        #====================================================================================================== 
    #====================================================================================================== 
    def smart(self):

        html = self.driver.page_source 
        soup_item = BeautifulSoup(html, "html.parser")
        smart_item_info = soup_item.select_one('div._2ZMO1PVXbA')

        th = self.driver.find_elements_by_css_selector('table > tbody > tr > th._1iuv6pLHMD')
        td = self.driver.find_elements_by_css_selector('table > tbody > tr > td.ABROiEshTD')
        
        dictkey = []
        dictvalue = []

        for ths in th:
            dictkey.append(ths.text)
        for tds in td:
            dictvalue.append(tds.text)

        # key값 상품번호 / 상품상태 / 제조사 / 브랜드 / 모델명 / 이벤트 / 사음품 / 원산지
        tables = dict(zip(dictkey, dictvalue))

        title = smart_item_info.select_one('h3').text
        print(f'title >> {title}')
        
        self.serial_number = tables['상품번호'].replace('<b>','')
        print(f'serial_number >> {self.serial_number}')

        price = smart_item_info.select_one('span._1LY7DqCnwR').text.replace(',','')
        print(f'price >> {price}')

        review_count = smart_item_info.select_one('strong._2pgHN-ntx6').text.replace(',','')
        print(f'review_count >> {review_count}')

        score_avg = smart_item_info.select_one('div._2Q0vrZJNK1 > strong._2pgHN-ntx6').text.replace('/5','')
        print(f'score_avg >> {score_avg}')
        
        image = smart_item_info.select_one('img').get('src')
        print(f'image >> {image}')

        link = self.driver.current_url
        print(f'link >> {link}')

        prod = tables['제조사']
        print(f'prod >> {prod}')

        # 하나씩 긁어 담어
        smart_item_infor = [title, price, review_count, self.serial_number, prod, link, score_avg, image]
        
        # 본사면 리뷰긁고 아니면 하지마
#         if link in self.new_list_url:
        # 위에 다 돌고 리뷰 진입
        self.smart_review()
        self.reviewDF.to_csv(f"naver_review_{self.pd_name}_{self.add_num}.csv", header = True, index=False, encoding="UTF-8")
            
        return smart_item_infor
    #======================================================================================================
    def smart_review(self):
        
        for i in range(2): # 스크롤내리기
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(0.3)
            
        try:
            # 한 페이지당 보여지는 리뷰갯수 20개
            review_tag_len = len(self.driver.find_elements_by_css_selector('#REVIEW > div > div._2y6yIawL6t > div > div.cv6id6JEkg > ul > li'))
            print('review_tag_len >> {}'.format(review_tag_len))
        except:
            pass
        
        try:
            # 페이징을 한장씩 할거니까 거 갯수 제한걸려 만든거
            smart_items_num = int(self.driver.find_element_by_css_selector('#REVIEW > div > div._2y6yIawL6t > div > div._1jXgNbFhaN > div.WiSiiSdHv3 > strong > span').text.replace('(','').replace(')','').replace(',',''))
            in_number = round(smart_items_num / review_tag_len)
            print(f'in_number >> {in_number}')
        except:
            pass
        
        if in_number > 100: #리뷰 초대가 2000개라 
            in_number = 99
        
        # 최신버튼
        self.driver.find_element_by_css_selector('#REVIEW > div > div._2y6yIawL6t > div > div._1jXgNbFhaN > div.WiSiiSdHv3 > ul > li:nth-child(2) > a').send_keys(Keys.ENTER)

#         try:
        for index in range(in_number): # 페이징 태그갯수

            html = self.driver.page_source
            soup_item = BeautifulSoup(html, "html.parser")
            smart_items = soup_item.select_one('ul.TsOLil1PRz')

            for smart_item in smart_items:
                self.re_index += 1
                text = smart_item.select_one('div.YEtwtZFLDz > span._3QDEeS6NLn').text
                print(f'text >> {text}')

                score = smart_item.select_one('div._2V6vMO_iLm > em._15NU42F3kT').text
                print(f'score >> {score}')
                try:
                    option = smart_item.select_one('button._3jZQShkMWY > span._3QDEeS6NLn').text
                except:
                    option = None
                print(f'option >> {option}')

                review_date = smart_item.select_one('div._2FmJXrTVEX > span._3QDEeS6NLn').text
                print(f'review_date >> {review_date}')
                
                NvReview(
                pd_index = self.re_index,
                serial_number = self.serial_number,
                review_text = text,
                score = score,
                p_option = option,
                review_date = review_date,
                ).save()
                
                
                 #리뷰 담는거
                self.reviewDF.loc[len(self.reviewDF)] = [self.re_index, self.serial_number, text, score, option, review_date ]
                print('♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥') 
            time.sleep(1.8)

            try:
                re_pageing_buton = self.driver.find_element_by_css_selector('#REVIEW > div > div._2y6yIawL6t > div > div.cv6id6JEkg > div > div > a:nth-child(%d)'%self.re_next_num)
                re_pageing_buton.send_keys(Keys.ENTER)
                re_pageing_buton_text = re_pageing_buton.text
                print(f're_pageing_buton_text >> {re_pageing_buton_text}')

                if re_pageing_buton_text == '다음':
                    self.re_next_num = 3
                elif re_pageing_buton_text == '100':
                    break
                else:
                    self.re_next_num += 1
            except:
                break
#         except:
#             pass
    #====================================================================================================== 
    def search(self):

        html = self.driver.page_source 
        soup_item = BeautifulSoup(html, "html.parser")
        search_item_info1 = soup_item.select_one('div.top_summary_title__15yAr')

        title = search_item_info1.select_one('h2').text
        print(f'title >> {title}')

        html = self.driver.page_source 
        soup_item = BeautifulSoup(html, "html.parser")
        search_item_info2 = soup_item.select_one('div.style_content_wrap__2VTVx')
        
        link = self.driver.current_url
        
        serial_number = link[42:53]
        print(f'serial_number >> {serial_number}') #일단 보류

        price = search_item_info2.select_one('em.lowestPrice_num__3AlQ-').text
        print(f'price >> {price}')

        review_count = search_item_info2.select_one('li.filter_on__X0_Fb > a > em').text.replace('(','').replace(')','').replace(',','')
        print(f'review_count >> {review_count}')

        score_avg = search_item_info2.select_one('div.totalArea_value__3UEUi').text.replace('/5','')
        print(f'score_avg >> {score_avg}')

        image = search_item_info2.select_one('img').get('src')
        print(f'image >> {image}')

        
        print(f'link >> {link}')

        th = self.driver.find_elements_by_css_selector('#__next > div > div.style_container__3iYev > div.style_inner__1Eo2z > div.top_summary_title__15yAr > div.top_info_inner__1cEYE > span.top_cell__3DnEV')
        td = self.driver.find_elements_by_css_selector('#__next > div > div.style_container__3iYev > div.style_inner__1Eo2z > div.top_summary_title__15yAr > div.top_info_inner__1cEYE > span.top_cell__3DnEV > em')

        search_dictkey = []
        search_dictvalue = []

        for ths in th:
            search_dictkey.append(ths.text)
        for tds in td:
            search_dictvalue.append(tds.text)

        keylist = []
        valuelist =[]
        for dic in search_dictkey:
            for em in search_dictvalue:
                num = dic.find(em)
                if num>-1:
                    keylist.append(dic[:num-1])
                    valuelist.append(em)    

        info_tables = dict(zip(keylist, valuelist))

        try:
            prod = info_tables['제조사']
        except:
            prod = None

        print(f'prod >> {prod}')

        search_item_infor = [title, price, review_count, serial_number, prod, link, score_avg, image]
        self.search_review()
        
        return search_item_infor
#====================================================================================================== 
    def search_review(self):
        
        for i in range(2): # 스크롤내리기
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(0.3)
            
        try:
            # 한 페이지당 보여지는 리뷰갯수 20개
            review_tag_len = len(self.driver.find_elements_by_css_selector('#section_review > ul > li'))
            print('review_tag_len >> {}'.format(review_tag_len))
        except:
            pass
        
        try:
            # 페이징을 한장씩 할거니까 거 갯수 제한걸려 만든거
            search_items_num = int(self.driver.find_element_by_css_selector('#section_review > div.filter_sort_group__Y8HA1 > div.filter_evaluation_tap__-45pp > ul > li.filter_on__X0_Fb > a > em').text.replace('(','').replace(')','').replace(',',''))
            in_number = round(search_items_num / review_tag_len)
            print(f'in_number >> {in_number}')
        except:
            pass
        
        if in_number > 100: #리뷰 초대가 2000개라 
            in_number = 99
        
        self.driver.find_element_by_css_selector('#section_review > div.filter_sort_group__Y8HA1 > div.filter_filter_box__iKVkl > div.filter_sort_box__223qy > a:nth-child(3)').click()
        
        self.se_next_num = 2
        
        for index in range(in_number): # 페이징 태그갯수
            html = self.driver.page_source
            soup_item = BeautifulSoup(html, "html.parser")
            seach_items = soup_item.select_one('ul.reviewItems_list_review__1sgcJ')
            
            for seach_item in seach_items:
                self.re_index += 1
                
                text = seach_item.select_one('p.reviewItems_text__XIsTc').text.replace('\n','')
                print('리뷰글 >> {}'.format(text))
                
                score = seach_item.select_one('span.reviewItems_average__16Ya-').text.replace('평점','')
                print('별점 >> {}'.format(score))
                
                option = None
                print(f'option >> {option}')
                
                review_date = seach_item.select_one('div.reviewItems_etc_area__2P8i3 > span:nth-of-type(4)').text
                print('날짜 >> {}'.format(review_date))
                
                NvReview(
                pd_index = self.re_index,
                serial_number = self.serial_number,
                review_text = text,
                score = score,
                p_option = option,
                review_date = review_date,
                ).save()
                
                #리뷰 담는거
                self.reviewDF.loc[len(self.reviewDF)] = [self.re_index, self.serial_number, text, score, option, review_date ]
                print('♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥') 
                
                
            try:
                self.driver.find_element_by_css_selector('#section_review > div.pagination_pagination__2M9a4 > a:nth-child(%d)'%self.se_next_num).send_keys(Keys.ENTER)
                review_tag_text = self.driver.find_element_by_css_selector('#section_review > div.pagination_pagination__2M9a4 > a:nth-child(%d)'%self.se_next_num).text
                time.sleep(1.5)
                if review_tag_text == '다음':
                    self.se_next_num = 3
                elif review_tag_text == '100':
#                     self.index_num = 0 # 또는 그냥 다 읽고나면 리셋
                    break
                else:
                    self.se_next_num += 1

            except:
                break
#====================================================================================================== 
    def in_crawling(self):
        title_url = self.driver.find_element_by_css_selector('#__next > div > div.style_container__1YjHN > div.style_inner__18zZX > div.style_content_wrap__1PzEo > div.style_content__2T20F > ul > div > div:nth-child(%d) > li > div > div.basicList_info_area__17Xyo > div.basicList_title__3P9Q7 > a'%self.this_tem_number)
        ## 선택한 제품 클릭  
        title_url.send_keys(Keys.RETURN)
        time.sleep(4)

        ## 제품 선택하고 생성된 새창으로 포커스 이동 
        last_tab = self.driver.window_handles[-1]
        self.driver.switch_to.window(window_name = last_tab)
        time.sleep(3)

        ## 해당 url 주소 가져오기 
        input_url = self.driver.current_url

        ## 가져온 주소에서 smartstore.naver.com 있는지 판단  -1 이 있다면 없음 
        naver_shop = input_url.find('smartstore.naver.com') #  주소안에스마트스토어만 찾아서 담아
    #===============================================================================        
        ## 불러온 url  -1 이면 
        if naver_shop == -1:

            naver_shop = input_url.find('search.shopping.naver.com')

            if naver_shop == -1:
                c_type = -1

            else :
                c_type = 2

        else :
            c_type = 1
    #===============================================================================

        if c_type == 1:
            smart_infor = self.smart()

            self.driver.close()
            last_tab = self.driver.window_handles[0]
            self.driver.switch_to.window(window_name=last_tab)
            
            insertlist = [self.index_number, self.pd_name, self.seller_name] + [self.reg_date, self.iis_ad] + smart_infor
            self.productDF.loc[len(self.productDF)] = insertlist
            
            NvProduct(
            pd_index = insertlist[0],
            keyword = insertlist[1],
            title = insertlist[2],
            price = int(insertlist[3].replace('원','').replace(',','')),
            review_count = int(str(insertlist[4]).replace(',','')),
            reg_date = insertlist[5],
            seller_name = insertlist[6],
            is_ad = insertlist[7],
            serial_number = insertlist[8],
            prod = insertlist[9],
            link = insertlist[10],
            score_avg = insertlist[11],
            image = insertlist[12],
            ).save()

        elif c_type == 2:
            search_infor = self.search()
            
            self.driver.close()
            last_tab = self.driver.window_handles[0]
            self.driver.switch_to.window(window_name=last_tab)

            insertlist = [self.index_number, self.pd_name, self.seller_name] + [self.reg_date, self.iis_ad] + search_infor
            self.productDF.loc[len(self.productDF)] = insertlist
            
            NvProduct(
            pd_index = insertlist[0],
            keyword = insertlist[1],
            title = insertlist[2],
            price = int(insertlist[3].replace('원','').replace(',','')),
            review_count = int(str(insertlist[4]).replace(',','')),
            reg_date = insertlist[5],
            seller_name = insertlist[6],
            is_ad = insertlist[7],
            serial_number = insertlist[8],
            prod = insertlist[9],
            link = insertlist[10],
            score_avg = insertlist[11],
            image = insertlist[12],
            ).save()
            
        else:

            self.driver.close()

            # 팝업 창 닫기 
            if len(self.driver.window_handles) >1:
                last_tab = self.driver.window_handles[1]
                self.driver.switch_to.window(window_name=last_tab)
                self.driver.close()
            last_tab = self.driver.window_handles[0]
            self.driver.switch_to.window(window_name=last_tab)
#======================================================================================================
    def fcrawgo(self):
        len_keyword = len(self.new_list_file) # 총 매칭키워드 수

        for keywords in range(len_keyword): # 총 1229까지 있음
            keyword = self.new_list_file[keywords] # 한개씩 꺼내서 keyword에 담고 검색을 진행함
            print(keyword)
            self.index_number = 0 # 키워드 바뀔때 마다 상품 인덱스번호 초기화
            
            # 검색 창 찾기 - 네이버 기준
            try:
                elem = self.driver.find_element_by_name("query")
            except:
                elem = self.driver.find_element_by_class_name("searchInput_search_input__1Eclz")

            elem.clear()
            # 제품명 변수 지정
            self.pd_name = keyword

            # 찾은 검색 창에 검색 
            elem.send_keys(self.pd_name)
            time.sleep(1)

            # 엔터 
            elem.send_keys(Keys.RETURN)
            time.sleep(3)
        #======================================================================================================
            for i in range(5):
                self.driver.execute_script("window.scrollTo(0, 9000)")
                time.sleep(1)

            #  전체 상품수
            items = int(self.driver.find_element_by_css_selector('#__next > div > div.style_container__1YjHN > div.style_inner__18zZX > div.style_content_wrap__1PzEo > div.style_content__2T20F > div.seller_filter_area > ul > li.active > a > span.subFilter_num__2x0jq').text.replace(',',''))
            print(f'items >> {items}')
            while True:
                self.while_count += 1

                # 현페이지 상품 갯수
                now_page_items = len(self.driver.find_elements_by_css_selector('#__next > div > div.style_container__1YjHN > div.style_inner__18zZX > div.style_content_wrap__1PzEo > div.style_content__2T20F > ul > div > div'))
                print(f'now_page_items >> {now_page_items}')

                for index in range(1, now_page_items + 1): # 요거 다돌면 나가지?
                    self.this_tem_number += 1
                    
                    try:
                        self.iis_ad = self.driver.find_element_by_css_selector('div:nth-child(%d) > li > div > div.basicList_info_area__17Xyo > div.basicList_price_area__1UXXR > button'%self.this_tem_number).text
                    except:
                        self.iis_ad = None

                    now_url = self.driver.find_element_by_css_selector('#__next > div > div.style_container__1YjHN > div.style_inner__18zZX > div.style_content_wrap__1PzEo > div.style_content__2T20F > ul > div > div:nth-child(%d) > li > div > div.basicList_img_area__a3NRA > div > a'%self.this_tem_number).get_attribute('href')
                    
                    self.reg_date = self.driver.find_element_by_xpath('//*[@id="__next"]/div/div[2]/div/div[3]/div[1]/ul/div/div[%d]/li/div/div[2]/div[5]/span[1]'%self.this_tem_number).text.replace('등록일','')
                    print(f'reg_date  >> {self.reg_date }')
                    
                    self.seller_name = self.driver.find_element_by_css_selector('#__next > div > div.style_container__1YjHN > div.style_inner__18zZX > div.style_content_wrap__1PzEo > div.style_content__2T20F > ul > div > div:nth-child(%d) > li > div > div.basicList_mall_area__lIA7R > div > a '%self.this_tem_number).text
                    print(f'self.seller_name >> {self.seller_name}')
                    
                    if self.iis_ad !='광고':
                        self.index_number += 1 # 끊어지지 않고 들어갈 인덱스넘버
                        if now_url in self.new_list_url:
                            print('♥♥♥♥♥본사왔어요?♥♥♥♥♥')
                            self.in_crawling()
                        else:
                            if self.othercheck <= 3:
                                self.othercheck += 1
                                self.in_crawling()
                            else:
                                pass
                                print('타사제품 읎다네')

                                time.sleep(1.5)
 
                pageing = round(items / now_page_items )
#                 print(f'pageing >> {pageing}')
                if self.while_count == pageing:
                    self.this_tem_number = 0 # 상품 태그번호 초기화
                    self.othercheck = 1 # 타사체크 초기화
                    self.while_count = 0 # while_count 초기화
                    break

                try:
                    next_item_button = self.driver.find_element_by_css_selector('#__next > div > div.style_container__1YjHN > div.style_inner__18zZX > div.style_content_wrap__1PzEo > div.style_content__2T20F > div.pagination_pagination__6AcG4 > a.pagination_next__1ITTf')
                    next_item_button.send_keys(Keys.RETURN)
                    self.this_tem_number = 0
                    time.sleep(1.5)

                except:
                    self.this_tem_number = 0
                    self.othercheck = 1
                    break 