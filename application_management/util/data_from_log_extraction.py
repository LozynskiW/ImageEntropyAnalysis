def standard_schema(log, num):
    if log[10][num] is None:
        raise AttributeError
    try:
        return {
            "time": log[0][num],
            "longitude": float(log[1][num]),
            "latitude": float(log[2][num]),
            "gps_height": float(log[3][num]),
            "barometric_height": float(log[4][num]),
            "pitch": float(log[5][num]),
            "roll": float(log[6][num]),
            "yaw": float(log[7][num]),
            "gps_speed": float(log[8][num]),
            "gps_course": float(log[9][num])
        }
    except ValueError:
        return None