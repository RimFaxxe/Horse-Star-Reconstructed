# Horse Star - System Reconstruction Overview

## Project Context

Horse Star (Punchers Impact / Mindscape, 2010) was an online Unity-based MMO that never left beta. The game relied heavily on client-side asset bundles and dynamically generated configuration files. No official server or source code is currently available.

This document consolidates all current reverse engineering findings into one technical reference.

---

## High-Level Architecture

The game is built around three systems that must all work together:

1. **Asset Bundles** (`.unity3d`) - all game content
2. **Configuration Files** (`Build_infos`) - the manifest that tells the engine what exists and where
3. **Runtime Loading Logic** (`Assembly-CSharp.dll`) - the code that reads the manifest and streams content

Without the config files, the engine has no index of what bundles exist. That is the root cause of the current revival issue.

---

## Configuration System

### The Three Core Files

| File | Role | Format |
|------|------|--------|
| `Build_infos.xml` | Original authored manifest | Plain XML |
| `Build_infos_generated.xml` | Runtime-generated copy | Plain XML |
| `Build_infos_generated.picf` | Compressed copy of generated XML | zlib (Ionic.Zlib) |

All three share the exact same XML schema. They were written to:
```
Editor Default Resources/Build Infos/
```
at runtime and deleted when the game closed, which is why they no longer exist on any recovered installation. A minimal version of them was rebuilt and is accepted by the game, and properly served by the local server.

### .picf Format

- Standard zlib compression (RFC 1950, the format with the `78 9C` / `78 DA` header)
- Uses Ionic.Zlib (`ZlibStream.CompressString` / `UncompressString`)
- No encryption, no custom magic bytes
- Fully reproducible from the XML

```python
import zlib
compressed = zlib.compress(xml_bytes, level=6)
# write compressed bytes to .picf
```

---

## XML Schema

### Root Structure

```xml
<?xml version="1.0" encoding="utf-8"?>
<build_infos>
  <asset_bundle_infos>
    <!-- one asset_bundle_info_container per bundle -->
  </asset_bundle_infos>
  <built_in_scenes>
    <!-- one built_in_scene per non-streamed scene -->
  </built_in_scenes>
  <minimap_infos>
    <!-- one minimap_info per map zone -->
  </minimap_infos>
</build_infos>
```

### Asset Bundle Container

```xml
<asset_bundle_info_container id="camargue_0_4">
  <unityPath>AssetBundleContents/camargue_0_4.unity3d</unityPath>
  <md5>559aca7f0036b5018dd867c3ea77b3c7</md5>
  <size>24358</size>
  <priority>0</priority>
  <isAssetContainer>false</isAssetContainer>
  <containsScene>true</containsScene>
  <asset_bundle_info name="camargue_0_4">
    <sceneName>camargue_0_5_0_1024</sceneName>
    <loadAtStart>false</loadAtStart>
    <isRoot>true</isRoot>
    <isLDScene>false</isLDScene>
    <containsTerrain>true</containsTerrain>
    <container>camargue_0_4</container>
    <assetBundleInfoLink></assetBundleInfoLink>
    <objects>
      <object>guid-string</object>
    </objects>
    <parent>parent-bundle-name</parent>
    <asset_bundle_dependency>dependency-name</asset_bundle_dependency>
  </asset_bundle_info>
</asset_bundle_info_container>
```

### Full Field Reference

#### asset_bundle_info_container fields

| Field | Type | Notes |
|-------|------|-------|
| `id` (attribute) | string | Unique identifier, matches the `name` attribute on its child `asset_bundle_info` |
| `unityPath` | string | CDN-relative path to the `.unity3d` file |
| `md5` | string | MD5 hash of the `.unity3d` file on disk |
| `size` | int | File size in bytes |
| `priority` | int | Load priority (0 = default) |
| `isAssetContainer` | bool | true for texture/asset-only bundles, false for scene bundles |
| `containsScene` | bool | true for world chunks and quest scenes |
| `asset_bundle_info` | list | One or more child bundle entries |

#### asset_bundle_info fields

