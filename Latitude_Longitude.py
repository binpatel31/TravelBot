from geopy.geocoders import Nominatim

def get_lat_log(loc1, loc2):
	geolocator = Nominatim(user_agent="Latitude_Longitude")

	location1 = geolocator.geocode(loc1)
	location2 = geolocator.geocode(loc2)
	
	return [(location1.latitude, location1.longitude), (location2.latitude, location2.longitude)]
	