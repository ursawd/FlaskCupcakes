"""Flask app for Cupcakes"""
# .env
import os
from dotenv import load_dotenv
from flask import Flask, request, redirect, render_template, flash, jsonify
from models import db, connect_db, Cupcake

# .env
load_dotenv()

app = Flask(__name__)

# .env
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///cupcake"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

connect_db(app)

# ----------------------------------------------------------------------
def serialize_cupcake(cupcake):
    """takes db record and returns dict of db record"""
    return {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image,
    }


# ----------------------------------------------------------------------
@app.route("/api/cupcakes")
def return_cupcakes():
    """return list of cupcakes as JSON"""

    # query all cupcake records from db
    cupcakes = Cupcake.query.all()
    # change db record objects into dict with serialize_cupcake function
    serialized = [serialize_cupcake(cake) for cake in cupcakes]

    return jsonify(cupcakes=serialized)


# ----------------------------------------------------------------------
@app.route("/api/cupcakes/<int:cupcake_id>")
def return_cupcake(cupcake_id):
    """return a cupcake as JSON"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = serialize_cupcake(cupcake)

    return jsonify(cupcake=serialized)


# ----------------------------------------------------------------------
@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    """makes a cupcake in db, return created record as json"""

    flavor = request.json["flavor"]
    rating = request.json["rating"]
    size = request.json["size"]
    image = request.json["image"]

    cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(cupcake)
    db.session.commit()

    serialized = serialize_cupcake(cupcake)

    return (jsonify(cupcake=serialized), 201)


# ----------------------------------------------------------------------
@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def patch_cake(cupcake_id):
    """patch route to update a cupcake"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake.flavor = request.json["flavor"]
    cupcake.size = request.json["size"]
    cupcake.rating = request.json["rating"]
    cupcake.image = request.json["image"]

    db.session.add(cupcake)
    db.session.commit()

    serialized = serialize_cupcake(cupcake)

    return (jsonify(cupcake=serialized), 200)


# ----------------------------------------------------------------------
@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def delete_cake(cupcake_id):
    """delete cupcake record by id from db"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    id = cupcake.id

    db.session.delete(cupcake)
    db.session.commit()

    return (jsonify({"message": f"Deleted record {id}"}), 200)
