from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///travel.db"

db = SQLAlchemy(app)


class DestinationModel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    destination = db.Column(db.String(50), nullable = False)
    country = db.Column(db.String(50), nullable = False)
    rating = db.Column(db.Float)


    def to_dict(self):
        return {
            "id" : self.id,
            "destination" : self.destination,
            "country" : self.country,
            "rating" : self.rating
        }


with app.app_context():
    db.create_all()


#GET destinations
@app.route("/destinations", methods=["GET"])
def get_destinations():
    destinations = DestinationModel.query.all()
    return jsonify([destination.to_dict() for destination in destinations])




#Get destination by id
@app.route("/destinations/<int:destination_id>", methods = ["GET"])
def  get_destination(destination_id):
    destination = DestinationModel.query.get(destination_id)
    if destination:
        return jsonify(destination.to_dict())
    else:
        return jsonify({"error":"Destination not Valid"}), 404



#Post, add data
@app.route("/destinations", methods=["POST"])
def add_destination():
    data = request.get_json()
    new_destination = DestinationModel(destination=data["destination"], country=data["country"], rating=data["rating"])
    db.session.add(new_destination)
    db.session.commit()

    return jsonify(new_destination.to_dict()), 201



#PUT Update
@app.route("/destinations/<int:destination_id>", methods=["PUT"])
def update_destination(destination_id):
    data = request.get_json()
    new_update = DestinationModel.query.get(destination_id)
    if new_update:
        new_update.destination=data.get("destination", new_update.destination)
        new_update.country=data.get("country", new_update.country)
        new_update.rating=data.get("rating", new_update.rating)

        db.session.commit()

        return jsonify(new_update.to_dict())
    else:
        return jsonify({"error":"Destination not found!"}), 404




#Delete
@app.route("/destinations/<int:destination_id>", methods=["DELETE"])
def delete_destination(destination_id):
    remove_object = DestinationModel.query.get(destination_id)
    if remove_object:
        db.session.delete(remove_object)
        db.session.commit()

        return jsonify({"message":"Destination has been removed"})

    else:
        return jsonify({"error":"Destination not found"}), 404




@app.route('/')

def Home():
    return jsonify({"message" : "Welcome to Travel Api"})
    



if __name__ == "__main__":
    app.run(debug=True)