import os
import pymongo
from geopy.geocoders import Nominatim

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["travel_bot"]
mycol = mydb['data']

def updb(file,value,city):	
	#print("-------------\nFILE: ",file +"\n" +"season"+"\nCITY: "+city+"\n, VALUE:", len(value))
	result = mycol.update({'place':city},{'$set':{file: value}},upsert = True)
	return 
    
def writef(file,path,place):
    fo=open(os.path.join(path, file),'r',encoding='UTF8')    
    filename,file_extension=os.path.splitext(file)
    m=fo.read()
    updb(filename,m,place)
    fo.close()
    return

def starthere(name):
	x="./Instantfill/"
	z=str(x) + str(name)
	items = os.listdir(z)
	# adding "attributes": "Rawdata.txt,History.txt..."
	attribute = ",".join(items)
	d = {}
	d['attributes'] = attribute
	# adding place, city, state
	n = Nominatim(user_agent="Wiki").geocode(name,  addressdetails=True, timeout=None)
	info = n.raw['address']
	print(info)
	d['place'] = name.lower()
	if("city" in info.keys()):
		d['city']= info['city'].lower()
	elif('state_district' in info.keys()):
		d['city']= info['state_district'].lower()
	if('state' in info.keys()):
		d['state']= info['state'].lower()
	if('country' in info.keys()):
		d['country']= "India" if info['country']=='in' else info['country'].title()

	print("Inserting: ", d)
	mycol.insert(d)
	for i in range(len(items)):
		print(items[i])
		writef(items[i],z,name.lower())
	
	return name.lower()
	
	
	