import time
import pymysql
import datetime as dt

def get_time():
    time_str = time.strftime("%Y{}%m{}%d-%X")
    return time_str.format("年","月","日")

def get_conn():
    conn = pymysql.connect(host= 'localhost',user = 'root',password='00000', port= 3306,charset='utf8mb4',database='Cov_data')
    cursor = conn.cursor()
    return conn,cursor

def close_connect(conn,cursor):
    conn.close()
    cursor.close()

def query(sql,*args):
    conn,cursor = get_conn()
    cursor.execute(sql,args)
    res = cursor.fetchall()
    close_connect(conn,cursor)
    return res

def get_total_data_of_china():
    sql = "select sum(currentConfirmedCount),sum(suspectedCount),sum(curedCount),sum(deadCount) from last_day_corona_virus_of_china;"
    res = query(sql)
    return res[0]


def get_china_map_data():
    sql = "select provinceShortName ,currentConfirmedCount from last_day_corona_virus_of_china;"
    res = query(sql)
    return res

def get_wordcloud_data():
    sql = "select id,content from hotSearch_data limit 20;"
    res = query(sql)
    return res

def get_top10_data():
    sql = "select provinceShortName,currentConfirmedCount from last_day_corona_virus_of_china where provinceShortName not in ('台湾','香港') order by currentConfirmedCount desc limit 10;"
    res = query(sql)
    return res

def get_cov_trend_data():
    current_date = int(time.strftime('%Y%m') + '01')
    date = 20220101
    res = []
    while(date <= current_date):
        sql = f"select sum(confirmedCount),sum(currentConfirmedCount),sum(suspectedCount),sum(curedCount),sum(deadCount) from corona_virus_of_china where dateId = {date} and provinceId not in (select provinceId from provinceName_china where provinceShortName in('台湾','香港'));"
        onedayInfr = [query(sql),date]
        res.append(onedayInfr)
        date += 100
    return res

def get_cov_trend_cq_data():
    sql = f"select dateId,confirmedIncr,currentConfirmedIncr,suspectedCountIncr,curedIncr,deadIncr from corona_virus_of_china where provinceId = (select provinceId from provinceName_china where provinceShortName = '重庆') order by dateId desc limit 7;"
    res = query(sql)
    return res

def get_cov_msg_data():
    sql = 'select content from covMsg_data'
    return query(sql)

def get_covIncr_cq_data():
    sql = 'select cityName,localIncr,asymptomaticIncr,dangerArea from covIncr_cq_data order by localIncr desc limit 5;'
    res = query(sql)
    return res

if __name__=='__main__':
    #print(get_total_data_of_china())
    #print(get_china_map_data())
    #print(get_top10_data())
#    print(get_cov_trend_data()[0][0][0][1])
#    print(get_cov_trend_of_cq_data()[0])
    print(get_covIncr_cq_data())
