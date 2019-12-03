from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import euclidean_distances
import math
import nltk
import re
import en_core_web_sm
nlp = en_core_web_sm.load()
import spacy
from nltk.stem.porter import PorterStemmer
import pymongo

from weather import weather, weather_cur
from nearby_gfg import nearby
from bing_Map import distance, time
from formattingOutput import more
from gensim.summarization import summarize
from Wiki.trry import doit

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
db = myclient["travel_bot"]

# google maps key
key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
welcomeMessages = ['hi', 'hello', 'welcome'	]

global corpus2
def similar_query(qry):
	qry = qry.strip()

	if(qry.lower() in welcomeMessages):
		resp = "Hi.. <br/>About me: This is Travel Bot. Currently I am in new phase and can help you with your travel related queries<br/>"
		resp += "<br/>Type of Questions: <br/>"
		d = ["Which is the best place to visit in Summer?",
			"Which places are likely to be visited in Gujarat?",
			"What things should I carry along to Gir?",
			"What is the current weather of Shillong?",
			"Weather at Bhuj.",
			"Give me some information about Ahmedabad.",
			#"Tell me something about Taj Mahal",
			"What is the distance between Ahmedabad and Mumbai?",
			"How far is Kolkata from Patna?",
			"Recommend me Palace",
			]
		count = 1
		for i in d:
			resp+="<a onclick=\"document.getElementById('myMessage').value='"+i+"';document.getElementById('myMessage').focus();\">"+str(count)+". "+i+"</a><br/>"
			count+=1
		return {'resp':[resp]}
	
	if qry.split(" ")[0].lower() in ['atms', 'parks', 'pharmacy', 'restaurants']:
		# means followup for query 1(location)
		print("Followup Qry 1")
		lst = []
		resp = nearby(qry)
		for r in resp:
			if 'photos' in r.keys():
				# (['formatted_address', 'geometry', 'icon', 'id', 'name', 'opening_hours', 'photos', 'place_id', 'plus_code', 'rating', 'reference', 'types', 'user_ratings_total']
				url = "https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference="+r["photos"][0]["photo_reference"]+"&key="+key
				url = """<a onclick= "document.getElementById('myModal').style.display = 'block';document.getElementById('img01').src = '"""+url+"""'; ">	Photo</a>	""";
				lst.append("Name: "+r['name']+" |  <b><u>"+url+"</u></b><br/>")
						
						
		return {'resp':lst}
		

	corpus2 = [
		"Which is best place to visit in SEASON?",###DONE
		"Which places are likely to be visited in PLACE?", ## Will be implemented using MachineLearning
		"What things I should carry along to PLACE", ## Almost DONE
		"What is the current weather of PLACE?",	## Will e implemented using weather APIs
		"Weather at PLACE", # same as above
		"Give me some information about PLACE.",###DONE
		"Tell me something about PLACE",  # same as above
		"What is the distance between PLACE1 and PLACE2", ##  implemented using MAP APIs
		"How far is PLACE2 from PALCE1.",	   ##  implemented using MAP APIs
		"Recommend me some PLACE",
		"Welcome.",
	]
	
	corpus2.insert(0, qry)
	########### steaming ##########
	porter_stemmer = PorterStemmer()
	corpus = []
	for sent in corpus2:
		nltk_tokens = nltk.word_tokenize(sent)
		x = []
		for w in sent.split(" "):
			x.append(porter_stemmer.stem(w)+" ")
		corpus.append(''.join(x))
	################################

	############## vectorize  ###############
	vectorizer = CountVectorizer()
	features = vectorizer.fit_transform(corpus).todense() 
	min = math.inf
	index = 1
	
	for i in range(1,len(features)):
		f = features[i]
		d = euclidean_distances(features[0], f)
		#print("\n corpus:", "\n"+corpus[i], "\n Distance: ", d)
		if (d<min):
			index = i
			min = d
	##########################################
	print("Index: ", index)
	if(index == 1 or index ==2):
		print("Similar to Q1(Location)")
		doc = nlp(qry)
		lst = []
		
		for X in doc.ents:
			if(X.label_ == "GPE" or X.label_=="PERSON" or X.label_=="ORG"):
				city = X.text
				print(city)
				x = eval("db.data.find({'$or': [{'city':{'$regex':'"+city.lower()+"'}}, {'state':{'$regex':'"+city.lower()+"'}} ]},{'_id':0,'place':1})")
				lst.append("<br/>Places in "+city.title()+":<br/>")
							
				## preety ##
				count = 1				
				for c in x:
					m = "Give me some information about " + c['place'].title() + "."
					lst.append(str(count) + """. <u><a onclick="document.getElementById('myMessage').value = '"""+m+"""'; document.getElementById('sendbutton').click();" ></u>"""+ c['place'].title() +"""</a></u><br/>""")
					count+=1
				d = {"nearby ATMs":"ATMs near "+city, "nearby Restaurants":"Restaurants near "+city, "nearby Parks":"Parks near "+city, "nearby Pharmacy":"Pharmacy near "+city}	
				return {'resp':more(lst), 'followup': d}
				
			elif(X.label_ == "DATE"):
				print("Similar to Q1(Season)")
				season = X.text
				x = eval("db.data.find({'metadata':{'$exists': True}, 'season': '"+ season.lower() +"' }, {'_id':0})")
				
				## preety ##
				count = 1
				x = x[0]
				places = x['place'].split(',')	#string of list of all places, seperated by ','
				lst.append("<br/>"+season+" Places: <br/>")
				for i in places:
					m = "Give me some information about " + i.title() + "."
					#lst.append(str(count)+". "+i.title()+"<br/>")
					lst.append("""<u><a onclick="document.getElementById('myMessage').value = '"""+m+"""'; document.getElementById('sendbutton').click();" ></u>"""+str(count)+". " +i.title() +"""</a></u><br/>""")
					count+=1
					
			return {'resp':"".join(more(lst))}	
	elif(index == 3):
		print("Similar to Q3")
		doc = nlp(qry)
		X = doc.ents
		print(len(x))
		if(len(X) == 0):
			city = qry.split[-1]			
		else:
			city = X[0].text
		regx = str(re.compile(".*"+city+".*"))
		x = eval("db.data.find( { 'place':{'$regex':"+ regx +", '$options':'i'} , 'season':{'$exists':True}} , {'season':1, '_id':0})")
		item_list = []
		xc= x.count()		
		print(xc)
		if(xc>0):
			x = x.next()
			print(x)
			if(x['season']=='Winter'):
				item_list.extend(['Warm Clothes ', 'Medicines ', 'Deodrants ', 'Official documents ', 'blankets ' ])
			elif(x['season']=='Summer'):
				item_list.extend(['SunGlasses ', 'Medicines ', 'Cap/Hat ', 'Deodrants ', 'Skin Lotion ' ])
			else:
				item_list.extend(['Umbrella ', 'Medicines ', 'Deodrants ', 'Locks ', 'official documents ' ])
		resp = ''
		count = 1
		for item in item_list:
			resp += str(count) + ". " + item + "<br/>"
			count += 1
		return {'resp':resp}
		pass
	elif(index == 4 or index == 5):	
		print("Similar to Q4,5")
		doc = nlp(qry)
		if(len(doc.ents)==0):
			return {'resp':"------"}
		X = doc.ents[0]
		d = weather_cur(X.text)
		print(d)
		return {'resp':"The weather details are: <br/> Status: "+d['status']+"<br/>Tempreature: "+str(d['tempreature'])}
		
	elif(index == 6 or index ==7):
		print("Similar to Q6,7")
		doc = nlp(qry)
		ansss=""
		X = {}
		if(len(doc.ents) == 0):
			lssst = qry.strip().split()
			ay=11
			#ansss="q"
			a=db.data.find({'metadata':{'$exists':False}},{'city':1, 'state':1, 'place':1})
			all_places_folder = []
			for aaa in a:
				#print("What is keys ",aaa.keys())
				all_places_folder.append(aaa['place'])
				if('city' in aaa):
					all_places_folder.append(aaa['city'])
				if('state' in aaa):
					all_places_folder.append(aaa['state'])
			for ii in all_places_folder:
				if(ay==119):
					break
				#print("ii:", ii)
				if(ii in lssst):
					ansss = ii
					ay=119
					print("INSDE",ansss)
					print("Spacy not found PLACE", ansss, ":")
					city = ansss
					X = eval("""db.data.find({'$or':[{'city': {'$regex' : \""""+ city.lower() +""""}}, {'state': {'$regex' : \""""+ city.lower() +""""}},{'place':{'$regex' : \""""+ city.lower() +""""}}]})""")
					break
		else:
			X = doc.ents[0]
			city = X.text
			print(city)
			#X = eval("""db.data.find({'$or':[{'city': {'$regex' : \""""+ city.lower() +""""}}, {'state': {'$regex' : \""""+ city.lower() +""""}},{'place':{'$regex' : \""""+ city.lower() +""""}}]})""")
			q = "db.data.find({'$or':[{'city':'"+city.lower()+"'}, {'state': '"+city.lower()+"'},{'place':'"+city.lower()+"'}]})"
			print(q)
			X = eval(q)
			print(X.count())
			if(X.count()==0):
				lssst = qry.split()
				a=db.data.find({},{'city':1, 'state':1, 'place':1})
				all_places_folder = []
				for aaa in a:
					#print("What is keys ",aaa.keys())
					all_places_folder.append(aaa['place'])
					if('city' in aaa):
						all_places_folder.append(aaa['city'])
					if('state' in aaa):
						all_places_folder.append(aaa['state'])
				fin=[]
				ay=11
				for ii in all_places_folder:
					if(ay==119):
						break
					temp11=ii.split(',')
					#fin.extend(temp1)
					for jj1 in temp11:
						temp2=jj1.split()
						if(set(lssst).intersection(set(temp2))):
							ansss = jj1
							ay=119
							print("INSDE",ansss)
							break
				print("In else city we found not spacy", ansss)
				X = eval("db.data.find({'$or':[{'city':'"+ansss.lower()+"'}, {'state': '"+ansss.lower()+"'},{'place':'"+ansss.lower()+"'}]})")
				if(X.count()==0):
					print("Palce not in DB, Adding")
					# means place not found in database!! SO sarthi wala program run karo
					print(city)
					X = doit(city)
					print(X.count())
					
					
		if(X.count()==0):
			lst = ["Sorry!<br/>"]
		else:
			lst = []
		#X = [{},{},{}]
		for x in X:
			count = 1
			print("X key",list(x.keys()))
			if 'attributes' in list(x.keys()):
				print("attributes in ")
				lst.append(x['place'].title() + "<br>")
				flag = 0
				st = x['attributes'].split(",")				
				for S in st:
					s = S[:-4]
					if(s in x.keys()):
						if(len(x[s].split("."))>3):
							if(s == "RawData"):
								content = '"'+summarize(x[s], ratio=0.1).replace('"', "&quot;").replace("'","&#39;").replace("\n", "<br/>").replace("\r", "    ")+'"'
							else:
								content = '"'+summarize(x[s], ratio=0.25).replace('"', "&quot").replace("'","&apos;").replace("\n", "<br/>").replace("‘", "&lsquo;").replace("’", "&lrquo;")+'"'
							if(len(content) > 5):
								flag = 1
								lst.append("""&nbsp &nbsp <a onclick = 'document.getElementById("myModalT").style.display = "block"; document.getElementById("contentT").innerHTML="""+content+""" '> """+ str(count) + "." + s + "</a><br/>")
								count+=1	
				if(flag == 0):
					#lst.append("&nbsp &nbsp Sorry, No information<br/>")
					lst.pop()
					
					
		return {'resp':"".join(lst)}

	elif(index == 8):
		print("Similar to Q8")
		doc = nlp(qry)
		X = doc.ents
		loc = []
		resp = ''
		print("LEN", len(X))
		if(len(X)>=2):
			for x in X:
				if(x.label_ == 'GPE' or x.label_=='ORG'):
					print(x.text)
					loc.append(x.text)
			if(len(loc)>=2):
				dist = distance(loc[0], loc[1])
				resp = "Distance between "+str(loc[0])+" and "+str(loc[1])+" is "+str(dist)+" Kms"
			else:
				loc1 = re.sub(r"[^a-zA-Z0-9]+", '', qry.split(" ")[:-1])
				loc2 = re.sub(r"[^a-zA-Z0-9]+", '', qry.split(" ")[:-3])
				distance(loc1, loc2)
				resp = "Distance between "+str(loc[0])+" and "+str(loc[1])+" is "+str(dist)+" Kms"
		return {'resp': resp}
		
	elif(index == 9):
		print("Similar to Q9")
		doc = nlp(qry)
		X = doc.ents
		loc = []
		if(len(X)>=2):
			for x in X:
				if(x.label_ == 'GPE' or x.label_=='ORG'):
					loc.append(x.text)
			if(len(loc)>=2):
				tim = time(loc[0], loc[1])
				resp = str(loc[0]) +" is "+str(tim)+" minutes away from "+str(loc[1])
			else:
				resp = "No City found" 
				qs = qry.split(" ")
				loc = []
				
				loc.append(re.sub(r"[^a-zA-Z0-9]+", '', qs[-1]))
				loc.append(re.sub(r"[^a-zA-Z0-9]+", '', qs[-3]))
				
				tim = time(loc[0], loc[1])
				resp = str(loc[0]) +" is "+str(tim)+" minutes away from "+str(loc[1])
		return {'resp': resp}
	elif(index==10):
		print("Similar to Q10")
		place_to_recommend = []
		lssst = qry.split()
		lssst=list(map(lambda x: x.lower(), lssst))
		a=db.data.find({},{'city':1, 'state':1, 'place':1})
		all_places_folder = []
		for aaa in a:
			#print("What is keys ",aaa.keys())
			all_places_folder.append(aaa['place'])
			if('city' in aaa):
				all_places_folder.append(aaa['city'])
			if('state' in aaa):
				all_places_folder.append(aaa['state'])
		fin=[]
		for ii in all_places_folder:
			temp11=ii.split(',')
			for jj1 in temp11:
				temp2=jj1.split()
				temp2=list(map(lambda x: x.lower(), temp2))
				if(set(lssst).intersection(set(temp2))):
					ansss = jj1
					place_to_recommend.append(ansss)
					print("INSDE",ansss)
		
		place_to_recommend= list(set(place_to_recommend))
		resp = ""
		count = 1
		for places in place_to_recommend:
			m = "Give me some information about "+places.title()
			resp += """<a onclick="document.getElementById('myMessage').value='"""+m+"""';document.getElementById('sendbutton').click();">"""+str(count)+". "+places.title()+"</a><br/>"
			count+=1
		return {'resp': resp}
	
	
	elif(index==11):
		print("Welcome qry")
		resp = "Welcome, I am a Travel-Bot. <br/> How may I help you?"
		return {'resp': resp}
	# ChatterBot the general chatbot will be implementd hear
	
	return {'resp':"Some Error occured!"}
	
	
	"""
	elif(index == 2):
		print("Similar to Q2")
		doc = nlp(qry)
		if(len(doc.ents)==0):
			city = qry.split(" ")[-1].trim()
			if(city[-1] == '?'):
				city = city[:-1]
		else:
			X = doc.ents[0]
			city = X.text
		print("City: ", city)	
		x = eval("db.data.find({'$or':[{'city':'"+city+"'},{'state':'"+city+"'}]}, {'_id':0, 'place':1})")
		lst = []
		count = 1
		for i in x:
			print(i)
			p = i['place']
			m="Give me some information about "+p
			lst.append(str(count)+". <u><a onclick='document.getElementById(\"myMessage\").value = \""+m+"\"; document.getElementById(\"sendbutton\").click()' ></u>"+ p +"</a></u><br/>")
			count+=1
		return {'resp': " ".join(lst)}

		pass
	"""
	