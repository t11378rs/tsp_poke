# -*- coding: utf-8 -*-

import psycopg2

#array dealing with stations
places = [
	"東京", "品川", "大崎", "渋谷", "高田馬場",
	"池袋", "四ツ谷", "日暮里", "秋葉原", "浜松町",
	"赤羽", "北千住", "松戸", "柏", "蒲田",
	"横浜", "藤沢", "武蔵小杉", "武蔵浦和", "大宮",
	"浦和", "八王子", "立川", "吉祥寺", "千葉", 
	"津田沼", "南船橋", "熊谷", "土浦", "羽田空港第2ビル"
]
indexs = range(len(places))


#connect db
conn = psycopg2.connect(dbname="postgres", host="localhost", port=5432, user="postgres", password="postgres")
cur = conn.cursor()

def executeSQL(sql):
	print sql
	cur.execute(sql)
	fetches = cur.fetchall()
	for fetch in fetches:
		for element in fetch:
			elem = str(element)
			print elem,
		print ""

def commitDB():
	conn.commit()
	print "commit!"
	

if __name__ == '__main__':
	sql = "select * from transfer_data where dep_sta = '八王子' and arr_sta = '武蔵浦和';"
	executeSQL(sql)
	cur.close()
	conn.close()