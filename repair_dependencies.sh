#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="/users/kennethdallmier/cathedral_engine"
cd "$REPO_ROOT"

# Locate the most recent quarantine folder from Phase 5
LATEST_QUARANTINE=$(ls -td 04_pipeline_tools/maintenance/quarantine/root_migration_* 2>/dev/null | head -n 1)

if [ -z "$LATEST_QUARANTINE" ] || [ ! -d "$LATEST_QUARANTINE" ]; then
    echo "❌ Error: Could not locate Phase 5 quarantine directory."
    exit 1
fi

echo "=== Recovering GDScript dependencies from $LATEST_QUARANTINE ==="

# 1. Recover master_view and character_select scripts to 03_godot_client/scripts/
mkdir -p "03_godot_client/scripts"
if [ -d "$LATEST_QUARANTINE/scripts" ]; then
    cp -n "$LATEST_QUARANTINE/scripts/"*.gd* "03_godot_client/scripts/"
    echo "✓ Recovered character & resonance scripts into 03_godot_client/scripts/"
fi

# 2. Recover Heart-Oculus scripts to 03_godot_client/
if [ -d "$LATEST_QUARANTINE/Code/GDScripts" ]; then
    cp -n "$LATEST_QUARANTINE/Code/GDScripts/heart-oculus-"*.gd* "03_godot_client/scripts/"
    # Symlink to 03_godot_client root for res://heart-oculus-*.gd resolution
    for f in 03_godot_client/scripts/heart-oculus-*.gd; do
        [ -e "$f" ] && ln -sfn "scripts/$(basename "$f")" "03_godot_client/$(basename "$f")"
    done
    echo "✓ Recovered heart-oculus scripts into 03_godot_client/"
fi

# 3. Patch spatial_triad_demo_scene.tscn path prefix
SCENE_PATH="03_godot_client/scenes/spatial_triad_demo_scene.tscn"
if [ -f "$SCENE_PATH" ]; then
    sed -i '' 's|res://03_godot_client/scripts/AtlasAnimator.gd|res://scripts/AtlasAnimator.gd|g' "$SCENE_PATH"
    echo "✓ Normalized res:// path in spatial_triad_demo_scene.tscn"
fi

# 4. Patch game_loop_engine.py with dual import fallback
GAME_LOOP="02_engine_core/logic_engines/game_loop_engine.py"
if [ -f "$GAME_LOOP" ]; then
    python3 - << 'PYEOF'
import re

path = "02_engine_core/logic_engines/game_loop_engine.py"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_block = """from .paraconsistent_engine import EAS03ParaconsistentEngine
from .emotional_physics_engine import EmotionalPhysicsEngine
from .arcana_engine import ArcanaEngine
from .enemy_engine import EnemyEngine, EnemyInstance, EnemySpectrum
from .dialogue_engine import DialogueEngine
from .progression_engine import ProgressionEngine
from .campaign_engine import CampaignEngine"""

new_block = """try:
    from .paraconsistent_engine import EAS03ParaconsistentEngine
    from .emotional_physics_engine import EmotionalPhysicsEngine
    from .arcana_engine import ArcanaEngine
    from .enemy_engine import EnemyEngine, EnemyInstance, EnemySpectrum
    from .dialogue_engine import DialogueEngine
    from .progression_engine import ProgressionEngine
    from .campaign_engine import CampaignEngine
except (ImportError, ValueError):
    from paraconsistent_engine import EAS03ParaconsistentEngine
    from emotional_physics_engine import EmotionalPhysicsEngine
    from arcana_engine import ArcanaEngine
    from enemy_engine import EnemyEngine, EnemyInstance, EnemySpectrum
    from dialogue_engine import DialogueEngine
    from progression_engine import ProgressionEngine
    from campaign_engine import CampaignEngine"""

if old_block in content:
    content = content.replace(old_block, new_block)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("✓ Added dual-import fallback to game_loop_engine.py")
else:
    print("⚠️ game_loop_engine.py import block already modified or differed.")
PYEOF
fi

# 5. Backward compatibility symlink for legacy 'engines' package callers
ln -sfn 02_engine_core/logic_engines engines
echo "✓ Ensured backward-compatibility symlink: engines -> 02_engine_core/logic_engines"

echo "=== Running Dependency Verification Audit ==="
python3 /users/kennethdallmier/cathedral_engine/verify_dependencies.py
