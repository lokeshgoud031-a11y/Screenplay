Set-Content tests\test_engine.py @"
import pytest
from app.schemas import SceneRecord, CanonicalCharacter
from app.continuity import ContinuityEngine

def test_alias_normalization():
    char = CanonicalCharacter(
        canonical_id='CHAR_AMAR_01',
        source_names_and_aliases=['Amar', 'A. Singh', 'elder brother'],
        adapted_name='Amarjeet',
        age=32,
        gender='Male',
        kinship_role='Elder Son',
        sociocultural_role='Farmer',
        face_seed_prompt='Sikh male, mid 30s, sharp jawline'
    )
    assert 'A. Singh' in char.source_names_and_aliases
    assert char.canonical_id == 'CHAR_AMAR_01'

def test_continuity_engine_flags_disappearing_prop():
    scenes = [
        SceneRecord(
            scene_id='SC01',
            scene_order=1,
            header='INT. ROOM - DAY',
            int_ext='INT',
            location_id='LOC_ROOM',
            time_of_day='Day',
            atmosphere='Tense',
            characters_present=['CHAR_AMAR_01'],
            costume_assignments={'CHAR_AMAR_01': 'COST_01'},
            props_brought_in=['PROP_LETTER'],
            props_left_with=['PROP_LETTER'],
            dramatic_purpose='Set stakes',
            emotional_shift='Dread'
        ),
        SceneRecord(
            scene_id='SC02',
            scene_order=2,
            header='EXT. STREET - DAY',
            int_ext='EXT',
            location_id='LOC_STREET',
            time_of_day='Day',
            atmosphere='Hot',
            characters_present=['CHAR_AMAR_01'],
            costume_assignments={'CHAR_AMAR_01': 'COST_01'},
            props_brought_in=['PROP_GUN'],
            props_left_with=[],
            dramatic_purpose='Action',
            emotional_shift='Panic'
        )
    ]
    chars = []
    warnings = ContinuityEngine.audit_continuity(scenes, chars)
    assert len(warnings) > 0
    assert 'PROP_GUN' in warnings[0]
"@