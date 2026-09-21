# ECHO Unity Client

Unity 6 LTS + URP vertical slice for the ECHO mobile RPG.

## Open

1. Open Unity Hub.
2. Add the `unity/` folder as an existing project.
3. Open `Assets/Scenes/Bootstrap.unity`.
4. Press Play.

The scene builds a stylized placeholder hub/zone at runtime so no binary art assets are required yet.

Character GLB files from `docs/images/*/Meshy_AI_model.glb` and `docs/images/icon/hero_3D.glb` are copied into `Assets/StreamingAssets/Characters/` and loaded with glTFast at runtime. `hero_3D.glb` is preferred as the player visual; the capsule remains as a fallback if a model cannot load. World/NPC/prop/weapon GLBs are cataloged in `Assets/StreamingAssets/World/catalog.json`.

## Controls

- Editor: `WASD` or arrow keys to move, `Space` to attack.
- Mobile: use the left joystick and the attack button.
- Walk to the glowing discovery marker to create a Memory and trigger the Echo state.

## Backend

The client targets `http://127.0.0.1:8000` by default. It checks `/health` and exposes the OAuth start flow through the login button. The FastAPI OAuth callback is currently a backend stub, so development mode keeps a local fallback session.

## Design mapping

- 3/4 camera with follow lag and bounded distance.
- Hub/zone vertical slice with readable silhouettes.
- Personal Memory scrapbook card and Echo alert.
- Mobile safe-area HUD, joystick, contextual attack action.
- Placeholder colors are intentionally easy to replace once design images are added.
