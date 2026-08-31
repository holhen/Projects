from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, func
import random

'''
Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record
@app.route('/random')
def get_random_cafe():
    cafes = db.session.execute(db.select(Cafe)).scalars().all()
    random_cafe = random.choice(cafes)
    return jsonify(cafe=random_cafe.to_dict())

@app.route('/all')
def get_all_cafes():
    cafes = db.session.execute(db.select(Cafe)).scalars().all()
    cafes_list = [cafe.to_dict() for cafe in cafes]
    return jsonify(cafes=cafes_list)

@app.route('/cafe/<cafe_id>')
def get_cafe(cafe_id):
    cafe = db.session.execute(db.select(Cafe).where(Cafe.id == cafe_id)).scalar()
    return jsonify(cafe=cafe.to_dict())

@app.route('/search')
def search_cafe():
    location = request.args.get('loc')
    print(location)
    cafe = db.session.execute(db.select(Cafe).where(Cafe.location == location)).scalar()
    if cafe is None:
        return jsonify(error={
            "Not Found": "Sorry, we don't have a cafe at that location",
        })
    return jsonify(cafe=cafe.to_dict())

# HTTP POST - Create Record
@app.route('/add', methods=['POST'])
def add_cafe():
    cafe = Cafe()
    cafe.name = request.form.get('name')
    cafe.map_url = request.form.get('map_url')
    cafe.img_url = request.form.get('img_url')
    cafe.location = request.form.get('location')
    cafe.seats = int(request.form.get('seats'))
    cafe.has_toilet = bool(request.form.get('has_toilet'))
    cafe.has_wifi = bool(request.form.get('has_wifi'))
    cafe.has_sockets = bool(request.form.get('has_sockets'))
    cafe.can_take_calls = bool(request.form.get('can_take_calls'))
    cafe.coffee_price = '$' + request.form.get('coffee_price')
    db.session.add(cafe)
    db.session.commit()
    return jsonify(response={
        "Success": "Successfully added cafe",
    })
# HTTP PUT/PATCH - Update Record
@app.route('/update_price/<int:cafe_id>', methods=['PATCH'])
def update_price(cafe_id):
    new_price = request.args.get("new_price")
    print(cafe_id, new_price)
    cafe = db.session.get(Cafe, cafe_id)
    if cafe is None:
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404
    else:
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the price."}), 200
# HTTP DELETE - Delete Record
@app.route('/delete/<int:cafe_id>', methods=['DELETE'])
def delete_cafe(cafe_id):
    api_key = request.args.get('api_key')
    if api_key != "TopSecretApiKey":
        return {
            "error": "Sorry, that is not allowed. Please make sure you have the correct API key and try again."
        }, 403
    else:
        cafe = db.session.get(Cafe, cafe_id)
        if cafe is None:
            return {
                "error": {
                    "Not Found": "Sorry a cafe with that id was not found in the database."
                }
            }, 404
        else:
            db.session.delete(cafe)
            db.session.commit()
            return {
                "success": "Successfully deleted cafe.",
            }

if __name__ == '__main__':
    app.run(debug=True)
