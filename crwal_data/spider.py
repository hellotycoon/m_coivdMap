import requests
from bs4 import  BeautifulSoup
import re
import json
from tqdm import tqdm
import pymysql
import time
from  selenium.webdriver import Chrome,ChromeOptions
import pymysql

class CoronaVirusSpider(object):
    def __init__(self):
        self.home_url = 'https://ncov.dxy.cn/ncovh5/view/pneumonia'
    def get_content_from_url(self,url):
        response = requests.get(url)
        home_page = response.content.decode()
        return home_page
    def parse_home_page(self,home_page,tag_Id):
        soup = BeautifulSoup(home_page,'lxml')
        script = soup.find(id = tag_Id)
        text = script.text
        json_str = re.findall(r'\[.+\]',text)[0]
        data = json.loads(json_str)
        return data
    def save(self,data,path):
        with open(path,'w',encoding='utf-8') as fp:
            json.dump(data,fp,ensure_ascii=False)
    def load(self,path):
        with open(path,'r',encoding='utf-8') as fp:
            data = json.load(fp)
            return data
    def mysql_init(self,init_table_sql,tablename):
        conn = pymysql.connect(host='localhost',port=3306,user='root',password='00000',charset='utf8mb4',database='Cov_data')
        cursor = conn.cursor()
        cursor.execute(init_table_sql)
        cursor.execute('truncate table %s;' % tablename)
        return conn,cursor
    def mysql_close(self,conn,cursor):
        conn.commit()
        cursor.close()
        conn.close()
    def save_to_mysql(self,corona_virus_data,init_table_sql,tablename,region):
        conn,cursor = self.mysql_init(init_table_sql,tablename)
        if(region == 'world'):
            sql = f'insert into {tablename} values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
            for country in corona_virus_data:
                data = (country['provinceName'],country['countryFullName'],country['currentConfirmedCount'],country['confirmedCount'],country['curedCount'],country['deadCount'],country['deadRate'],country['incrVo']['currentConfirmedIncr'],country['incrVo']['confirmedIncr'],country['incrVo']['deadIncr'])
                cursor.execute(sql,data)
        elif(region == 'china'):
            sql = f'insert into {tablename} values(%s,%s,%s,%s,%s,%s,%s)'
            for country in corona_virus_data:
                data = (country['provinceName'],country['provinceShortName'],country['currentConfirmedCount'],country['confirmedCount'],country['suspectedCount'],country['curedCount'],country['deadCount'])
                cursor.execute(sql,data)
        self.mysql_close(conn,cursor)

    def crawl_last_day_corona_virus(self): #???????????????????????????????????????
        home_page = self.get_content_from_url(self.home_url)
        last_day_corona_virus = self.parse_home_page(home_page,'getListByCountryTypeService2true')
        self.save(last_day_corona_virus,'/srv/test/crwal_data/data/last_day_corona_virus.json')
        sql = 'create table if not exists last_day_corona_virus(provinceName  varchar(255) primary key, countryFullName varchar(255),currentConfirmedCount int,confirmedCount int,curedCount int,deadCount int ,deadRate int, currentConfirmedIncr int,confirmedIncr int,deadIncr int);'
        self.save_to_mysql(last_day_corona_virus,sql,'last_day_corona_virus','world')

    def crawl_last_day_corona_virus_of_china(self): #crawl the last day corona virus data of china
        home_page = self.get_content_from_url(self.home_url)
        last_day_corona_virus_of_china = self.parse_home_page(home_page,'getAreaStat')
        self.save(last_day_corona_virus_of_china, '/srv/test/crwal_data/data/last_day_corona_virus_of_china.json')
        sql = 'create table if not exists last_day_corona_virus_of_china(provinceName  varchar(255) primary key, provinceShortName varchar(255) ,currentConfirmedCount int,confirmedCount int,suspectedCount int,curedCount int,deadCount int) ;'
        self.save_to_mysql(last_day_corona_virus_of_china,sql,'last_day_corona_virus_of_china','china')

    def crawl_corona_virus(self):# ??????????????????????????????
     # 1. ????????????????????????
    # 2. ????????????????????????,???????????????URL
    #3. ????????????,????????????json??????
    # 4. ???json???????????????python???????????????,??????????????????
    # 5. ????????????json?????????????????????
        last_day_corona_virus = self.load('/srv/test/crwal_data/data/last_day_corona_virus.json')
         # ????????????,???????????????????????????????????????
        init_sql = 'create table if not exists countryName_world (countryId int primary key,countryName varchar(255),countryFullName varchar(255));'
        conn1,cursor1 = self.mysql_init(init_sql,'countryName_world')
        init_sql = 'create table if not exists corona_virus_data(countryId int,confirmedCount int,confirmedIncr int,curedCount int,curedIncr int,currentConfirmedCount int,currentConfirmedIncr int,dateId date,deadCount int,deadIncr int,highDangerCount int, midDangerCount int,suspectedCount int,suspectedCountIncr int,primary key(countryId,dateId));'
        conn2,cursor2 = self.mysql_init(init_sql, 'corona_virus_data')
        covData_sql = 'insert into corona_virus_data values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
        conName_sql = 'insert into countryName_world  values(%s,%s,%s);'
        countryId = 0
        for country in tqdm(last_day_corona_virus,"??????2022???1???1?????????????????????????????????"):
            if(country['countryFullName'] == 'China'): #china has no id
                countryId = 999999999
            else:
                countryId = country['id']
            countryInfor = (countryId,country['provinceName'],country['countryFullName'])
            cursor1.execute(conName_sql,countryInfor)
            statistics_data_url = country['statisticsData']
            statistics_data_json_str = self.get_content_from_url(statistics_data_url)
            statistics_data = json.loads(statistics_data_json_str)['data']
            count = len(statistics_data)
            i = 0
            while(i < count):
                if(str(statistics_data[i]['dateId']) == '20220101'):
                    break
                i += 1
            while (i < count):
                covData = [countryId]
                for key in statistics_data[i]:
                    covData.append(statistics_data[i][key])
                cursor2.execute(covData_sql,tuple(covData))
                i += 1
        self.mysql_close(conn1,cursor1)
        self.mysql_close(conn2,cursor2)
    def crawl_corona_virus_of_china(self):# ????????????????????????????????????
    # 1. ????????????????????????
    # 2. ????????????????????????,???????????????URL
    #3. ????????????,????????????json??????
    # 4. ???json???????????????python???????????????,??????????????????
    # 5. ????????????json?????????????????????
        last_day_corona_virus_of_china = self.load('/srv/test/crwal_data/data/last_day_corona_virus_of_china.json')
        init_sql = 'create table if not exists provinceName_china (provinceId int primary key,provinceName varchar(255),provinceShortName varchar(255));'
        conn1,cursor1 = self.mysql_init(init_sql,'provinceName_china')
        init_sql = 'create table if not exists corona_virus_of_china(provinceId int,confirmedCount int,confirmedIncr int,curedCount int,curedIncr int,currentConfirmedCount int,currentConfirmedIncr int,dateId date,deadCount int,deadIncr int,highDangerCount int, midDangerCount int,suspectedCount int,suspectedCountIncr int,primary key(provinceId,dateId));'
        conn2,cursor2 = self.mysql_init(init_sql, 'corona_virus_of_china')
        covData_sql = 'insert into corona_virus_of_china values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
        proName_sql = 'insert into provinceName_china  values(%s,%s,%s);'
        for province in tqdm(last_day_corona_virus_of_china,"??????2022???1???1?????????????????????????????????"):
            statistics_data_url = province['statisticsData']
            provinceInfor = (province['locationId'],province['provinceName'],province['provinceShortName'])
            cursor1.execute(proName_sql,provinceInfor)
            statistics_data_json_str = self.get_content_from_url(statistics_data_url)
            statistics_data = json.loads(statistics_data_json_str)['data']
            count = len(statistics_data)
            i = 0
            while(i < count):
                if(str(statistics_data[i]['dateId']) == '20220101'):
                    break;
                i += 1
            while (i < count):
                covData = [province['locationId']]
                for key in statistics_data[i]:
                    covData.append(statistics_data[i][key])
                cursor2.execute(covData_sql,tuple(covData))
                i += 1
        self.mysql_close(conn1,cursor1)
        self.mysql_close(conn2,cursor2)
    def run(self):
        self.crawl_last_day_corona_virus()
        self.crawl_last_day_corona_virus_of_china()
        self.crawl_corona_virus()
        self.crawl_corona_virus_of_china()

