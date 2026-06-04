# Horse Star - System Reconstruction Overview

## Project Context

Horse Star (Mindscape, 2010) was an online Unity-based MMO that never left beta. The game relied heavily on client-side asset bundles and dynamically generated configuration files. No official server or source code is currently available.

This document brings together all current reverse engineering findings into one clear technical reference.

---

## High-Level System Architecture

The game is built around three core systems:

1. Asset Bundles (.unity3d)
2. Configuration Files (Build_infos)
3. Runtime Loading Logic (from Assembly-CSharp.dll)

All runtime behavior comes from how these systems interact.

---

## Configuration System

### The Three Core Files

| File                       | Role                                | Format |
| -------------------------- | ----------------------------------- | ------ |
| Build_infos.xml            | Original authored manifest          | XML    |
| Build_infos_generated.xml  | Runtime-generated version           | XML    |
| Build_infos_generated.picf | Compressed version of generated XML | zlib   |

All three use the exact same structure.

---

### .picf Format

* Standard zlib compression (Ionic.Zlib)
* No encryption
* Direct compression of XML content

**Conclusion:** This format is fully reproducible.

---

## XML Structure

Root structure:

```xml
<build_infos>
  <asset_bundle_infos>
  <built_in_scenes>
  <minimap_infos>
</build_infos>
```

---

### Asset Bundle Containers

Each bundle is defined like this:

```xml
<asset_bundle_info_container id="...">
  <unityPath>...</unityPath>
  <md5>...</md5>
  <size>...</size>
  <priority>0</priority>
  <isAssetContainer>true/false</isAssetContainer>
  <containsScene>true/false</containsScene>

  <asset_bundle_info name="...">
    <sceneName>...</sceneName>
    <container>...</container>
  </asset_bundle_info>
</asset_bundle_info_container>
```

---

## Asset Bundle System

### Two Types of Bundles

Each world chunk uses two bundle types:

1. Geometry bundle

   * camargue_X_Y.unity3d
   * Contains terrain, colliders, objects, audio

2. Texture bundle

   * Named using its MD5 hash
   * Contains terrain splat textures
   * Links back using `assetBundleInfoLink`

---

## World System

### Naming Formula

From DLL analysis:

```
camargue_<X>_<Y>_<subX>_<subY>
```

Where:

* Grid size = 512 units
* X, Y = world grid coordinates
* subX, subY = subdivisions within the grid

---

### Important Discovery

**sceneName is not the same as the bundle name**

Example:

| Bundle Name  | sceneName           |
| ------------ | ------------------- |
| camargue_0_4 | camargue_0_5_0_1024 |
| camargue_2_0 | camargue_1_3_512_0  |

What this means:

* bundle name = streaming grid cell
* sceneName = actual Unity scene being loaded

---

### Terrain Pairing

Each chunk has:

* Geometry bundle --> containsScene = true
* Texture bundle --> isAssetContainer = true

These must be linked together in the XML.

---

## Quest and Scene Data

Quest bundles contain full gameplay structures:

* HorseSpawner
* obstacle systems
* race paths (_path01 - _path09)
* trigger zones

These are complete scenes, not placeholders.

---

## World Content Findings

### POI System

Confirmed format:

```
HorseStar|POI_names|POI_<name>
```

Example:

* POI_plage_orestan (Orestan Beach)

---

### Audio System

Pattern:

```
DLT_SND_<X>_<Y>_<subX>_<subY>_<type>
```

Examples include:

* forest bird sounds
* river ambience

---

### Collision System

Pattern:

```
DLT_coll_<X>_<Y>_<subX>_<subY>_<index>
```

---

## Asset Categories

From DLL string analysis:

### Avatar Bundles

* AVT_* --> clothing, body parts, accessories

### Horse Bundles

* CHV_* --> horse models, gear, textures

### Rider Configuration

* RIDER_MALE_*, RIDER_FEMALE_*

### Shop Bundles

* SHOP_*

### Dialog Data

* EN_Dialogs.txt, FR_Dialogs.txt, etc.

---

## Built-in Scenes

These are loaded directly (not from asset bundles):

* Sc_MainScene
* Sc_Login
* Sc_HorseCreation
* Sc_AvatarCreation
* Sc_Ecurie
* Sc_Pansage

---

## Minimap System

* Naming follows: camargue_X_Y
* Uses zoom values and GUID references

Texture paths:

* /Textures/Minimap/
* /Minimap/

---

## Data Sources

### Confirmed Sources

* Asset bundles (.unity3d files)
* Assembly-CSharp.dll
* Local cache files (MD5s.xml)
* Old installation directories

---

### Historical CDN

Hardcoded URL:

```
http://assets01.horsestar.net/r12/
```

Likely bundle path:

```
AssetBundleContents/<bundle>.unity3d
```

---

## Current Project State

* 1000+ asset bundles available
* ~90 analyzed so far
* Full schema recovered

---

## What Is Still Missing

| Element              | Status     |
| -------------------- | ---------- |
| Full bundle analysis | Incomplete |
| unityPath values     | Unknown    |
| Dependency graph     | Incomplete |
| Object GUIDs         | Missing    |
| Minimap GUIDs        | Missing    |
| Full grid size       | Unknown    |

---

## Key Insight

This is not a data loss problem.

> The data exists. It just needs to be processed.

---

## Reconstruction Feasibility

This is fully achievable with:

* Complete bundle processing
* XML reconstruction
* Dependency mapping

No encryption or server-only logic has been identified so far.

---

## Contribution Focus Areas

* Bundle analysis (remaining files)
* Tooling for automated extraction
* XML reconstruction
* Dependency mapping
* Unity 3.x asset pipeline knowledge

---

## Final Note

The system itself is understood. What remains now is execution.
