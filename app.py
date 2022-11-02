from flask import Flask, request, jsonify, render_template
# from flask_cors import CORS, cross_origin

from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"
# app.config['CORS_SUPPORTS_CREDENTIALS'] = True

connect_db(app)

@app.route('/')
def show_home_page():
    """Return html home page"""
    cupcakes = Cupcake.query.all()
    return render_template('home.html', cupcakes = cupcakes)

@app.route('/api/cupcakes')
def get_cupcakes():
    """Get data about all cupcakes, return JSON
    {cupcakes: [{id, flavor, size, rating, image}, ...]}
    """

    cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)

@app.route('/api/cupcakes/<int:cupcake_id>')
def get_cupcake(cupcake_id):
    """Get data about a single cupcake, return JSON
    {cupcake: {id, flavor, size, rating, imgage}} or 404 if not found"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake = cupcake.serialize())

@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    """Create a new cupcake"""

    new_cupcake = Cupcake(flavor=request.json["flavor"], size=request.json["size"],
                          rating=request.json["rating"], image=request.json["image"])
    db.session.add(new_cupcake)
    db.session.commit()
    response_json = jsonify(cupcake=new_cupcake.serialize())
    return (response_json, 201)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PUT'])
def update_cupcake(cupcake_id):
    """Update a cupcake or raise 404 if not found
    Return JSON {cupcake: {id, flavor, size, rating, image}}"""

    cupcake = Cupcake.query.get_or_404(cupcake_id) #get cupcake by id

    cupcake.flavor = request.json.get("flavor", cupcake.flavor) #update cupcake props
    cupcake.size = request.json.get("size", cupcake.size)
    cupcake.rating = request.json.get("rating", cupcake.rating)
    cupcake.image = request.json.get("image", cupcake.image)
    db.session.commit()

    return jsonify(cupcake = cupcake.serialize())

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    """Delete a cupcake or raise a 404 if it doesn't exist"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")