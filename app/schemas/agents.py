"""
Agent I/O Schemas — Pydantic models defining the contracts
between agents and pipeline stages.

These schemas are the "external contracts" of the system.
Backward compatibility is strictly maintained.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


# --- Visual / Scene Schemas ---

class VisualPrompt(BaseModel):
    """Per-timing visual generation prompt."""
    timing: str
    prompt: str
    caption: str = ""
    caption_position: str = "bottom"


class VideoScenePrompt(BaseModel):
    """Scene-level video generation prompt for the media pipeline."""
    scene_id: str
    purpose: str
    prompt: str
    duration_hint_sec: float = Field(gt=0)


# --- Scoring Schemas ---

class TopicScore(BaseModel):
    topic: str
    score: float
    reason: str = ""


# --- SEO & Marketing Schemas ---

class SeoPackage(BaseModel):
    title: str
    description: str
    tags: list[str]
    hashtags: list[str]


class ProductInfo(BaseModel):
    name: str
    one_liner: str
    link: str = ""


class MarketingData(BaseModel):
    summary: str = ""
    guide_content: list[str] = Field(default_factory=list)
    comparison: list[dict[str, Any]] = Field(default_factory=list)
    checkpoints: list[str] = Field(default_factory=list)
    products: list[ProductInfo] = Field(default_factory=list)


# --- Core Entity Schemas ---

class ScriptBase(BaseModel):
    idea_id: int
    hook: str
    body: list[str]
    cta: str
    estimated_duration: int = 0
    template_type: str | None = None
    visuals: list[VisualPrompt] | None = None
    video_scene_prompts: list[VideoScenePrompt] | None = None
    seo_data: SeoPackage | None = None
    marketing_data: MarketingData | None = None
    operational_metadata: dict[str, Any] | None = None


class ScriptPackageOutput(ScriptBase):
    """
    The immutable output contract from ScriptAgent → MediaPipeline.

    This is the most critical schema in the system. All downstream
    consumers (media pipeline, upload packager, analytics) depend
    on this shape. Changes require full downstream impact analysis.
    """
    pass


class Script(ScriptBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ScriptRequest(BaseModel):
    """Input to the Script Agent."""
    idea_id: int
    topic: str
    grade: str = "C"
    template_type: str = "A"
    context: dict[str, Any] = Field(default_factory=dict)


# --- Topic / Idea Schemas ---

class IdeaBase(BaseModel):
    text: str
    score: float = 0.0
    status: str = "suggested"


class Idea(IdeaBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CandidateSource(BaseModel):
    """Where a topic candidate originated."""
    collector: str  # e.g., "news", "youtube", "reddit", "trends"
    url: str = ""
    collected_at: datetime | None = None


class CandidateItem(BaseModel):
    """A single topic candidate from ingestion."""
    topic: str
    source: CandidateSource
    raw_score: float = 0.0
    metadata: dict[str, Any] = Field(default_factory=dict)


class CandidateInput(BaseModel):
    """Batch input for the ingest pipeline."""
    candidates: list[CandidateItem]
    ingest_mode: str = "auto"
