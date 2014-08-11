# -*- coding: utf-8 -*-

import urllib
import BeautifulSoup
import re
import random
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
'''
places = [
	"tokyo", "shinagawa", "oosaki", "shibuya", "takadanobaba",
	"ikebukuro", "yotsuya", "nippori", "akihabara", "hamamatsuchou",
	"akabane", "kitasenju", "matsudo", "kashiwa", "kamata",
	"yokohama", "fujisawa", "musashikosugi", "musashiurawa", "oomiya",
	"urawa", "hachiouji", "tachikawa", "kichijouji", "chiba", 
	"tsudanuma", "minamifunabashi", "kumagaya", "tsuchiura", "hanedakuukoudai2biru"
]
'''
indexs = range(len(places))

#pettern
time_pattern = u"(\d+):(\d+)[\w+]"

#connect db
conn = psycopg2.connect(dbname="postgres", host="localhost", port=5432, user="postgres", password="postgres")
cur = conn.cursor()

def main():
	for time_slot in range(9,17): #9~16
		print "time_slot: %(time_slot)d" % locals()
		for dep in range(len(places)):
			print "From: %s" % (places[dep])
			for arr in range(len(places)):
				if dep != arr:
					url = "http://transit.loco.yahoo.co.jp/search/result?flatlon=&from=%s&tlatlon=&to=%s&via=%s&via=%s&via=%s&ym=201408&d=05&hh=%s&m2=0&m1=0&type=1&ticket=ic&al=1&shin=1&ex=1&hb=1&lb=1&sr=1&s=0&expkind=1&ws=2&kw=%s" % (places[dep], places[arr], "", "", "", str(time_slot).zfill(2), places[arr])
					html = urllib.urlopen(url).read()
					soup = BeautifulSoup.BeautifulSoup(html)
					print soup.find("span", attrs={"class": "route-departure"})
					print soup.find("span", attrs={"class": "route-arrive-on"})
					raw_dep_time = soup.find("span", attrs={"class": "route-departure"}).string
					raw_arr_time = soup.find("span", attrs={"class": "route-arrive-on"}).string
					match_dep = re.match(time_pattern, raw_dep_time, re.U)
					match_arr = re.match(time_pattern, raw_arr_time, re.U)
					time = calcTime(int(match_dep.group(1)), int(match_dep.group(2)), int(match_arr.group(1)), int(match_arr.group(2)))
					#print "所要時間： %(time)d\t" % locals(),
					#print "%s - %s" % (places[dep], places[arr])
					insertDeta(places[dep], places[arr], time, time_slot)
				else:
					pass
	print ""
	commitDB()

def calcTime(dep_h, dep_m, arr_h, arr_m):
 	dep_by_min = dep_h * 60 + dep_m
 	arr_by_min = arr_h * 60 + arr_m
 	if dep_by_min > arr_by_min:
 		arr_by_min += 24*60
 	return arr_by_min - dep_by_min

def resetAndMakeTable():
	print "resetAndMakeTable()"
	sql = "DROP TABLE transfer_data;"
	executeSQL(sql)
	sql = "CREATE TABLE transfer_data (dep_sta text, arr_sta text, time integer, time_slot integer);"
	executeSQL(sql)

def insertDeta(dep, arr, t, ts):
	sql = "INSERT INTO transfer_data (dep_sta, arr_sta, time, time_slot) VALUES (\'%(dep)s\', \'%(arr)s\', %(t)d, %(ts)d);" % locals()
	executeSQL(sql)

def executeSQL(sql):
	print sql
	cur.execute(sql)

def commitDB():
	conn.commit()
	print "commit!"
	

if __name__ == '__main__':
	resetAndMakeTable()
	main()
	cur.close()
	conn.close()