| Field | Type | Notes |
|-------|------|-------|
| `name` (attribute) | string | Internal bundle name |
| `sceneName` | string | Unity scene name to load (not the same as the bundle name for world chunks) |
| `loadAtStart` | bool | Whether to preload on game start |
| `isRoot` | bool | Whether this is a root-level bundle |
| `isLDScene` | bool | Level-design scene flag |
| `containsTerrain` | bool | true for world terrain chunks |
| `container` | string | ID of the parent container |
| `assetBundleInfoLink` | string | For texture bundles: links back to the paired geometry bundle |
| `objects` / `object` | string list | Object GUIDs inside the bundle |
| `parent` | string | Parent bundle dependency |
| `asset_bundle_dependency` | string | Child bundle dependency |

### Built-in Scenes

These are loaded directly by the engine, not streamed from asset bundles:

```xml
<built_in_scenes>
  <built_in_scene>Sc_MainScene</built_in_scene>
  <built_in_scene>Sc_Login</built_in_scene>
  <built_in_scene>Sc_HorseCreation</built_in_scene>
  <built_in_scene>Sc_AvatarCreation</built_in_scene>
  <built_in_scene>Sc_Ecurie</built_in_scene>
  <built_in_scene>Sc_Pansage</built_in_scene>
</built_in_scenes>
```

### Minimap Info

```xml
<minimap_infos>
  <minimap_info name="camargue_X_Y">
    <md5>hash-of-minimap-asset</md5>
    <zoom>1.0</zoom>
    <GUID>unity-asset-guid</GUID>
  </minimap_info>
</minimap_infos>
```

---

## Asset Bundle System

### Two Bundle Types Per World Chunk

Every terrain area requires exactly two linked bundles:

**Geometry bundle** (`camargue_X_Y.unity3d`)
- `containsScene = true`, `isAssetContainer = false`
- Contains: terrain mesh, collision data, GameObjects, audio sources, LOD meshes

**Texture bundle** (named using its own MD5 hash)
- `containsScene = false`, `isAssetContainer = true`
- The filename is the bundle's own MD5 hash (self-verifying naming scheme)
- Contains: terrain splat textures
- Uses `assetBundleInfoLink` to point back to its geometry bundle

### Important: sceneName is not the same as the bundle name

The `sceneName` field is the Unity internal level name, not the bundle filename. These are different values:

| Bundle name | sceneName |
|-------------|-----------|
| `camargue_0_4` | `camargue_0_5_0_1024` |
| `camargue_0_5` | `camargue_0_5_0_1024` |
| `camargue_2_0` | `camargue_1_3_512_0` |
| `camargue_5_1` | `camargue_2_3_1024_0` |

Note that adjacent chunks can share a `sceneName`. This is intentional and means multiple bundles contribute to the same playable area.

### World Grid Formula

From `Streaming_AdditiveScenesLoader.GetAssetBundleName()` in the DLL:

```
bundle_name = "camargue_" + X + "_" + Y
scene_name  = "camargue_" + X + "_" + Y + "_" + subX + "_" + subY
grid_unit   = 512
```

X and Y are the world position divided by 512. subX and subY are the sub-cell coordinates within that grid cell.

### Known Shared Dependency Bundles

These bundle names appear as `customassetbundle-X` dependency references inside decoded
prop and character bundles. They are shared library bundles loaded early at startup and
referenced by large numbers of individual prop bundles. They have not yet been found as
standalone `.unity3d` files in the dataset.

| Bundle name | Probable contents |
|-------------|------------------|
| `scripts` | Core MonoBehaviour scripts (SceneLauncher, Photographable, CollectableObject, shop logic, etc.) |
| `shaders` | Main shared shader library |
| `vegetation` | Shared vegetation materials and textures |
| `buildings` | Shared building materials |
| `mobilier` | Furniture and interior fixture materials |
| `vehicules` | Vehicle materials and textures |
| `clotures_murs` | Fence and wall shared materials |
| `fxs` | Shared VFX and particle materials |
| `terraintextures` | Shared terrain splat textures referenced by TERRAIN_TEX bundles |
| `cso` | Course Sportive Obstacles - shared obstacle materials and scripts |
| `109b3289...` | Unknown, referenced by both LD_Gabarit obstacle bundles with timing triggers |
| `675fb414...` | Unknown, referenced by vegetation material stubs |
| `73112f0e...` | Unknown, referenced by Grass_Lotier_02 and other grass props |
| `fca32753...` | Unknown, referenced by sansouire_block_1 |
| `d7c42031...` | Unknown, referenced by Rock 12 prop |

