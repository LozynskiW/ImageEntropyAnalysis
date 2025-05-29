from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True)
class GeoLocalizationData:
    x: float | None
    y: float | None
    z: float | None
    time_s: float | None
    barometric_height: float | None
    gps_height: float | None
    pitch: float | None
    roll: float | None
    yaw: float | None
    image_identifier: str
