from geopy import Nominatim
import pyowm
import dateutil.parser


	geolocator = Nominatim()
	place = input("Enter the place:")
	location = geolocator.geocode(place)
	owm = pyowm.OWM('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
	observation = owm.weather_at_place(location.address)
	w = observation.get_weather()
	yourdate = dateutil.parser.parse(w.get_sunrise_time('iso'))
	print('Sunrise time:',yourdate)
	yourdate = dateutil.parser.parse(w.get_sunset_time('iso'))
	print('Sunset time:', yourdate)
	print('Status:', w.get_detailed_status())
	print('Wind:',w.get_wind()['speed'])
	print('Humidity:',w.get_humidity())
	temp=w.get_temperature('celsius')
	print('Temperature:',temp['temp'])