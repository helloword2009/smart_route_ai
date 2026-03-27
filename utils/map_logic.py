import pandas as pd
import requests
import streamlit as st


def load_places() -> pd.DataFrame:
    return pd.read_csv("data/nakhonsawan_places.csv")


def get_place_coords(df: pd.DataFrame, place_name: str):
    row = df[df["name"] == place_name].iloc[0]
    return row["lat"], row["lon"]


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
    response.raise_for_status()
    data = response.json()

    coords = data["features"][0]["geometry"]["coordinates"]
    summary = data["features"][0]["properties"]["summary"]

    return {
        "path": coords,
        "distance_km": round(summary["distance"] / 1000, 1),
        "time_min": round(summary["duration"] / 60),
    }