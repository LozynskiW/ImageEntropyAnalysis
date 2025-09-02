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

    def to_dict(self) -> dict:
        return {
            "x": self.x,
            "y": self.y,
            "z": self.z,
            "time_s": self.time_s,
            "barometric_height": self.barometric_height,
            "gps_height": self.gps_height,
            "pitch": self.pitch,
            "roll": self.roll,
            "yaw": self.yaw
        }
