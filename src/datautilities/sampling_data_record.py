from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class AttachmentPayload:
    filename: str
    mime_type: Optional[str] = None
    # plugin may store either local path or bucket/key or url
    storage_type: Optional[str] = None  # 'local' | 's3' | 'gcs' | ...
    storage_path: Optional[str] = None
    storage_bucket: Optional[str] = None
    storage_object_key: Optional[str] = None
    storage_url: Optional[str] = None
    storage_meta: Dict[str, Any] = field(default_factory=dict)
    caption: Optional[str] = None
    file_size_bytes: Optional[int] = None
    uploaded_by: Optional[str] = None


@dataclass
class AnswerPayload:
    key: str  # canonical question key like "q1_depth"
    question_text: str  # original question prompt (full text)
    value_text: Optional[str] = None
    value_numeric: Optional[float] = None
    value_boolean: Optional[bool] = None
    value_json: Optional[Dict[str, Any]] = None
    answer_order: Optional[int] = None
    qc_flag: Optional[str] = None
    note: Optional[str] = None


@dataclass
class SamplePayload:
    # metadata
    external_id: Optional[str] = None  # plugin-provided id for idempotency
    plugin_id: Optional[str] = None  # which plugin produced this
    plugin_version: Optional[str] = None

    # sample core
    name: Optional[str] = None
    description: Optional[str] = None
    sample_date: Optional[datetime] = None

    # location (plugin may return address or lat/lon)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    street_address: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    country_code: Optional[str] = None
    the_geom_wkt: Optional[str] = None  # if plugin returns WKT

    # organization context
    organization_id: Optional[int] = None

    # collector / source
    collector_id: Optional[str] = None
    collector_name: Optional[str] = None

    # answers & attachments
    answers: List[AnswerPayload] = field(default_factory=list)
    attachments: List[AttachmentPayload] = field(default_factory=list)

    # raw plugin payload for audit: keep full JSON if needed
    raw_payload: Optional[Dict[str, Any]] = None

    # optional attributes bag for quick storage
    attributes: Dict[str, Any] = field(default_factory=dict)