---

## World Content

### Points of Interest

POI localization keys are embedded directly in world bundles:
```
HorseStar|POI_names|POI_<name>
```
Confirmed example: `POI_plage_orestan` (Orestan Beach) found inside `camargue_2_0`

### Audio Emitters

```
DLT_SND_<X>_<Y>_<subX>_<subY>_<soundtype><index>
```
Examples: `forest02_birds_midday04`, `forest01_river20`

### Collision Meshes

```
DLT_coll_<X>_<Y>_<subX>_<subY>_<index>
```

### World Grid Extent (known so far)

Bundle analysis has confirmed terrain texture packs for the following grid coordinates.
The grid uses negative Y values, meaning the world extends below row 0.

- X range confirmed: 0 to 18
- Y range confirmed: -3 to 9
- Negative Y confirmed at: X=12 (Y=-3), X=13 (Y=-3), X=15 (Y=-3)

---

## Asset Categories

From DLL string analysis, the full set of named bundle container IDs:

| Prefix | Category |
|--------|----------|
| `AVT_*` | Avatar (rider) clothing and body parts |
| `CHV_*` | Horse models and equipment |
| `RIDER_MALE_*` / `RIDER_FEMALE_*` | Rider body configuration |
| `HORSE_*` | Horse body configuration |
| `SHOP_*` | Shop category bundles |
| `ANIMAL_*` | Pet and animal bundles |
| `DLT_Q*` | Quest dialog scenes |
| `LD_*` | Level design prefabs and obstacles |
| `Sc_*` | Named scenes |
| `camargue_*` | World terrain chunks |
| `<md5 hash>` | Terrain texture packs (hash-named) |

---

## Character Assets Recovered So Far

| Asset | Size | Notes |
|-------|------|-------|
| Horse full rig + 61 animation clips | 5.3 MB | Complete locomotion system |
| Adulte_F full skeleton rig (female rider biped) | 584 KB | Full biped with facial bones |
| Adulte_F skeleton/rig (secondary bundle) | 10 KB | Smaller companion rig bundle |
| Adolescente full skeleton rig | 531 KB | Female teen biped; full finger, facial, and IK bones; includes HUD_Quete bone for quest indicator attachment |
| Adolescente2 + Instructeur5 combined rig | 113 KB | Two meshes in one bundle; Instructeur5 has Alpha_Mesh LOD variant |
| NPC_PecheurVieux (old fisherman) | 506 KB | Named quest NPC with full environment props |
| NPC_Instructeur_1 (riding instructor) | 476 KB | Tutorial and quest NPC |
| NPC_Instructeur_2 / Directeur | 497 KB | Full rig with animal controller; eyelid IK bones animated |
| NPC_Adolescent_1 | 501 KB | Teen NPC with full rig and animal controller |
| NPC_Gitan_2 (Romani NPC) | 460 KB | Has m_isPlayer and m_cameraMode fields, shares base class with player controller |
| Palefrenier (stable NPC) | 500 KB | Stable hand NPC |
| Palefrenier_Bip | 472 KB | Alternate Palefrenier rig |
| Palefrenier + Vendeur1 stub | 14 KB | Paired stable hand and vendor rig stub |
| Gitan2@MONTRER animation clip | 18 KB | Named show/present gesture for NPC_Gitan_2 |
| Gitan2@TOURNER_GAUCHE animation clip | 13 KB | Named turn-left clip; also contains Directeur full bone path data |
| Unnamed animation clip bundle | 18 KB | CompressedAnimationCurve format, no named rig |

Horse animation clips include: `IDLE_RESPIRATION`, `PAS1_D` through `PAS3_D`, `TROT1_D` through `TROT3_D`, `GALOP1_D` through `GALOP3_D`, `GRAND_SAUT`, `PETIT_SAUT`, `AGGRESSIF`, `ENERVE_COUP_SABOT`, `SECOUER_TETE`, grooming poses, and more. 61 clips total.

