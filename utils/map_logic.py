from __future__ import annotations

from typing import Any, Dict, List, Optional, Set, Tuple

import pandas as pd
import requests
import streamlit as st


ORS_DIRECTIONS_URL = "https://api.openrouteservice.org/v2/directions/driving-car"


def load_places() -> pd.DataFrame:
    return pd.read_csv("data/nakhonsawan_places.csv", encoding="utf-8-sig")


def get_place_coords(df: pd.DataFrame, place_name: str) -> Tuple[float, float]:
    row = df[df["name"] == place_name].iloc[0]
    return float(row["lat"]), float(row["lon"])


def _traffic_status(time_min: float) -> str:
    if time_min < 15:
        return "จราจรดี"
    if time_min < 25:
        return "ปานกลาง"
    return "หนาแน่น"


def _route_payload(
    start_lat: float,
    start_lon: float,
    end_lat: float,
    end_lon: float,
    *,
    preference: str = "recommended",
    alternative_routes: Optional[Dict[str, Any]] = None,
    avoid_features: Optional[List[str]] = None,
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "coordinates": [
            [start_lon, start_lat],
            [end_lon, end_lat],
        ],
        "preference": preference,
        "instructions": False,
        "geometry_simplify": False,
    }

    if alternative_routes:
        payload["alternative_routes"] = alternative_routes

    if avoid_features:
        payload["options"] = {"avoid_features": avoid_features}

    return payload


def _call_ors(payload: Dict[str, Any]) -> Dict[str, Any]:
    api_key = st.secrets["ORS_API_KEY"]
    headers = {
        "Authorization": api_key,
        "Accept": "application/json, application/geo+json",
        "Content-Type": "application/json",
    }

    response = requests.post(
        ORS_DIRECTIONS_URL,
        params={"format": "geojson"},
        json=payload,
        headers=headers,
        timeout=20,
    )
    response.raise_for_status()
    return response.json()


def _decode_polyline(encoded: str) -> List[List[float]]:
    coordinates: List[List[float]] = []
    index = 0
    lat = 0
    lon = 0

    while index < len(encoded):
        shift = 0
        result = 0
        while True:
            byte = ord(encoded[index]) - 63
            index += 1
            result |= (byte & 0x1F) << shift
            shift += 5
            if byte < 0x20:
                break
        lat += ~(result >> 1) if result & 1 else result >> 1

        shift = 0
        result = 0
        while True:
            byte = ord(encoded[index]) - 63
            index += 1
            result |= (byte & 0x1F) << shift
            shift += 5
            if byte < 0x20:
                break
        lon += ~(result >> 1) if result & 1 else result >> 1

        coordinates.append([lon / 1e5, lat / 1e5])

    return coordinates


def _extract_route_features(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    if data.get("features"):
        return data["features"]

    features: List[Dict[str, Any]] = []
    for route in data.get("routes", []):
        geometry = route.get("geometry")
        if isinstance(geometry, str):
            geometry = {
                "type": "LineString",
                "coordinates": _decode_polyline(geometry),
            }

        features.append(
            {
                "type": "Feature",
                "geometry": geometry,
                "properties": {
                    "summary": route.get("summary", {}),
                },
            }
        )

    return features


def _build_route_row(feature: Dict[str, Any], route_key: str, route_name: str) -> Dict[str, Any]:
    summary = feature["properties"]["summary"]
    distance_km = round(summary["distance"] / 1000, 1)
    time_min = round(summary["duration"] / 60)

    return {
        "route_key": route_key,
        "route_name": route_name,
        "distance_km": distance_km,
        "time_min": time_min,
        "fuel_cost_baht": round(distance_km * 2.2),
        "traffic_status": _traffic_status(time_min),
        "path": feature["geometry"]["coordinates"],
    }


def _dedupe_routes(routes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    unique_routes: List[Dict[str, Any]] = []
    seen_signatures: Set[Tuple[float, float]] = set()

    for route in routes:
        signature = (route["distance_km"], route["time_min"])
        if signature in seen_signatures:
            continue
        seen_signatures.add(signature)
        unique_routes.append(route)

    return unique_routes


def get_route_options(start_lat: float, start_lon: float, end_lat: float, end_lon: float) -> pd.DataFrame:
    candidate_routes: List[Dict[str, Any]] = []

    primary_payload = _route_payload(
        start_lat,
        start_lon,
        end_lat,
        end_lon,
        preference="recommended",
        alternative_routes={
            "target_count": 2,
            "weight_factor": 1.6,
            "share_factor": 0.6,
        },
    )

    primary_data = _call_ors(primary_payload)
    features = _extract_route_features(primary_data)

    for index, feature in enumerate(features):
        if index == 0:
            candidate_routes.append(_build_route_row(feature, "balanced", "แนะนำที่สุด"))
        elif index == 1:
            candidate_routes.append(_build_route_row(feature, "fastest", "เร็วที่สุด"))
        else:
            candidate_routes.append(_build_route_row(feature, "cheapest", "ประหยัดที่สุด"))

    fallback_requests = [
        ("fastest", "เร็วที่สุด", _route_payload(start_lat, start_lon, end_lat, end_lon, preference="fastest")),
        ("cheapest", "ประหยัดที่สุด", _route_payload(start_lat, start_lon, end_lat, end_lon, preference="shortest")),
        (
            "balanced",
            "แนะนำที่สุด",
            _route_payload(
                start_lat,
                start_lon,
                end_lat,
                end_lon,
                preference="recommended",
                avoid_features=["highways"],
            ),
        ),
    ]

    existing_keys = {route["route_key"] for route in candidate_routes}
    for route_key, route_name, payload in fallback_requests:
        if route_key in existing_keys:
            continue
        fallback_data = _call_ors(payload)
        fallback_features = _extract_route_features(fallback_data)
        if not fallback_features:
            continue
        candidate_routes.append(_build_route_row(fallback_features[0], route_key, route_name))

    routes = _dedupe_routes(candidate_routes)
    priority = {"balanced": 0, "fastest": 1, "cheapest": 2}
    routes.sort(key=lambda row: priority.get(row["route_key"], 99))

    return pd.DataFrame(routes)
