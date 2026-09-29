import os
import json
from openai import OpenAI
from app.schemas import ExtractionResponse, SceneRecord, CanonicalCharacter, CanonicalCostume
from app.continuity import ContinuityEngine

EXTRACTION_SYSTEM_PROMPT = """
You are an expert Hollywood/Indian Script Continuity Supervisor.
Extract the screenplay into structured JSON conforming to the requested schema.
CRITICAL RULES:
1. Merge character aliases into ONE CanonicalCharacter record (e.g. 'Amar', 'A. Singh', 'elder son' -> one ID).
2. Reuse costume_ids across scenes unless there is a story-driven wardrobe change.
3. Track props entered and exited for every scene.
"""

def extract_screenplay(raw_text: str) -> ExtractionResponse:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"{EXTRACTION_SYSTEM_PROMPT}\n\nSCREENPLAY:\n{raw_text}\n\nReturn JSON with keys: scenes, characters, costumes."
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": EXTRACTION_SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    )
    
    data = json.loads(response.choices[0].message.content)

    scenes = [SceneRecord(**s) for s in data.get("scenes", [])]
    characters = [CanonicalCharacter(**c) for c in data.get("characters", [])]
    costumes = [CanonicalCostume(**ct) for ct in data.get("costumes", [])]

    audit_warnings = ContinuityEngine.audit_continuity(scenes, characters)
    
    return ExtractionResponse(
        scenes=scenes,
        characters=characters,
        costumes=costumes,
        continuity_warnings=audit_warnings
    )