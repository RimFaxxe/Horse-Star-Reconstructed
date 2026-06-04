# Horse Star - Asset Bundle Analysis Findings

## Overview

This document consolidates all findings from analyzing Horse Star's `.unity3d` asset bundles. Everything here comes from real data - bundle binaries and DLL analysis - not guesswork.

**Current progress:** around 110 of roughly 1087 bundles analyzed.

---

## Bundle Format

All recovered bundles share the same format:

- **Container:** `UnityWeb` (LZMA compressed)
- **Unity version:** `3.1.0f4`
- **Header size:** 56 bytes (0x38)
- **Compression:** LZMA1 (standard Python `lzma` module)

---

The header fields (all big-endian, after the two null-terminated version strings):

| Offset | Field | Notes |
|--------|-------|-------|
| +0 | `file_size` (u32) | Total uncompressed size |
| +4 | `header_size` (u32) | Always 0x38 = 56 |
| +8 | `unk1` (u32) | Always 1 |
| +12 | `file_count` (u32) | Number of assets in bundle |
| +16 | `compressed_size` (u32) | LZMA stream size |
| +20 | `uncompressed_size` (u32) | Decompressed size |

---

## Bundle Categories

### WORLD_CHUNK - Terrain Scene Bundles

Named `camargue_X_Y.unity3d`. Each contains one Unity scene.

- `containsScene = true`
- `isAssetContainer = false`
- `containsTerrain = true`
- Internal scene name follows the `camargue_X_Y_subX_subY` pattern
- Adjacent chunks may share the same `sceneName`

Note: the `sceneName` in the XML is the internal Unity level name, not the bundle filename. These are different values. See the system overview for the full mapping table.

Contents include: terrain geometry, collision meshes (`DLT_coll_*`), audio emitters (`DLT_SND_*`), GameObjects, LOD meshes, and POI localization keys.

---

### TERRAIN_TEX - Terrain Texture Packs

Named using the bundle's own MD5 hash as the filename.

- `containsScene = false`
- `isAssetContainer = true`
- `assetBundleInfoLink` points to the paired geometry bundle

One texture bundle per world chunk. Contains terrain splat textures (Texture2D assets) for the paired geometry bundle's terrain renderer.

**Confirmed pairings so far:**

| Geometry bundle | Texture bundle (hash) |
|-----------------|----------------------|
| `camargue_0_5` | `077b4143ea30c794ca0194f755f28174` |
| `camargue_2_0` | `20cba32e9e550ad48850b10c44867f16` |
| `camargue_5_1` | `da6d3e6bad071dc4d89da074a72573b4` |
| (see catalog for full list) | |

---

### QUEST_SCENE - Quest and Dialog Scenes

Named `Sc_DLT_Q#####_A.unity3d` or `Sc_DLT_Q#####_B.unity3d`.

- `containsScene = true`
- `isAssetContainer = false`
- Contain complete gameplay geometry and logic

Confirmed contents from binary analysis:

- `HorseSpawner` objects
- Race paths `_path01` through `_path09`
- Obstacle objects with dimension metadata (e.g. `_Obstacle01_400_40_100`)
- Trigger chains (`_CSO_Chain_trigger_01`, `_02`)
- Barrier geometry (`_wallGauche`, `_wallDroite`, `_barriere`)

Quest scenes are complete and functional, not stubs or placeholders.

---

### CHAR_ANIM - Character Skeletons and Rigs

The core character bundles. These are among the largest files in the set.

| Bundle | Content | Compressed size |
|--------|---------|-----------------|
| `2c81c468...` | Horse full rig + 61 animation clips | 5.3 MB |
| `04bc26f6...` | Female rider (Adulte_F) full biped skeleton | 584 KB |
| `0a9fe77f...` | Palefrenier (stable hand) rig | 500 KB |
| `3ed484fa...` | NPC_PecheurVieux (old fisherman) | 506 KB |
| `3f69468a...` | NPC_Instructeur_1 (riding instructor) | 476 KB |
| `2fbeb84d...` | Palefrenier_Bip alternate rig | 472 KB |
| `3e8be2e7...` | Palefrenier + Vendeur1 NPC pair | 14 KB |
| `0fc35c45...` | Adulte_F skeleton stub | 10 KB |

