import pandas as pd


def load_places() -> pd.DataFrame:
    return pd.read_csv("data/nakhonsawan_places.csv")


def get_place_coords(df: pd.DataFrame, place_name: str):
    row = df[df["name"] == place_name].iloc[0]
    return row["lat"], row["lon"]


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

    key = (origin, destination)
    return routes.get(key, None)


def build_fallback_variants(start_lat, start_lon, end_lat, end_lon):
    # route เร็วที่สุด
    fastest = [
        [start_lon, start_lat],
        [(start_lon * 2 + end_lon) / 3, (start_lat * 2 + end_lat) / 3 + 0.002],
        [(start_lon + end_lon * 2) / 3, (start_lat + end_lat * 2) / 3 + 0.001],
        [end_lon, end_lat],
    ]

    # route ประหยัดที่สุด
    cheapest = [
        [start_lon, start_lat],
        [(start_lon * 2 + end_lon) / 3 - 0.002, (start_lat * 2 + end_lat) / 3 - 0.001],
        [(start_lon + end_lon * 2) / 3 - 0.001, (start_lat + end_lat * 2) / 3 - 0.002],
        [end_lon, end_lat],
    ]

    # route แนะนำที่สุด
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