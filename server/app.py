# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here

# The view should query the database to get the earthquake with that id, and return a response containing the model attributes and values (id, location, magnitude, year) formatted as an JSON string. 
# The response should include an error message if no row is found. Don't forget to import Earthquake from the models module.
@app.route('/earthquakes/<int:id>')
def earthquake_by_id(id):
    earthquake = Earthquake.query.filter(Earthquake.id == id).first()

    if earthquake:
        body = {'id': earthquake.id,
                'magnitude': earthquake.magnitude,
                'location': earthquake.location,
                'year': earthquake.year}
        status = 200
    else:
        body = {'message': f'Earthquake {id} not found.'}
        status = 404

    return make_response(body, status)


# The view should query the database to get all earthquakes having a magnitude greater than or equal to the parameter value, 
# and return a JSON response containing the count of matching rows along with a list containing the data for each row.
@app.route('/earthquakes/magnitude/<float:magnitude>')
def earthquake_by_magnitude(magnitude):
    earthquakes = []
    for earthquake in Earthquake.query.filter(Earthquake.magnitude >= magnitude).all():
        earthquake_dict = {'id': earthquake.id,
                            'magnitude': earthquake.magnitude,
                            'location': earthquake.location,
                            'year': earthquake.year}
        earthquakes.append(earthquake_dict)
    body = {"count": len(earthquakes),
                'quakes': earthquakes
            }


    return make_response(body, 200)



if __name__ == '__main__':
    app.run(port=5555, debug=True)
