import os
import json
from openai import OpenAI
from app.schemas import AdaptationRequest

ADAPTATION_PROMPT = """
You are an award-winning Indian cinematic dialogue adapter and dramaturg.
Adapt the provided scenes to the specified culture and dialect.
DO NOT provide a simple word translation.
You must:
1. Rewrite dialogue using authentic dialect syntax, idioms, and code-switching.
2. Adapt non-verbal action: posture, touching feet, eye contact, seating hierarchy.
3. Replace food, props, and architectural nuances to match the exact rural/urban setting.
4. Keep the core dramatic conflict intact.
"""

def adapt_screenplay(req: AdaptationRequest) -> dict:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    payload = {
        "scenes": [s.model_dump() for s in req.scenes],
        "characters": [c.model_dump() for c in req.characters],
        "costumes": [ct.model_dump() for ct in req.costumes],
        "culture_plan": req.culture_plan.model_dump()
    }
    
    prompt = f"{ADAPTATION_PROMPT}\n\nINPUT DATA:\n{json.dumps(payload)}\n\nOutput JSON with key 'adapted_scenes' containing an array of adapted scenes with: scene_id, adapted_header, adapted_action, adapted_dialogue, cultural_notes."
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": ADAPTATION_PROMPT},
            {"role": "user", "content": prompt}
        ]
    )
    
    return json.loads(response.choices[0].message.content)