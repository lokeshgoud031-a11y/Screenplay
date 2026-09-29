import os
import httpx
from app.schemas import CanonicalCharacter

REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

async def generate_character_bible_image(char: CanonicalCharacter) -> str:
    if not REPLICATE_API_TOKEN or REPLICATE_API_TOKEN == "your_replicate_api_key_here":
        return f"https://placehold.co/600x800/png?text={char.canonical_id}+{char.adapted_name}"
    
    headers = {"Authorization": f"Token {REPLICATE_API_TOKEN}", "Content-Type": "application/json"}
    payload = {
        "version": "black-forest-labs/flux-schnell",
        "input": {"prompt": f"Cinematic portrait of {char.face_seed_prompt}", "aspect_ratio": "3:4"}
    }
    async with httpx.AsyncClient() as client:
        res = await client.post("https://api.replicate.com/v1/predictions", json=payload, headers=headers)
        return res.json().get("urls", {}).get("get", "")