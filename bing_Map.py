import urllib, json
from Latitude_Longitude import get_lat_log

def distance(place1, place2):
	#[(ola, olo), (dla, dlo)] = get_lat_log("mumbai", "delhi")
	[(ola, olo), (dla, dlo)] = get_lat_log(place1, place2)

	bingMapsKey = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
	routeUrl = "https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix?origins="+str(ola)+","+str(olo)+"&destinations="+str(dla)+","+str(dlo)+"&travelMode=driving&key="+str(bingMapsKey)
	r = urllib.request.urlopen(routeUrl)
	data = json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))

	return (data["resourceSets"][0]["resources"][0]["results"][0]['travelDistance'])
	
def time(place1, place2):
	#[(ola, olo), (dla, dlo)] = get_lat_log("mumbai", "delhi")
	[(ola, olo), (dla, dlo)] = get_lat_log(place1, place2)

	bingMapsKey = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
	routeUrl = "https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix?origins="+str(ola)+","+str(olo)+"&destinations="+str(dla)+","+str(dlo)+"&travelMode=driving&key="+str(bingMapsKey)
	r = urllib.request.urlopen(routeUrl)
	data = json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))

	return (data["resourceSets"][0]["resources"][0]["results"][0]['travelDuration'])