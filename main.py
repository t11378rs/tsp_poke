# -*- coding: utf-8 -*-

import urllib
import BeautifulSoup
import re
import random
import psycopg2

TIME_LIMIT = 7 * 60 + 30

#array dealing with stations
places = [
	"東京", "品川", "大崎", "渋谷", "高田馬場",
	"池袋", "四ツ谷", "日暮里", "秋葉原", "浜松町",
	"赤羽", "北千住", "松戸", "柏", "蒲田",
	"横浜", "藤沢", "武蔵小杉", "武蔵浦和", "大宮",
	"浦和", "八王子", "立川", "吉祥寺", "千葉", 
	"津田沼", "南船橋", "熊谷", "土浦", "羽田空港第2ビル"
]

time_slot = [9,10,11,12,13,14,15,16]
TS = 4
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

#susa_route = [
# "羽田空港第2ビル", "浜松町", "東京", "秋葉原", "日暮里", "北千住  松戸", "柏", "南船橋", "津田沼", "千葉", "高田馬場", "池袋", "赤羽", "浦和", "武蔵浦和", "大宮", "熊谷", "蒲田", "品川", "大崎", "武蔵小杉", "横浜", "藤沢", "渋谷", "四ツ谷", "吉祥寺", "立川", "八王子", "土浦"
#]

indexs = range(len(places))

db_matrix = [[[None for ts in range(len(time_slot))] for a in range(len(places))]for d in range(len(places))]

#connect db
conn = psycopg2.connect(dbname="postgres", host="localhost", port=5432, user="postgres", password="postgres")
cur = conn.cursor()

#def calcRoute(rt):
#	time=0
#	for point in range(len(rt)):
#		station_index = places.find(susa_route)



def printCulumn(fs):
	for fetch in fs:
		for element in fetch:
			elem = str(element)
			print elem,
		print ""

def printMatrix(mx):
	for i, d in enumerate(mx):
		for j, a in enumerate(d):
			for k, t in enumerate(a):
				print "%4d min  (FROM %s TO %s WHEN %d O\'CLOCK)" % (t, places[i], places[j], time_slot[k])

def printRoute(rt):
	for p in rt:
		print "%s -" % (places[p]),
	print "(%d stations)" % (len(rt))

def printMinToTime(m):
	hour = int(m / 60)
	minuite = (m - hour * 60)
	print "%s:%s"%(str(hour).zfill(2), str(minuite).zfill(2))

def executeSQL(sql):
	print sql
	cur.execute(sql)

def prepareData():
	sql = "select * from transfer_data"
	cur.execute(sql)
	#fetches = cur.fetchall()
	#print fetches[0]
	for t in range(len(time_slot)):
		for d in range(len(places)):
			for a in range(len(places)):
				if d != a:
					#print "%d %d %d" %(d,a,t)
					sql = "SELECT * FROM transfer_data WHERE dep_sta = \'%s\' AND arr_sta = \'%s\' AND time_slot = \'%s\'" % (places[d], places[a], str(time_slot[t]))
					executeSQL(sql)
					db_matrix[d][a][t] = cur.fetchone()[2]
				else:
					db_matrix[d][a][t] = 9999
	printMatrix(db_matrix)
	#printCulumn(fetches)

def findShortestRoute(dep, rest):
	shortest = 99999
	shortest_index = -1
	for arr in rest:
		if(db_matrix[dep][arr][4]<shortest):
			shortest = db_matrix[dep][arr][4]
			shortest_index = arr
	#new_rest = rest.pop(arr)
	return shortest_index, shortest

def routeByCheatedGreedy():
	#高田馬場、吉祥寺だけfix
	time = 0
	next = 4 #places.find("高田馬場")
	rest = list(indexs)
	rt = []
	rt.append(next) #最初だけ別に
	rest.remove(next) #最初だけべつに
	for i in range(len(places)-1):
		if next !=4:#places.find("高田馬場")
			next, t = findShortestRoute(next, rest)
		else:
			kichijouji = 23 #places.find("吉祥寺")
			t = db_matrix[next][kichijouji][4]
			next = kichijouji
		if time+t <= TIME_LIMIT:
			time += t
			rt.append(next)
			rest.remove(next)
		else:
			break
	return rt, time

#貪欲法
def routeByGreedy():
	routes = []
	times = []
	for j in range(len(places)):
		time = 0
		next = j
		rest = list(indexs)
		rt = []
		rt.append(next) #最初だけ別に
		rest.remove(next) #最初だけべつに
		for i in range(len(places)-1):
			next, t = findShortestRoute(next, rest)
			if time+t <= TIME_LIMIT:
				time += t
				rt.append(next)
				rest.remove(next)
			else:
				routes.append(rt)
				times.append(time)
				break
	best_route_index = -1
	best_score_time = 9999
	best_route = []
	for i in range(len(routes)):
		if len(best_route)<=len(routes[i]):
			if best_score_time > times[i]:
				best_route_index = i
				best_score_time = times[i]
			else:
				pass
		else:
			pass
	return routes[best_route_index], times[best_route_index]