**Horse animation clips confirmed in `2c81c468...`:**

Locomotion: `IDLE_RESPIRATION`, `PAS1_D`, `PAS2_D`, `PAS3_D`, `TROT1_D`, `TROT2_D`, `TROT3_D`, `GALOP1_D`, `GALOP2_D`, `GALOP3_D`

Jumping: `GRAND_SAUT`, `PETIT_SAUT`

Behaviour: `AGGRESSIF`, `ENERVE_COUP_SABOT` (angry hoof kick), `SECOUER_TETE` (head shake)

Grooming: `SABOT_AV_G_LEVER` (lift front-left hoof) and equivalents for all four hooves

61 clips total.

---

### AVATAR_ASSET / HORSE_ASSET - Character Equipment

Rider clothing and horse equipment bundles. Named with `AVT_*` or `CHV_*` prefixes in their internal content.

Confirmed items found so far:

- `AVT_F_Buste_Tshirt2_Bras2_Type01_A` - female T-shirt variant
- `AVT_F_Buste_Polo_Bras2_Type01_A` - female polo shirt
- `AVT_M_Buste_Chemise_Bras2_Type01_A` - male dress shirt

The full set of known bundle IDs from DLL string analysis is documented in the system overview.

---

### WORLD_PROP - Environment Props

Standalone mesh bundles for world decoration. These are streamed alongside terrain chunks.

Confirmed props found so far:

**Flora:** `pin_alep_01` (Aleppo pine), `Peuplier_Blanc_01` (white poplar), `massette_02` (cattail), `pres_sale_02` (salt marsh), `Oyat_groupe_1` (marram grass), `Lis_Maritime` (sea lily), `bamboos04`, `verseau01`, `Grass_Lotier_01`, `rock_compo_01`

**Built environment:** `Mur01` (stone wall), `Camepement_tente_01` (campsite tent)

---

### PROP_MESH - General Props

Smaller prop bundles for specific objects.

Confirmed: `barriere_poteau_double` (double-post fence), `passerelle_elevation` (raised walkway), `passerelle_45_Barriere` (angled fence bridge), `voiture_rouge` (red car), `Vespa` (scooter), `flacon_shampooing` (shampoo bottle, stable prop), `chicore_tige` (chicory stem), `Pelle_sot_00` (shovel)

---

### LD_BUNDLE - Level Design Prefabs

Obstacle course prefabs used by quest scenes.

Confirmed: `LD_Gabarit_Obstacle_250_145_60`, `LD_Gabarit_Obstacle_400_110_60`

The naming format `LD_Gabarit_Obstacle_<length>_<height>_<width>` gives the physical dimensions of each obstacle in the racing system.

---

### MATERIAL_STUB - Tiny Dependency Bundles

Very small bundles (under roughly 3KB) containing only a material reference. These are loaded as dependencies of larger mesh bundles, allowing the engine to share materials across multiple assets.

These do not need their own top-level `asset_bundle_info_container` entry. They are referenced via `asset_bundle_dependency` inside their parent bundle's entry.

---

### AUDIO

Audio bundles confirmed in the dataset. Naming pattern suggests ambient audio is keyed to terrain coordinates using the same `DLT_SND_X_Y_subX_subY` coordinate system as the world chunks.

---

## World Map Coverage (as of batch 6)

Terrain chunks confirmed so far cover columns 0-18 and rows 0-8.

This suggests a world grid of roughly 19 x 9 = 171 terrain chunks minimum, each with a paired texture bundle. That would be around 342 world-related bundles out of 1087 total. The remaining bundles cover character assets, props, audio, dialog, UI, and other game content.

---

## Key Insight

The asset data is intact. The bundles decompress cleanly, internal geometry is present, animation data is complete, and quest scenes are fully structured. The only missing piece is the configuration manifest that tells the engine what exists.

Once bundle analysis is complete, generating `Build_infos.xml` is a straightforward process: go through every bundle, compute its MD5 and size, extract its internal name and scene reference, and write the XML entry.
