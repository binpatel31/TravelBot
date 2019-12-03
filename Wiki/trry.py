import os
from .seperate import mainfun
from .GrabData import grabInfo
from .filerold import writef,updb,starthere
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["travel_bot"]

def doit(name):   
	p2 = './Instantfill'
	name = grabInfo(name,p2)
	p1 = './Instantfill' + '/' + name + '/RawData.txt'
	p3 = './Instantfill' + '/' + name
	if not os.path.exists(p2):
		os.makedirs(p2)

	if not os.path.exists(p3):
		os.makedirs(p3)


	mainfun(p1,p3)
	name = starthere(name)
	return eval("mydb.data.find({'place':'"+name.lower()+"'})")
	
if __name__ == "__main__":
	name = input("Enter Name: ")
	for x in doit(name):
		print(x)