---

## Gameplay Systems Inferred from Bundle Analysis

These systems were identified from MonoBehaviour field names extracted during bundle
decoding. They are inferences from field names, not recovered source code.

### Shop and Item System

A vendor MonoBehaviour found in the bundle dataset exposes the following fields:

| Field | Type | Notes |
|-------|------|-------|
| `m_isSellingRiderCloth` | bool | Whether this vendor sells clothing |
| `m_riderLevelMin` | int | Minimum rider level to purchase |
| `m_horseLevelMin` | int | Minimum horse level to purchase |
| `m_disposable` | bool | Whether the item is consumable |
| `m_descriptionTextId` | string | Localization key for item description |
| `m_textureName` | string | Item texture asset name |
| `m_textureLowAssetBundleName` | string | Low-quality texture bundle for streaming |
| `m_textureHighAssetBundleName` | string | High-quality texture bundle |
| `m_iconTextureName` | string | HUD icon asset name |
| `m_iconLowAssetBundleName` | string | Low-quality icon bundle |
| `m_iconHighAssetBundleName` | string | High-quality icon bundle |

The dual low/high bundle pair confirms a two-LOD streaming strategy for item assets. The level gating fields (`m_riderLevelMin`, `m_horseLevelMin`) confirm progression-locked shop inventory.

### Collectable and Photography System

Two distinct collectable MonoBehaviours have been found:

**CollectableObject** - general pickup with `m_collectableObjectType` (typed enum, multiple categories) and `m_isHighlightEnabled` (visual proximity indicator). Uses a SphereCollider trigger.

**Photographable** - landmark photography system with `m_photographableType` (typed enum). Confirmed on the aqueduct prop (~1.5 MB, largest single prop found). Players could photograph landmarks, likely for a quest or collection mechanic.

### Scene Trigger System

`SceneLauncher` objects in the open world load named interior scenes on proximity. Confirmed example: an object with `m_sceneName = "Sc_Ecurie"` triggers the stable interior load. This confirms the world uses additive scene streaming for interiors rather than baking them into the open world chunks.

### Level Design Obstacle System

LD obstacle bundles come in two variants:

**Simple obstacles** (earlier format) - mesh only, no trigger volumes, named by physical dimensions (`LD_Gabarit_Obstacle_length_height_width`).

**Triggered obstacles** (later format) - same naming, but contain two BoxCollider trigger volumes: `Trigger_Entree` (entry) and `Trigger_Sortie` (exit). These are the timing gates used to score obstacle performance. Both variants depend on the `cso` shared bundle (Course Sportive Obstacles, probable expansion).

### Multiplayer Network System

A `Network_RemoteHorseRiderMessageHandler` script bundle confirms the game had a live multiplayer system for syncing remote horse and rider state. The NPC_Gitan_2 character bundle contains an `m_isPlayer` boolean field on its AnimalController, confirming the player controller and NPC controller share the same base class. This is consistent with a system where remote players are rendered using the same controller as NPCs, differing only by the `m_isPlayer` flag.

---

## Historical CDN

The original asset server URL is hardcoded in the DLL:
```
http://assets01.horsestar.net/r12/
```

Likely bundle path pattern:
```
AssetBundleContents/<bundle_name>.unity3d
```

This server is offline. Wayback Machine snapshots may have partial data.

---

## What Is Still Missing

| Element | Status |
|---------|--------|
| Bundle analysis | Around 210 of roughly 1087 complete |
| `unityPath` values | Pattern known, full list incomplete |
| Dependency graph | Partially mapped; shared bundle names known, files not yet found |
| Object GUIDs | Not yet extracted |
| Minimap GUIDs and zoom values | Not yet extracted |
| Full world grid dimensions | X: 0-18 confirmed, Y: -3 to 9 confirmed, full extent unknown |
| Shop item definitions | Field structure known, actual item data not recovered |
| Collectable type enum values | Type system confirmed, enum values not recovered |

---

## Reconstruction Feasibility

- No encryption blocking access
- No server-exclusive logic identified
- Core systems fully understood
- Full data set available

Full reconstruction is technically achievable.
