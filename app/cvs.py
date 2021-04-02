from typing import Dict, List, TypedDict
import csv

import requests
from geopy import distance


url = "https://www.cvs.com/immunizations/covid-19-vaccine.vaccine-status.json?vaccineinfo"
s = requests.Session()
s.headers.update({"User-Agent": "closest vaccine appointment finder"})

class AppointmentData(TypedDict):
    city: str
    state: str
    status: str

def get_vaccine_info():
    r = s.get(url)
    r.raise_for_status()

    d = r.json()
    return d.get('responsePayloadData', {}).get("data")

def get_availabilities_for_state(state: str) -> List[AppointmentData]:
    state_data = get_vaccine_info().get(state)
    available_appts_for_state = [appt for appt in state_data if appt.get("status") == "Available"]
    return available_appts_for_state

def get_coords_from_csv(cities: List[str], state: str):
    coords = {}
    print(cities)
    with open('us_cities.csv') as f:
        reader = csv.DictReader(f, delimiter=",")
        for row in reader:
            if row["STATE_CODE"].upper() == state and row["CITY"].upper() in cities:
                coords[f"{row['CITY'].upper()}, {state}"] = [row["LATITUDE"], row["LONGITUDE"]]

    return coords

def get_distance_between_two_coords(point_a, point_b):
    return int(distance.geodesic(point_a, point_b).miles)
