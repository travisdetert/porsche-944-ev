# 3D car models (optional)

Drop a glTF model here as **`944.glb`** and the **CAR** tab loads it automatically — auto-fit
and centered — falling back to the built-in primitive 944 if it's absent.

## Suggested model
Sketchfab — **"1991 Porsche 944 Turbo"**:
https://sketchfab.com/3d-models/1991-porsche-944-turbo-570249cd14c342ea947b05fee05245d9

## How to add it
1. Open the link and **check the LICENSE** — respect the author's terms / attribution.
2. **Download** (needs a free Sketchfab account). Choose **glTF Binary (.glb)** if offered;
   otherwise download the glTF `.zip` and export/convert to a single `944.glb`
   (e.g. open in Blender → Export → glTF Binary).
3. Save it here as **`app/frontend/models/944.glb`**.
4. **Refresh** the CAR tab.

## Notes
- Model files are **gitignored** — don't commit someone else's licensed asset to the repo.
  Keep the author's attribution with the model per its license.
- The pop-up-light toggle and glow effects are wired to the **built-in** primitive; a downloaded
  model shows as-is (its own lights). Mapping effects to a real model's parts is a later step.
