from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, HttpUrl, confloat, constr


class AttachmentModel(BaseModel):
    filename: constr(strip_whitespace=True, max_length=255)
    mime_type: Optional[str] = None
    storage_type: Optional[str] = Field(
        None, description="local, s3, gcs, azure_blob, etc."
    )
    storage_path: Optional[str] = None
    storage_bucket: Optional[str] = None
    storage_object_key: Optional[str] = None
    storage_url: Optional[HttpUrl] = None
    storage_meta: Optional[Dict[str, Any]] = None
    caption: Optional[str] = None
    file_size_bytes: Optional[int] = None
    uploaded_by: Optional[str] = None


class AnswerModel(BaseModel):
    key: constr(strip_whitespace=True, max_length=150)
    question_text: str
    value_text: Optional[str] = None
    value_numeric: Optional[confloat(ge=-1e12, le=1e12)] = None
    value_boolean: Optional[bool] = None
    value_json: Optional[Dict[str, Any]] = None
    answer_order: Optional[int] = 0
    qc_flag: Optional[str] = None
    note: Optional[str] = None


class SampleModel(BaseModel):
    external_id: Optional[str] = None
    plugin_id: Optional[str] = None
    plugin_version: Optional[str] = None

    name: Optional[str] = None
    description: Optional[str] = None
    sample_date: datetime

    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    street_address: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    country_code: Optional[str] = Field(None, min_length=2, max_length=2)

    organization_id: Optional[int] = None
    collector_id: Optional[str] = None
    collector_name: Optional[str] = None

    answers: List[AnswerModel] = []
    attachments: List[AttachmentModel] = []
    attributes: Optional[Dict[str, Any]] = {}
    raw_payload: Optional[Dict[str, Any]] = None

    class Config:
        extra = "allow"  # tolerate plugins sending extra fields
