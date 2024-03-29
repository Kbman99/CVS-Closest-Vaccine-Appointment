from app import app, cvs

from operator import itemgetter

from flask import render_template, jsonify

@app.route('/')
def hello():
    return render_template("index.html")

@app.route('/ping')
def ping():
    return jsonify("pong")

@app.route('/appointments/<state>/<city>', methods=['GET'])
def appointments(state: str, city: str):
    state = state.upper()
    city = city.upper()

    available_appts_for_state = cvs.get_availabilities_for_state(state)
    base_coords = cvs.get_coords_from_csv([city], state)
    if not base_coords:
        return jsonify({"error": "invalid state code or city in url"}), 200

    cities = [appt.get("city") for appt in available_appts_for_state]
    available_appt_coords = cvs.get_coords_from_csv(cities, state)

    appt_data = []
    for appt in available_appts_for_state:
        try:
            appt["distance"] = cvs.get_distance_between_two_coords(base_coords[f"{city}, {state}"], available_appt_coords[f"{appt['city']}, {appt['state']}"])
        except KeyError:
            continue
        appt_data.append(appt)

    sorted_by_distance_appt_data = sorted(appt_data, key=itemgetter('distance'))
    
    return jsonify(sorted_by_distance_appt_data)
