import requests
import calendar
from geopy import Nominatim
import pyowm
import dateutil.parser

def weather(city, date1):
	api_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
	api_call = 'https://api.openweathermap.org/data/2.5/forecast?appid=' + api_key
	api_call += '&q=' + city
	json_data = requests.get(api_call).json()
	location_data = {
			'city': json_data['city']['name'],
			'country': json_data['city']['country']
		}
	
	
	current_date = ''
	for item in json_data['list']:
		time = item['dt_txt']
		next_date, hour = time.split(' ')
		d = {}
		if current_date != next_date:
			current_date = next_date
			
			year, month, day = current_date.split('-')
			date = {'y': year, 'm': month, 'd': day}
			temperature = item['main']['temp']
			description = item['weather'][0]['description'],		
			d['status']  = description
			d['tempreature'] =  '{:.2f}'.format(temperature - 273.15)
			if(current_date == date1):
				return d
	return "----"
		

def weather_cur(place):
	d = {}
	while True:
		try:
			geolocator = Nominatim()
			location = geolocator.geocode(place, timeout=None)
			owm = pyowm.OWM('0f8abea03bc1ec680faf61d204b089a3')
			observation = owm.weather_at_place(location.address)
			w = observation.get_weather()
			yourdate = dateutil.parser.parse(w.get_sunrise_time('iso'))
			d['sunrise'] = yourdate
			yourdate = dateutil.parser.parse(w.get_sunset_time('iso'))
			d['sunset'] = yourdate
			d['status'] = w.get_detailed_status()
			d['wind'] = w.get_wind()['speed']
			d['humidity'] = w.get_humidity()
			temp=w.get_temperature('celsius')
			d['tempreature'] = temp['temp']
			return d
		except:
			print("GeoPY timeout!")
			continue
def main():
	city = input('Please input the city name: ')
	
