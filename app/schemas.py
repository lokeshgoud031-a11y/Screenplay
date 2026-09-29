from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class CanonicalCharacter(BaseModel):
    canonical_id: str
    source_names_and_aliases: List[str]
    adapted_name: str
    age: int
    gender: str
    kinship_role: str
    sociocultural_role: str
    face_seed_prompt: str
    costume_id: Optional[str] = None
    inventory: List[str] = Field(default_factory=list)

class CanonicalCostume(BaseModel):
    costume_id: str
    character_id: str
    garments: str
    fabric: str
    color_palette: List[str]
    footwear: str
    headwear_grooming: str
    scenes_worn: List[str] = Field(default_factory=list)
    image_url: Optional[str] = None

class SceneRecord(BaseModel):
    scene_id: str
    scene_order: int
    header: str
    int_ext: str
    location_id: str
    time_of_day: str
    atmosphere: str
    characters_present: List[str]
    costume_assignments: Dict[str, str]
    props_brought_in: List[str]
    props_left_with: List[str]
    dramatic_purpose: str
    emotional_shift: str
    continuity_warnings: List[str] = Field(default_factory=list)

class AdaptationPlan(BaseModel):
    target_culture: str
    dialect: str
    region_milieu: str
    setting_type: str
    output_script: str
    kinship_rules: Dict[str, str]
    idiomatic_shifts: Dict[str, str]
    gesture_rules: List[str]
    cultural_justification: str

class ExtractionResponse(BaseModel):
    scenes: List[SceneRecord]
    characters: List[CanonicalCharacter]
    costumes: List[CanonicalCostume]
    continuity_warnings: List[str]

class AdaptationRequest(BaseModel):
    scenes: List[SceneRecord]
    characters: List[CanonicalCharacter]
    costumes: List[CanonicalCostume]
    culture_plan: AdaptationPlan