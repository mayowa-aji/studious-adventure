#!/usr/bin/env python3

from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate

from models import db, Hero, HeroPower, Power

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return ''

@app.route('/heroes', methods = ['GET'])
def heroes():
    heroes_list = [hero.to_dict() for hero in Hero.query.all()]
    return make_response(jsonify(heroes_list),200)

@app.route('/heroes/<int:id>', methods=['GET'])
def hero_by_id(id):
    hero = Hero.query.filter(Hero.id == id).first()

    if not hero:
        return make_response(jsonify({'error': 'Hero not found'}),404)

    if request.method == 'GET':
        return make_response(jsonify(hero.to_dict()),200)

@app.route('/powers', methods=['GET'])
def powers():
    power_list = [power.to_dict() for power in Power.query.all()]
    return make_response(jsonify(power_list),200)


@app.route('/powers/<int:id>', methods=['GET', 'PATCH'])
def powers_with_id(id):
    power = Power.query.filter(Power.id == id).first()

    if not power:
        response_dict = { "error": "Power not found"}
        response = make_response(
            jsonify(response_dict),
            404
        )
        return response

    if request.method == 'GET':
        response = make_response(jsonify(power.to_dict()), 200)
        return response

    elif request.method == 'PATCH':
        request_json = request.get_json()

        for key in request_json:
            setattr(power, key, request_json[key])

            db.session.add(power)
            db.session.commit()

            if not power:
                response_dict = { "error": "Power not found"}
                response = make_response(jsonify(response_dict),404)
                return response

        return make_response(jsonify(power.to_dict()), 200)

@app.route('/hero_powers', methods = ['POST'])
def hero_powers():
    request_json = request.get_json()
    new_hero_powers = HeroPower(
        strength = request_json.get('strength'),
        power_id = request_json.get('power_id'),
        hero_id = request_json.get('hero_id')
    )

    db.session.add(new_hero_powers)
    db.session.commit()

    if not new_hero_powers:
        response_dict = { "error": "Invalid input"}
        response = make_response(
            jsonify(response_dict),
            404
            )
        return response

    else:
        hero = new_hero_powers.hero

        response = make_response(
            jsonify(hero.to_dict()),201)

        return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)
