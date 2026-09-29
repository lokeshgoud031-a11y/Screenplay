from typing import List, Dict
from app.schemas import SceneRecord, CanonicalCharacter

class ContinuityEngine:
    @staticmethod
    def audit_continuity(scenes: List[SceneRecord], characters: List[CanonicalCharacter]) -> List[str]:
        warnings = []
        prop_carrier_tracker: Dict[str, str] = {}
        last_costumes: Dict[str, str] = {}

        sorted_scenes = sorted(scenes, key=lambda s: s.scene_order)

        for scene in sorted_scenes:
            for prop in scene.props_brought_in:
                if prop not in prop_carrier_tracker and scene.scene_order > 1:
                    warnings.append(
                        f"Scene {scene.scene_id}: Prop '{prop}' introduced without preceding acquisition origin."
                    )
            
            for prop in scene.props_left_with:
                prop_carrier_tracker[prop] = scene.scene_id

            for char_id, cost_id in scene.costume_assignments.items():
                if char_id in last_costumes:
                    if last_costumes[char_id] != cost_id and "later" not in scene.time_of_day.lower() and "next day" not in scene.time_of_day.lower():
                        warnings.append(
                            f"Scene {scene.scene_id}: Character '{char_id}' changed costume from {last_costumes[char_id]} to {cost_id} within continuous story time without explanation."
                        )
                last_costumes[char_id] = cost_id
                
        return warnings