#ランダム
def routeByRandom():
	last_index = -1
	time = 0
	rt = list(indexs)
	random.shuffle(rt)
	for i in range(len(rt)-1):
		t = db_matrix[rt[i]][rt[i+1]][4]
		if time+t <= TIME_LIMIT:
			time += t
		else:
			last_index = i
			break
	if last_index != -1:
		rt = list(rt[:last_index])
	return rt, time

#ちゃんとリミットもうける総当り
def routeBySmart():
	rest = list(indexs)
	next = 0
	rt = []
	rt.append(next) #最初だけ別に
	rest.remove(next) #最初だけべつに

	branchAndBound(rt[-1], rest, rt, 0)
	return best_route, best_score_time

def branchAndBound(dep_index, my_rest, my_route, current_time):
	global best_score
	global best_route
	global best_score_time

	if current_time < TIME_LIMIT:
		if not my_rest:#my_restが空
			print "Collection completed"
			print my_route
			score = len(my_route)
			if best_score < score:
				best_route = my_route
				best_score = score
				best_score_time = current_time
				print "NEW SCORE!!!"
				print best_score
				print best_route
				print best_score_time

			elif best_score == score:
				if best_score_time > current_time:
					best_route = my_route
					best_score_time = current_time
					print "NEW TIME!"
					print best_score
					print best_route
					print best_score_time
				else:
					#print "processing..."
					pass
			else:
				#print "processing..."
				pass
		else:#中身がまだあったら、繰り返す
			for arr_index in my_rest:
				tmp_rest = list(my_rest)
				tmp_route = list(my_route)
				tmp_rest.remove(arr_index)
				latest_time = current_time + db_matrix[dep_index][arr_index][TS]
				tmp_route.append(arr_index)
				branchAndBound(arr_index, tmp_rest, tmp_route, latest_time)
	else: 
		#print "time over"
		print my_route
		score = len(my_route)
		if best_score < score:
			best_route = my_route
			best_score = score
			best_score_time = current_time
			print "NEW SCORE!!!"
			print best_score
			print best_route
			print best_score_time
		elif best_score == score:
			if best_score_time > current_time:
				best_route = my_route
				best_score_time = current_time
				print "NEW TIME!"
				print best_score
				print best_route
				print best_score_time
			else:
				#print "processing..."
				pass
		else:
			#print "processing..."
			pass

best_route = {}
best_score = 27
best_score_time = 7*60+12
def routeByRoundRobin():
	rest = list(indexs)
	next = 0
	rt = []
	rt.append(next) #最初だけ別に
	rest.remove(next) #最初だけべつに

	roundRobin(rt[-1], rest, rt, 0)
	return best_route, best_score_time

#総当り
def roundRobin(dep_index, my_rest, my_route, current_time):
	if not my_rest:#my_restが空
		global best_score
		global best_route
		global best_score_time
		score = len(my_route)
		print my_route
		print "%d %d" % (best_score, best_score_time)
		if best_score < score:
			best_route = my_route
			best_score = score
			best_score_time = current_time
			print "NEW SCORE!!!"
		elif best_score == score:
			if best_score_time > current_time:
				best_route = my_route
				best_score_time = current_time
				print "NEW TIME!"
			else:
				print "processing..."
		else:
			print "processing..."
	else:#中身がまだあったら、繰り返す
		for arr_index in my_rest:
			tmp_rest = list(my_rest)
			tmp_route = list(my_route)
			tmp_rest.remove(arr_index)
			latest_time = current_time + db_matrix[dep_index][arr_index][TS]
			tmp_route.append(arr_index)
			roundRobin(arr_index, tmp_rest, tmp_route, latest_time)

class Route:
	def __init__(self, m):
		self.method = m
		self.route = None
		self.route = -1
		if self.method == "GREEDY":
			self.route, self.time = routeByGreedy()
		elif self.method == "RANDOM":
			self.route, self.time = routeByRandom()
		elif self.method == "ROUND_ROBIN":
			self.route, self.time = routeByRoundRobin()
		elif self.method == "SMART":
			self.route, self.time = routeBySmart()
		elif self.method == "CGREEDY":
			self.route, self.time = routeByCheatedGreedy()
 		else:
			print "failed!!!"

	def show(self):
		printRoute(self.route)
		printMinToTime(self.time)

def main():
	r0 = Route("SMART")
	r0.show()
	#r1 = Route("RANDOM")
	#r1.show()
	#r2 = Route("RANDOM")
	#r2.show()
	#pass

if __name__ == '__main__':
	prepareData()
	#for i in range(10):
	main()
	cur.close()
	conn.close()