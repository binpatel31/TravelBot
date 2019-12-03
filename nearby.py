from geopy import Nominatim
geolocator = Nominatim()
place = input("Enter the place:")
location = geolocator.geocode(place)
print(location.address)
print(location.latitude)
print(location.longitude)
import urllib.request
import json
endpoint = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
api_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
loc = str(location.latitude)+','+str(location.longitude);
radius = 1500;
stype = 'restaurant';
print(loc)
nav_req = '?location={}&radius={}&type={}&key={}'.format(loc,radius,stype,api_key)
request = endpoint+nav_req;
response = urllib.request.urlopen(request).read()
places_search = json.loads(response)
#print(places_search)
#print(places_search.keys())
results = places_search['results']
#print("\n\n")
print('***************result*********')
#print(results)
print(results[0].keys())
photos = ''
for i in range(0,len(results)):
	#geometry=results[i]['geometry']
	#vicinity=results[i]['vicinity']
	name=results[i]['name']
	reference=results[i]['reference']
	photos=results[i]['photos']
	#rating=results[i]['rating']
	#print(vicinity)
	#print(geometry)
	for p in photos:
		print(p)
	print(name)
	print(reference)
	#print(rating)
	break

val = input("want to know current weather?")    
if val == '1':
    import pyowm
    owm = pyowm.OWM('0f8abea03bc1ec680faf61d204b089a3')
    observation = owm.weather_at_place(location.address)
    w = observation.get_weather()
    import dateutil.parser
    yourdate = dateutil.parser.parse(w.get_sunrise_time('iso'))
    print('Sunrise time:',yourdate)
    yourdate = dateutil.parser.parse(w.get_sunset_time('iso'))
    print('Sunset time:', yourdate)
    print('Status:', w.get_detailed_status())
    print('Wind:',w.get_wind()['speed'])
    print('Humidity:',w.get_humidity())
    temp=w.get_temperature('celsius')
    print('Temperature:',temp['temp'])
else:
    print('Closing...')
