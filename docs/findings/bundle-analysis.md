# Horse Star - Asset Bundle & Config Reconstruction Findings

## Overview

This document consolidates all current findings from analyzing Horse Star’s asset bundles and game assemblies. The goal is to clearly explain how the game’s content is structured, how it loads at runtime, and what is needed to reconstruct its configuration system.

Everything here comes directly from real data - .unity3d files and DLL analysis - not guesswork.

---

## Current Progress

* 1000+ asset bundles recovered
* ~90 bundles analyzed so far
* XML schema fully reverse engineered

This means we are no longer guessing how the system works. We are now filling in missing data.

---

## What the Asset Bundles Contain

The .unity3d files are the backbone of the game. They contain:

* world terrain chunks
* textures
* quest scenes
* character assets
* audio sources
* gameplay objects

From what we've seen so far, the data inside these bundles is complete and usable.

---

## Two Types of Bundles Per World Chunk

Each terrain area is split into two linked bundles:

### 1. Geometry Bundle

* Format: `camargue_X_Y.unity3d`
* Contains:

  * terrain meshes
  * collision data
  * game objects
  * sound emitters

### 2. Texture Bundle

* Format: `<md5>.unity3d`
* The filename itself is the MD5 hash
* Contains:

  * terrain splat textures

These are connected in the config using:

```
assetBundleInfoLink --> parent terrain chunk
```

---

## World Structure

### Naming System

From DLL analysis, world bundles follow this pattern:

```
camargue_<X>_<Y>_<subX>_<subY>
```

* Grid size is 512 units
* X, Y represent large world grid positions
* subX, subY represent subdivisions within that grid

This gives us a full coordinate-based streaming system.

---

## Important Discovery: sceneName vs Bundle Name

One of the most important findings:

> sceneName is NOT the same as the bundle filename

Example:

| Bundle Name  | sceneName           |
| ------------ | ------------------- |
| camargue_0_4 | camargue_0_5_0_1024 |
| camargue_2_0 | camargue_1_3_512_0  |

What this means:

* Bundle name --> where the data is stored
* sceneName --> what Unity actually loads

This distinction is critical when rebuilding the config files.

---

## Terrain Chunk Behavior

Some terrain bundles share the same sceneName.

This is intentional.

It means:

* multiple bundles can contribute to the same playable area
* the world is stitched together at runtime

---

## Confirmed World Data

### Points of Interest (POIs)

We found live POI data inside world bundles:

```
HorseStar|POI_names|POI_<name>
```

Example:

* POI_plage_orestan (Orestan Beach)

This confirms:

* localization keys are embedded in bundles
* world metadata is still intact

---

## Quest Scene Bundles

Quest-related bundles are fully structured scenes, not placeholders.

They include:

* HorseSpawner objects
* race paths (_path01 - _path09)
* obstacle systems
* trigger zones

These scenes appear to be complete and ready to run if properly loaded.

---

## Object Naming Patterns

### Audio

```
DLT_SND_<X>_<Y>_<subX>_<subY>_<type>
```

Examples:

* forest ambient sounds
* river audio loops

---

### Collision

```
DLT_coll_<X>_<Y>_<subX>_<subY>_<index>
```

These define physical interaction surfaces.

---

## Config System (From DLL Analysis)

All asset loading is controlled by the Build_infos system.

There are three files:

* Build_infos.xml
* Build_infos_generated.xml
* Build_infos_generated.picf

All three share the same structure.

---

## The .picf Format

The .picf file is simply:

> zlib-compressed XML

* Uses Ionic.Zlib
* No encryption
* Fully reversible

This means we can regenerate it once the XML is complete.

---

## XML Schema Status

The full schema has been recovered from Assembly-CSharp.dll.

We know:

* all element names
* all attributes
* full structure of bundle entries

What we *don’t* have yet is all the actual data to fill it.

---

## What We Still Need

To complete reconstruction, we still need:

* More bundle analysis (majority still untouched)
* Full list of bundle names and sizes
* unityPath values (CDN structure)
* Dependency relationships between bundles
* Object GUIDs
* Minimap data (GUIDs + zoom levels)

---

## Where Missing Data Can Come From

The remaining data is not gone - it just needs to be sourced.

Possible sources:

* additional .unity3d bundles
* old game installations
* MD5s.xml cache files
* CDN snapshots (Wayback Machine)
* Unity project remnants

---

## Key Insight

This is not a lost media problem.

> The data still exists. The challenge is processing and organizing it.

---

## Reconstruction Outlook

Based on current findings:

* No encryption is blocking access
* No server-exclusive data has been identified
* Core systems are fully understood

This makes full reconstruction technically possible.

---

## How to Contribute

If you're jumping into this project, the most useful areas are:

* analyzing remaining bundles
* building tools to extract data faster
* mapping dependencies between assets
* helping reconstruct config files
* working with Unity 3.x asset pipelines

Even partial findings are useful.

---

## Final Thoughts

We are past the "is this possible?" stage. The structure is understood and the pipeline is clear.

Now it's just a matter of continuing the work.
