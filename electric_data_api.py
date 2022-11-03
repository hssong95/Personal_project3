import requests
import json
import os
import sqlite3
# 2007.1 ~ 2022.8


API_KEY = 'fk5c936Rh31iz1G42vUaX8SWFdSEt61U2A9yH1hV'
DB_NAME = 'Electricity.db'
DB_PATH = os.path.join(os.getcwd(),DB_NAME)
# year='2020'
# month='11'
# bizcode='C'
# api_url=f'https://bigdata.kepco.co.kr/openapi/v1/powerUsage/industryType.do?year=2022&month=08&bizCd=C&apiKey={API_KEY}&returnType=json'
# # f'https://bigdata.kepco.co.kr/openapi/v1/powerUsage/industryType.do?year={year}&month={month}&apiKey={API_KEY}&bizCd={bizcode}&returnType=json'
# raw_data=requests.get(api_url)
# text_data=raw_data.text
# data_split=text_data.split('}{')
# data_split[0]=data_split[0]+'}'
# data_split[1]='{'+data_split[1]
# data=data_split
# total_data=json.loads(data[0])
# main_data=json.loads(data[1])
# # print(total_data['totData'])
# print(main_data['data'][-1])

def get_data(year,month,API_KEY=API_KEY):
    api_url=f'https://bigdata.kepco.co.kr/openapi/v1/powerUsage/industryType.do?year={year}&month={month}&apiKey={API_KEY}&returnType=json'
    response=requests.get(api_url)
    text_data=response.text
    data_split=text_data.split('}{')
    data_split[0]=data_split[0]+'}'
    data_split[1]='{'+data_split[1]
    data=data_split
    total_data=json.loads(data[0])
    main_data=json.loads(data[1])
    main_data=main_data['data']
    total_data=total_data['totData']
    
    return total_data, main_data


def connect_to_db(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    return conn, cur


conn, cur = connect_to_db(DB_PATH)
cur.execute("""CREATE TABLE main_data(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
year INTEGER,
month INTEGER,
metro VARCHAR,
city VARCHAR,
biz VARCHAR,
custCnt INTEGER,
powerUsage INTEGER,
bill INTEGER,
unitCost FLOAT);""")

cur.execute("""CREATE TABLE total_data(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
year INTEGER,
month INTEGER,
metro VARCHAR,
city VARCHAR,
biz VARCHAR,
custCnt INTEGER,
powerUsage INTEGER,
bill INTEGER,
unitCost FLOAT);""")

for y in range(2007,2023):
    if y == 2022:
        for m in range(1,9):
            y=str(y)
            m='0'+str(m)
            total_data, main_data=get_data(year=y,month=m)
            for i in main_data:
                cur.execute("INSERT INTO main_data (year,month,metro,city,biz,custCnt,powerUsage,bill,unitCost) VALUES(?,?,?,?,?,?,?,?,?);",list(i.values()))
            for l in total_data:
                cur.execute("INSERT INTO total_data (year,month,metro,city,biz,custCnt,powerUsage,bill,unitCost) VALUES(?,?,?,?,?,?,?,?,?);",list(l.values()))
    else:
        for m in range(1,13):
            y=str(y)
            if (m != 10)&(m != 11)&(m != 12):
                m='0'+str(m)
            else:
                m=str(m)
            total_data, main_data=get_data(year=y,month=m)
            for i in main_data:
                cur.execute("INSERT INTO main_data (year,month,metro,city,biz,custCnt,powerUsage,bill,unitCost) VALUES(?,?,?,?,?,?,?,?,?);",list(i.values()))
            for l in total_data:
                cur.execute("INSERT INTO total_data (year,month,metro,city,biz,custCnt,powerUsage,bill,unitCost) VALUES(?,?,?,?,?,?,?,?,?);",list(l.values()))

conn.commit()
conn.close()