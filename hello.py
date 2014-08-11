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

#route = ["品川","大崎","横浜","池袋","浜松"]

tmp_best = ["東京","秋葉原","四ツ谷","渋谷","大崎",
	"品川","浜松町","蒲田","横浜","武蔵小杉",
	"池袋","高田馬場","赤羽","浦和","大宮"
	"武蔵浦和","日暮里","北千住","松戸","柏",
	"南船橋","津田沼","千葉","吉祥寺","立川",
	"八王子","藤沢"]

pettern = re.compile(r"(\d+)時間(\d+)分（乗車(\d+)時間(\d+)分、ほか(\d+)分）")

def main():
	time = 0
	random.shuffle(indexs)
	#route = []
	#for i in range(len(places)):
	#	route.append(places[indexs[i]])
	#	print "%s-" %(places[indexs[i]]),
	#	#route = [places[indexs[0]], places[indexs[1]], places[indexs[2]], places[indexs[3]], places[indexs[4]]]
	#print ""

	for i in range(len(tmp_best)):
		route.append(tmp_best[i])
		print "%s-" %(tmp_best[i]),
		#route = [places[indexs[0]], places[indexs[1]], places[indexs[2]], places[indexs[3]], places[indexs[4]]]
	print ""	

	count = 0
	while count < range(len(route)-2):
		#print count
		url = "http://transit.loco.yahoo.co.jp/search/result?flatlon=&from=%s&tlatlon=&to=%s&via=%s&via=%s&via=%s&ym=201407&d=31&hh=14&m2=4&m1=5&type=1&ticket=ic&al=1&shin=1&ex=1&hb=1&lb=1&sr=1&s=0&expkind=1&ws=2&kw=%s" % (route[count],route[count+4],route[count+1],route[count+2],route[count+3],route[count+4])
		print url
		html = urllib.urlopen(url).read()
		soup = BeautifulSoup.BeautifulSoup(html)
		# 基本はfindかfindAllでタグ名指定で要素を取得
		str_time = soup.find("dl", attrs={"class": "time"}).findAll('dd')
		iterator = pettern.finditer(str(str_time))
		for match in iterator:
			total_h = int(match.groups()[0])
			total_m = int(match.groups()[1])
			#ride_h = int(match.groups()[2])
			#ride_m = int(match.groups()[3])
			#other_m = int(match.groups()[4])
		time += total_h*60 + total_m
		print "%s - %s - %s - %s - %s" % (route[count], route[count+1], route[count+2], route[count+3], route[count+4])
		print "所要時間： %(time)d" % locals()
		count+=4

	url = "http://transit.loco.yahoo.co.jp/search/result?flatlon=&from=%s&tlatlon=&to=%s&via=%s&via=%s&via=%s&ym=201407&d=31&hh=14&m2=4&m1=5&type=1&ticket=ic&al=1&shin=1&ex=1&hb=1&lb=1&sr=1&s=0&expkind=1&ws=2&kw=%s" % (route[28],route[29],"","","",route[29])
	html = urllib.urlopen(url).read()
	soup = BeautifulSoup.BeautifulSoup(html)
	# 基本はfindかfindAllでタグ名指定で要素を取得
	str_time = soup.find("dl", attrs={"class": "time"}).findAll('dd')
	iterator = pettern.finditer(str(str_time))
	for match in iterator:
		time += int(match.groups()[0])*60 + int(match.groups()[1])
		#ride_h = int(match.groups()[2])
		#ride_m = int(match.groups()[3])
		#other_m = int(match.groups()[4])
	print "%s - %s" % (route[28], route[29])
	print "所要時間： %(time)d" % locals()

	print time

if __name__ == '__main__':
	main()