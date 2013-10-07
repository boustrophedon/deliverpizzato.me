import math

from locu.api import VenueApiClient

from config import api_key

def get_pizza_places(lat, long, radius):
	venue_client = VenueApiClient(api_key)

	venues = venue_client.search(cuisine=['pizza'], location = (lat,long), radius=radius)
	
	return venues


#def distance(base, other):
#	return math.sqrt( (base[0] - other[0])**2 + (base[1] - other[1])**2)

def distance(base, other):
    lat1,lon1 = map(math.radians, base)
    lat2,lon2 = map(math.radians, other)
    radius = 6371
    return math.acos(math.sin(lat1)*math.sin(lat2) + 
                        math.cos(lat1)*math.cos(lat2) *
                        math.cos(lon2-lon1)) * radius;


def get_closest_ten(base, places):
	distances = list()
	for place in places['objects']:
		distances.append( (distance(base, (place['lat'], place['long']) ), place) )

	return [x[1] for x in sorted(distances, key= lambda x:x[0])[0:10]]

def parse_chosen(places, day):
	parsed_list = list()
	venue_client = VenueApiClient(api_key)
	for place in places:
		venue_info = venue_client.get_details(place['id'])['objects'][0]
	
		d = dict()
		d['name'] = place['name']
		d['addr'] = place['street_address']+", "+place['locality']+", "+place['region']
		d['phone'] = place['phone']
		phnum = place['phone'].replace("(", "").replace(")","").replace(" ","").replace("-","")
		d['int_phone'] = "+1"+phnum
		d['open_hours'] = venue_info['open_hours'][day]

		parsed_list.append(d)

	return parsed_list


