import pandas as pd
import random


def simulate_routes(origin: str, destination: str) -> pd.DataFrame:
    base_time = random.randint(12, 20)
    base_distance = random.uniform(7, 12)

    routes = [
        {
            "route_name": "เส้นทาง A",
            "time_min": base_time,
            "distance_km": base_distance,
        },
        {
            "route_name": "เส้นทาง B",
            "time_min": base_time - random.randint(1, 3),
            "distance_km": base_distance + random.uniform(0.5, 1.5),
        },
        {
            "route_name": "เส้นทาง C",
            "time_min": base_time + random.randint(1, 3),
            "distance_km": base_distance - random.uniform(0.5, 1.5),
        },
    ]

    df = pd.DataFrame(routes)

    # คำนวณค่าน้ำมัน (ง่าย ๆ)
    df["fuel_cost_baht"] = df["distance_km"] * 2.2
    df["traffic_status"] = df["time_min"].apply(
        lambda x: "จราจรดี" if x < 15 else "ปานกลาง" if x < 18 else "หนาแน่น"
    )

    return df


def get_best_routes(df: pd.DataFrame) -> dict:
    fastest = df.loc[df["time_min"].idxmin()]
    cheapest = df.loc[df["fuel_cost_baht"].idxmin()]
    balanced = df.loc[(df["time_min"] + df["fuel_cost_baht"]).idxmin()]

    return {
        "fastest": fastest,
        "cheapest": cheapest,
        "balanced": balanced
    }