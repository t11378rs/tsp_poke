# -*- coding: utf-8 -*-

import urllib
import BeautifulSoup
import re
import random

places = [
	"東京", "品川", "大崎", "渋谷", "高田馬場",
	"池袋", "四ツ谷", "日暮里", "秋葉原", "浜松町",
	"赤羽", "北千住", "松戸", "柏", "蒲田",
	"横浜", "藤沢", "武蔵小杉", "武蔵浦和", "大宮",
	"浦和", "八王子", "立川", "吉祥寺", "千葉", 
	"津田沼", "南船橋", "熊谷", "土浦", "羽田空港第2ビル"
]

indexs = range(len(places))

#route = ["東京","秋葉原","四ツ谷","渋谷","大崎",
#	"品川","浜松町","蒲田","横浜","武蔵小杉",
#	"池袋","高田馬場","赤羽","浦和","大宮",
#	"武蔵浦和","日暮里","北千住","松戸","柏",
#	"南船橋","津田沼","千葉","吉祥寺","立川",
#	"八王子","藤沢"]

route = [
	"吉祥寺", "立川", "八王子", "高田馬場", "池袋",
	"赤羽", "浦和", "大宮", "武蔵浦和", "渋谷",
	"大崎", "品川", "浜松町", "東京", "秋葉原",
	"四ツ谷", "日暮里", "北千住", "松戸", "柏",
	"南船橋", "津田沼", "千葉", "武蔵小杉", "横浜",
	"蒲田", "羽田空港第2ビル"
]

time_pattern = u"(\d+):(\d+)[\w+]"

TIME_LOSS = 5

def printClock(min):
	h = int(min/60)
	m = min - h*60
	h_str = str(h).zfill(2)
	m_str = str(m).zfill(2)
	print "%s:%s" % (h_str, m_str)

def printRoute(rt):
	for p in rt:
		print "%s -" % (p),
	print "(%d stations)" % (len(rt))

def calcTime(dep_h, dep_m, arr_h, arr_m):
 	dep_by_min = dep_h * 60 + dep_m
 	arr_by_min = arr_h * 60 + arr_m
 	if dep_by_min > arr_by_min:
 		arr_by_min += 24*60
 	return arr_by_min - dep_by_min

def main():
	clock = 9*60 + 30

	printRoute(route)

	for count in range(len(route)-1):
		dep = route[count]
		arr = route[count+1]
		hour = int(clock/60)
		minuite = clock - hour*60
		min_one = minuite % 10
		min_ten = (minuite - min_one) / 10
		url = "http://transit.loco.yahoo.co.jp/search/result?flatlon=&from=%s&tlatlon=&to=%s&via=&via=&via=&ym=201408&d=05&hh=%s&m2=%d&m1=%d&type=1&ticket=ic&al=1&shin=1&ex=1&hb=1&lb=1&sr=1&s=0&expkind=1&ws=2&kw=%s" % (dep, arr, hour, min_one, min_ten, arr)		
		print url

		html = urllib.urlopen(url).read()
		soup = BeautifulSoup.BeautifulSoup(html)
		#print soup.find("span", attrs={"class": "route-departure"})
		#print soup.find("span", attrs={"class": "route-arrive-on"})
		raw_dep_time = soup.find("span", attrs={"class": "route-departure"}).string
		raw_arr_time = soup.find("span", attrs={"class": "route-arrive-on"}).string
		match_dep = re.match(time_pattern, raw_dep_time, re.U)
		match_arr = re.match(time_pattern, raw_arr_time, re.U)
		time = calcTime(int(match_dep.group(1)), int(match_dep.group(2)), int(match_arr.group(1)), int(match_arr.group(2)))
		clock += time
		clock += TIME_LOSS
		print "from %s  to %s" % (dep, arr)
		printClock(clock)

if __name__ == '__main__':
	main()