class Hotsearchspider(object):
    def __init__(self):
        self.baidu_Hotsearch_url = 'https://top.baidu.com/board?tab=realtime'
        self.baidu_Hotsearch_xpath = '//*[@id="sanRoot"]/main/div[2]/div/div[2]/div/div[2]/a/div[1]'
        self.dx_url = 'https://ncov.dxy.cn/ncovh5/view/pneumonia'
        self.covMsg_xpath = '//*[@id="root"]/div/div[2]/div[2]/div/div[1]/div[1]/div[1]/span'
        self.covIncr_cq_xpath = '//*[@id="root"]/div/div[3]/div[5]/div[3]/div[6]/div/p'
    def mysql_init(self,init_table_sql,tablename):
        conn = pymysql.connect(host='localhost',port=3306,user='root',password='00000',charset='utf8mb4',database='Cov_data')
        cursor = conn.cursor()
        cursor.execute(init_table_sql)
        cursor.execute('truncate table %s;' % tablename)
        return conn,cursor
    def mysql_close(self,conn,cursor):
        cursor.close()
        conn.close()
    def get_browser_data(self,url,xpath):
        option = ChromeOptions()
        option.add_argument('--headless')
        option.add_argument('--no-sandbox')
        browser = Chrome(options=option)
        browser.get(url)
        elements = browser.find_elements(by='xpath',value = xpath)
        content = [element.text for element in elements]
        return content
    def get_covIncr_cq_data(self,url,xpath): #???????????????????????????????????????????????????,????????????get_attribute("innerText")????????????
        option = ChromeOptions()
        option.add_argument('--headless')
        option.add_argument('--no-sandbox')
        browser = Chrome(options=option)
        browser.get(url)
        elements = browser.find_elements(by='xpath',value = xpath)
        content = [element.get_attribute("innerText").replace(",",'') for element in elements] #??????????????????????????????,?????????????????????????????????,??????1,028,?????????????????????
        return content

    def update_browser_data(self):
        init_hotSearch_sql = 'create table if not exists hotSearch_data(id int auto_increment,date_time date,content varchar(255), primary key(id))'
        init_covMsg_sql = 'create table if not exists covMsg_data(id int auto_increment,date_time date,content varchar(255), primary key(id))'
        init_covIncr_cq_sql = "create table if not exists covIncr_cq_data(cityName varchar(255) primary key, date_time date, localIncr int,asymptomaticIncr  int,dangerArea int)"
        conn1,cursor1 = self.mysql_init(init_hotSearch_sql,'hotSearch_data')
        conn2,cursor2 = self.mysql_init(init_covMsg_sql,'covMsg_data')
        conn3,cursor3 = self.mysql_init(init_covIncr_cq_sql,'covIncr_cq_data')
        current_date = time.strftime('%Y-%m-%d')
        try:
            content = self.get_browser_data(self.baidu_Hotsearch_url,self.baidu_Hotsearch_xpath)
            sql = 'insert into hotSearch_data(date_time,content) values(%s,%s)'
            for element in content:
                cursor1.execute(sql,(current_date,element))
            conn1.commit()
        except:
            print("??????????????????????????????")
        try:
            content = self.get_browser_data(self.dx_url,self.covMsg_xpath)
            sql = 'insert into covMsg_data(date_time,content) values(%s,%s)'
            for element in content:
                cursor2.execute(sql,(current_date,element))
            conn2.commit()
        except:
            print("??????????????????????????????")
        try:
            content = self.get_covIncr_cq_data(self.dx_url,self.covIncr_cq_xpath)
            sql = 'insert into covIncr_cq_data(cityName,date_time,localIncr,asymptomaticIncr,dangerArea) values(%s, %s, %s, %s,%s)'
            i = 6
            while(i < len(content)):
                cursor3.execute(sql,(content[i],current_date,content[i+1],content[i+2],content[i+4]))
                i += 6 
            conn3.commit()
        except:
            print("??????????????????????????????")
        self.mysql_close(conn1,cursor1)
        self.mysql_close(conn2,cursor2)
        self.mysql_close(conn3,cursor3)

if __name__ == '__main__':
    Cov_spider = CoronaVirusSpider()
    Cov_spider.run()
    Hotsearch_spider = Hotsearchspider()
    Hotsearch_spider.update_browser_data()
