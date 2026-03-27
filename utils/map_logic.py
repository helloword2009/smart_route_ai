import math
import pandas as pd
import requests
import streamlit as st


def get_real_route_from_ors(start_lat, start_lon, end_lat, end_lon):
    api_key = st.secrets["ORS_API_KEY"]

    url = "https://api.openrouteservice.org/v2/directions/driving-car/geojson"

    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json",
    }

    body = {
        "coordinates": [
            [start_lon, start_lat],
            [end_lon, end_lat]
        ]
    }

    response = requests.post(url, json=body, headers=headers, timeout=20)

    if response.status_code != 200:
        raise Exception(response.text)

    data = response.json()

    coords = data["features"][0]["geometry"]["coordinates"]
    summary = data["features"][0]["properties"]["summary"]

    return {
        "path": coords,
        "distance_km": round(summary["distance"] / 1000, 1),
        "time_min": round(summary["duration"] / 60),
    }


def load_places() -> pd.DataFrame:
    return pd.read_csv("data/nakhonsawan_places.csv")


def get_place_coords(df: pd.DataFrame, place_name: str):
    row = df[df["name"] == place_name].iloc[0]
    return row["lat"], row["lon"]


# เก็บไว้ก่อน เผื่อต้องใช้ route mock สำรอง
def build_route_variants(origin: str, destination: str):
    routes = {
        ("โรงเรียนสตรีนครสวรรค์", "เซ็นทรัลนครสวรรค์"): {
            "fastest": [
                [100.1372, 15.7047],
                [100.1358, 15.7064],
                [100.1318, 15.7072],
                [100.1270, 15.7060],
                [100.1238, 15.7032],
                [100.1224, 15.6985],
            ],
            "cheapest": [
                [100.1372, 15.7047],
                [100.1360, 15.7036],
                [100.1330, 15.7010],
                [100.1290, 15.7000],
                [100.1250, 15.6990],
                [100.1224, 15.6985],
            ],
            "balanced": [
                [100.1372, 15.7047],
                [100.1350, 15.7060],
                [100.1305, 15.7070],
                [100.1260, 15.7055],
                [100.1238, 15.7025],
                [100.1224, 15.6985],
            ],
        },
        ("เซ็นทรัลนครสวรรค์", "โรงเรียนสตรีนครสวรรค์"): {
            "fastest": [
                [100.1224, 15.6985],
                [100.1238, 15.7032],
                [100.1270, 15.7060],
                [100.1318, 15.7072],
                [100.1358, 15.7064],
                [100.1372, 15.7047],
            ],
            "cheapest": [
                [100.1224, 15.6985],
                [100.1250, 15.6990],
                [100.1290, 15.7000],
                [100.1330, 15.7010],
                [100.1360, 15.7036],
                [100.1372, 15.7047],
            ],
            "balanced": [
                [100.1224, 15.6985],
                [100.1238, 15.7025],
                [100.1260, 15.7055],
                [100.1305, 15.7070],
                [100.1350, 15.7060],
                [100.1372, 15.7047],
            ],
        },
    }

    return routes.get((origin, destination), None)


def build_fallback_variants(start_lat, start_lon, end_lat, end_lon):
    fastest = [
        [start_lon, start_lat],
        [(start_lon * 2 + end_lon) / 3, (start_lat * 2 + end_lat) / 3 + 0.002],
        [(start_lon + end_lon * 2) / 3, (start_lat + end_lat * 2) / 3 + 0.001],
        [end_lon, end_lat],
    ]
    cheapest = [
        [start_lon, start_lat],
        [(start_lon * 2 + end_lon) / 3 - 0.002, (start_lat * 2 + end_lat) / 3 - 0.001],
        [(start_lon + end_lon * 2) / 3 - 0.001, (start_lat + end_lat * 2) / 3 - 0.002],
        [end_lon, end_lat],
    ]
    balanced = [
        [start_lon, start_lat],
        [(start_lon * 2 + end_lon) / 3, (start_lat * 2 + end_lat) / 3 + 0.001],
        [(start_lon + end_lon * 2) / 3, (start_lat + end_lat * 2) / 3 - 0.001],
        [end_lon, end_lat],
    ]

    return {
        "fastest": fastest,
        "cheapest": cheapest,
        "balanced": balanced,
    }


def calculate_path_distance_km(path):
    total = 0.0
    for i in range(len(path) - 1):
        lon1, lat1 = path[i]
        lon2, lat2 = path[i + 1]
        dx = (lon2 - lon1) * 111 * math.cos(math.radians((lat1 + lat2) / 2))
        dy = (lat2 - lat1) * 111
        total += math.sqrt(dx**2 + dy**2)
    return round(total, 1)


def build_route_metrics_from_variants(route_variants):
    speed_profiles = {
        "fastest": 42,
        "cheapest": 30,
        "balanced": 36,
    }

    fuel_rate_profiles = {
        "fastest": 2.4,
        "cheapest": 2.0,
        "balanced": 2.2,
    }

    traffic_profiles = {
        "fastest": "ปานกลาง",
        "cheapest": "จราจรดี",
        "balanced": "สมดุล",
    }

    route_names = {
        "fastest": "🔵 เร็วที่สุด",
        "cheapest": "🟢 ประหยัดที่สุด",
        "balanced": "🟠 แนะนำที่สุด",
    }

    rows = []

    for key in ["fastest", "cheapest", "balanced"]:
        path = route_variants[key]
        distance_km = calculate_path_distance_km(path)
        avg_speed = speed_profiles[key]
        time_min = round((distance_km / avg_speed) * 60)
        fuel_cost_baht = round(distance_km * fuel_rate_profiles[key])

        rows.append({
            "route_key": key,
            "route_name": route_names[key],
            "time_min": time_min,
            "distance_km": distance_km,
            "fuel_cost_baht": fuel_cost_baht,
            "traffic_status": traffic_profiles[key],
            "path": path,
        })

    return rows