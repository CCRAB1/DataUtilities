from datetime import datetime

from pydantic import BaseModel


class PlatformDataRecord(BaseModel):
    organization: str
    platform_handle: str
    obs_type: str
    uom_type: str
    s_order: int
    value: float
    date_time: datetime
    latitude: float
    longitude: float
    altitude: float
