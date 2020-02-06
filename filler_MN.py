
# coding: utf-8

# In[195]:


import os
import pymongo


# In[236]:


# if you want to add something else in database, but of the same structure, just change the path below
path = ".\RawData"
os.chdir(path)
print(os.listdir())

print(os.listdir())
info = []

for d in os.listdir():
    #print(os.listdir())
    if(os.path.isdir(d)):
        #print("\n--- ",d)
        os.chdir(d)
        for e in os.listdir():
            #print(os.listdir())
            if(os.path.isdir(e)):
                #print("\n------ ",e)
                os.chdir(e)
                for f in os.listdir():
                    #print(os.listdir())
                    if(os.path.isdir(f)):
                        #print("\n--------- ",f)
                        os.chdir(f)
                        for g in os.listdir():
                            #print(os.listdir())
                            if(os.path.isdir(g)):                                
                                dictionary = {}
                                #print("------------ ", g)
                                os.chdir(g)
                                #print("\n{1}, {2}, {3},{4}\n".format(0, g,f,e,d))
                                dictionary['place'] = g.strip() #print("Place: ",g)
                                dictionary['city'] = f.strip() #print("City: ", f)
                                dictionary['state'] = e.strip() #print("State: ", e)
                                dictionary['country'] = d.strip() #print("Country: ", d)
                                st = ''
                                for i in os.listdir():
                                    print(e,",",f,",",g,",",i)
                                    try:
                                        with open(i,'rb') as fi:
                                            lines = fi.read().decode("utf-8", "replace").strip()
                                            dictionary[i[:-4]] = lines
                                    except UnicodeDecodeError:
                                        with open(i,'r') as fi:
                                            lines = fi.read().decode("utf-8", "replace").strip()
                                            dictionary[i[:-4]] = lines
                                    st += i+","
                                dictionary['attributes'] = st[:-1].strip()
                                stateInfo = ''
                                for x in [f for f in os.listdir("../..") if os.path.isfile(os.path.join("../..",f))]:
                                    stateInfo += x + ','
                                stateInfo = stateInfo[:-1]
                                dictionary['stateInfo'] = stateInfo
                                # pymongo to update in "place info"
                                #print([i for i in dictionary.keys()])
                                info.append(dictionary)
                                #print("-------------------------")
                                os.chdir("..")
                        os.chdir("..")
                os.chdir("..")    
        os.chdir("..")
    
   
os.chdir("C:/Users/DELL/Desktop/Proj-sem7/AllAboutBot/RawData")

# In[237]:


################ now adding meta data files
metadata = ['season']  # for now, only season. We can add more fields as we want
infoMeta = []
for m in metadata:
    season = ['summer', 'winter', 'spring']
    for s in season:
        dictionary = {}
        dictionary['place'] = ''
        with open("C:/Users/DELL/Desktop/Proj-sem7/AllAboutBot/RawData/"+s+".txt", 'r', encoding='windows-1252') as f:
            lines = f.readlines()
            for l in lines:
                place = ''
                for p in l.split(':')[0].split(" "):
                    place += p[0].upper() + p[1:] + " "
                dictionary['place'] += place[:-1] + ","
        
        dictionary['place'] = dictionary['place'][:-1]  # removing trailing ','
        dictionary['season'] = s
        dictionary['metadata'] = True
        infoMeta.append(dictionary)


# In[241]:


client = pymongo.MongoClient("mongodb://localhost:27017")
mydb = client['travel_bot']

##### IMPORTANT  ############
# delete the old collection before inserting data again
#mydb.data.drop()
mycol = mydb['data']
############################

result = mycol.insert_many(info)
print("documnet added: ",len(result.inserted_ids))
result = mycol.insert_many(infoMeta)
print("documnet added: ",len(result.inserted_ids))




for i in mycol.find({'season':'spring'},{'place':1, '_id':0}):
    print(i['place'].split(','))

