"""
Media Pipeline Models — Data contracts for the 5-stage pipeline.

Plan → Asset → Render → Package → Publish
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class BudgetTier(str, Enum):
    LOW = "LOW"
    MID = "MID"
    HIGH = "HIGH"


class SceneType(str, Enum):
    HOOK = "HOOK"
    EXPLAIN = "EXPLAIN"
    BROLL = "BROLL"
    CTA = "CTA"


class VisualTarget(str, Enum):
    VIDEO = "video"
    IMAGE = "image"


class ReasonCode(str, Enum):
    SUCCESS = "SUCCESS"
    BUDGET_EXCEEDED = "BUDGET_EXCEEDED"
    API_ERROR = "API_ERROR"
    VALIDATION_FAILED = "VALIDATION_FAILED"
    FALLBACK_IMAGE = "FALLBACK_IMAGE"
    RENDER_FAILED = "RENDER_FAILED"
    INTERNAL_ERROR = "INTERNAL_ERROR"


class Scene(BaseModel):
    scene_id: str
    type: SceneType
    prompt: str
    expected_sec: float = Field(gt=0)


class ToneProfile(BaseModel):
    """Visual tone consistency profile across all scenes."""
    palette: str
    lighting: str
    realism_level: str
    camera_style: str
    environment_density: str
    subject_style: str
    motion_energy: str
    summary: str = ""


class ScriptReadyPayload(BaseModel):
    """Input to the media pipeline from the orchestrator."""
    narration_text: str
    scenes: list[Scene]
    tone_profile: ToneProfile | None = None
    budget_tier: BudgetTier = BudgetTier.MID


class RenderResult(BaseModel):
    """Output of the render stage."""
    video_path: str
    duration_sec: float
    resolution: str = "1080x1920"
    reason_code: ReasonCode = ReasonCode.SUCCESS


class SceneReferencePolicy(str, Enum):
    """How to handle visual references across scenes."""
    NONE = "none"
    SHARE_TONE = "share_tone"
    SHARE_SUBJECT = "share_subject"
    FULL_CONTINUITY = "full_continuity"


class ReferenceBundle(BaseModel):
    """Cached visual references for scene consistency."""
    tone_profile: ToneProfile
    policy: SceneReferencePolicy = SceneReferencePolicy.SHARE_TONE
    reference_images: list[str] = Field(default_factory=list)
