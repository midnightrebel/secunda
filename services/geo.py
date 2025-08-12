def normalize_bounds(lat1: float, lon1: float, lat2: float, lon2: float):
    min_lat = min(lat1, lat2)
    max_lat = max(lat1, lat2)
    min_lon = min(lon1, lon2)
    max_lon = max(lon1, lon2)
    return min_lat, min_lon, max_lat, max_lon
