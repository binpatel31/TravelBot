
def followup(msg):
	if(qry.split(" ")[1] in ["near","in"] and len(qry.split(" "))<6 and len(qry.split(" "))>2):
		#if(" ".join(qry.split(" ")[:2]) in ["ATMs near","Restaurants near", "Parks near", "Pharmcy near"]):
			print("Followup Qry 1")
			doc = nlp(qry)
			lst = []
			for X in doc.ents:
				if(X.label_ == "GPE"):
					print(X.text)
					resp = nearby(" ".join(qry.split(" ")[:2])+" "+X.text)
					for r in resp:
						if 'photos' in r.keys():
							# (['formatted_address', 'geometry', 'icon', 'id', 'name', 'opening_hours', 'photos', 'place_id', 'plus_code', 'rating', 'reference', 'types', 'user_ratings_total']
							url = "https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference="+r["photos"][0]["photo_reference"]+"&key="+key
							url = """<a onclick= "document.getElementById('myModal').style.display = 'block';document.getElementById('img01').src = '"""+url+"""'; ">	Photos</a>	""";
							lst.append("Name: "+r['name']+" Photo: <b><u>"+url+"</u></b><br/>")
							
							
			return {'resp':lst}