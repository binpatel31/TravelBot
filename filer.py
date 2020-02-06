import os
import pymongoo
def updb(file,value,season,city):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["mydatabase"]
    mycol = mydb[season]
    print (file +"\n" +"season"+"\n"+city+"\n")
    
    result = mycol.update({'city':city},{'$set':{file: value}},upsert = True)
    return 
    



def writef(file,path,seasons,city):
	print("\n------\n",file,"\n----------\n")
	fo=open(os.path.join(path, file),'r',encoding='utf-8')
	filename,file_extension=os.path.splitext(file)
	m=fo.read()
	updb(filename,m,seasons,city)
	fo.close()
	return



def writedb(folder,path,seasons):
       # print (folder)
 
        v=os.path.join(path,folder)
        files=os.listdir(v)
        for x in range(len(files)):
            writef(files[x],v,seasons,folder)

        #print(*files,sep="\n ")
        return





#x="c:/users/DELL/desktop/"
x = "./all/"
Y=['_summer','_winter','_spring']
for y in Y:
	z=str(x) + str(y)
	items = os.listdir(z)

	#newlist = []
	#for names in items:
	 #   if names.endswith("."):
	  #      newlist.append(names)
	#print(*items, sep = "\n ") 
	for i in range(len(items)):
		print(items[i])
		writedb(items[i],z,y)