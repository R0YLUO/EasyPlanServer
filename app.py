from flask import Flask, request, jsonify
from recommendations import recommendation
from random_string import generate_unique_random_string


app = Flask(__name__)

existing_strings = set()
groups = {}

@app.route('/recommendations', methods=['GET'])
def get_recommendations():
    group_key = request.args.get("group")
    if group_key not in groups:
        return jsonify({ "message": "Group not found", "status": 404 })
    locations = groups[group_key]["locations"]
    food_preferences = groups[group_key]["foodPreferences"]
    return recommendation(locations, food_preferences)

@app.route('/group', methods=['GET'])
def get_group():
    try:
        return jsonify(groups[request.args.get("group")])
    except KeyError:
        return jsonify({ "message": "Group not found", "status": 404 })

@app.route('/join-group', methods=['POST'])
def join_group():
    group_key = request.args.get("group")
    if group_key not in groups:
        return jsonify({ "message": "Group not found", "status": 404 })
    try: 
        name = request.json["name"]
        groups[group_key]["members"].append(name)
        return jsonify({ "message": "Success", "group": groups[group_key], "status": 200 })
    except KeyError:
        return jsonify({ "message": "Name not provided", "status": 400 })


@app.route('/new-group', methods=['POST'])
def create_group():
    group_key = generate_unique_random_string(existing_strings=existing_strings)
    groups[group_key] = {
        "foodPreferences": [],
        "members": [],
        "locations": []
    }
    return jsonify({"group": group_key})

@app.route('/set-food-preferences', methods=['POST'])
def set_food_preferences():
    group_key = request.args.get("group")
    if group_key not in groups:
        return jsonify({ "message": "Group not found", "status": 404 })
    try:
        food_preferences = request.json["foodPreferences"]
        groups[group_key]["foodPreferences"].append(food_preferences)
        return jsonify({ "message": "Success", "group": groups[group_key], "status": 200 })
    except KeyError:
        return jsonify({ "message": "Food preferences not provided", "status": 400 })

@app.route('/set-locations', methods=['POST'])
def set_locations():
    group_key = request.args.get("group")
    if group_key not in groups:
        return jsonify({ "message": "Group not found", "status": 404 })
    try:
        lon = request.json["lon"]
        lat = request.json["lat"]
        groups[group_key]["locations"].append((lon, lat))
        return jsonify({ "message": "Success", "group": groups[group_key], "status": 200 })
    except KeyError:
        return jsonify({ "message": "Location not provided", "status": 400 })

if __name__ == '__main__':
    app.run(debug=True)
