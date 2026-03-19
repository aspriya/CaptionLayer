from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class Timing(BaseModel):
    start: float = Field(..., description="Start time in seconds")
    end: float = Field(..., description="End time in seconds")
    duration: float = Field(..., description="Duration in seconds")

class WordStyle(BaseModel):
    is_emphasized: bool = Field(default=False)
    color: Optional[str] = Field(default=None)
    custom_attrs: Dict[str, Any] = Field(default_factory=dict)

class Word(BaseModel):
    text: str = Field(..., description="The word text")
    timing: Timing
    confidence: Optional[float] = Field(default=None, description="ASR or alignment confidence")
    style: Optional[WordStyle] = Field(default_factory=WordStyle)

class SegmentStyle(BaseModel):
    speaker: Optional[str] = Field(default=None)
    position: Optional[str] = Field(default="bottom")
    preset_name: Optional[str] = Field(default=None)
    custom_attrs: Dict[str, Any] = Field(default_factory=dict)

class Segment(BaseModel):
    id: str = Field(..., description="Unique identifier for the segment")
    text: str = Field(..., description="Full text of the segment")
    words: List[Word] = Field(default_factory=list, description="Words contained in this segment")
    timing: Timing
    style: Optional[SegmentStyle] = Field(default_factory=SegmentStyle)

class SourceAssetMetadata(BaseModel):
    filename: str
    duration: Optional[float] = None
    format: Optional[str] = None
    audio_channels: Optional[int] = None
    sample_rate: Optional[int] = None

class ProcessingProvenance(BaseModel):
    asr_model: Optional[str] = None
    alignment_model: Optional[str] = None
    segmentation_method: Optional[str] = None
    processed_at: datetime = Field(default_factory=datetime.now)

class ProjectMetadata(BaseModel):
    project_id: str
    name: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class CanonicalTimeline(BaseModel):
    version: str = Field(default="1.0.0", description="Schema version")
    project_metadata: ProjectMetadata
    source_metadata: SourceAssetMetadata
    transcript: str = Field(..., description="Full transcript text")
    segments: List[Segment] = Field(default_factory=list, description="Caption segments")
    provenance: ProcessingProvenance = Field(default_factory=ProcessingProvenance)
