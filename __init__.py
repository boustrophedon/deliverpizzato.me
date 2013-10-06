from flask import Flask
app = Flask(__name__)

from flask import render_template
from flask import jsonify
from flask import request

from locu_utils import *

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/getPizza')
def pizza():
	lat = request.args.get('lat', 42.358766, type=float)
	long = request.args.get('long', -71.093799, type=float)
	#lat = request.args.get('lat', 0, type=float)
	#long = request.args.get('long', 0, type=float)
	day = ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')[request.args.get('day', 0, type=int)]

	places = get_pizza_places(lat,long)
	
	chosen = get_closest_ten((lat,long), places)

	places_list = parse_chosen(chosen, day) # these are all horrible names. worse is better.


	return render_template('pizza.html', places=places_list)
