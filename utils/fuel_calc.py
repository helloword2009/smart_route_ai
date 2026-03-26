def estimate_fuel_cost(distance_km: float, fuel_efficiency_km_per_liter: float, fuel_price: float) -> float:
    if fuel_efficiency_km_per_liter <= 0:
        return 0.0
    liters_used = distance_km / fuel_efficiency_km_per_liter
    return liters_used * fuel_price