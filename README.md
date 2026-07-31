# Horse Star Reconstructed

A reverse engineering and preservation project for the 2010 MMO *Horse Star*. 

The game never left beta and was killed off alongside *Mission Equitation Online*. While the official servers and source code are entirely lost, we have partially recoverable client data. This repo is dedicated to documenting and tearing down the game's internal data structures to figure out how it worked and eventually get it running again.

For context on the game itself, check out the [TMQ Horse Game Database wiki page](https://miraheze.org).

## Goals
* Crack and document all core data formats.
* Reverse and rebuild the asset bundle configuration system including `Build_infos.xml`, `Build_infos_generated.xml`, and `.picf`.
* Map out asset bundle dependencies and how the client handles loading.
* Stand up a precise private server based entirely on client-side data.

## What's working so far
We have broken past the initial black box stage and mapped out a solid chunk of the engine:
* **Schemas and Compression:** Pulled the full XML schema out of `Assembly-CSharp.dll` and confirmed `.picf` is just standard zlib (`Ionic.Zlib`).
* **World Mechanics:** Mapped the asset bundle containers and cracked the world streaming system, which uses a `camargue_X_Y_subX_subY` grid with 512-unit cells. Chunks are handled via geometry plus texture bundle pairings.
* **Assets and Logic:** Verified that quest scenes still hold full geometry and gameplay scripts. Standard scenes like login, character creation, stables, and grooming are fully identified.
* **Rigs and Renders:** Recovered NPC rigs for the instructor, stable hand, fisherman, and vendor. We also have the full horse animation rig featuring 61 named clips.
* **Progress:** Deep-dived and analyzed roughly 110 out of 1,087 total asset bundles, though all 1,087 were fully extracted.

## The Todo List
* Parse and analyze the remaining 977 asset bundles.
* Reconstruct original `unityPath` values and map the complete bundle dependency graph.
* Pull object GUIDs and associated metadata.
* Figure out the true outer boundaries of the world grid.
* Generate working config files directly from recovered data.

## Data Availability
The full asset bundle dataset is too heavy to host directly in this git repository. You can find all extracted metadata, research findings, and scripts right here. If you want to dive into the raw data files, grab instructions from [`data/README.md`](data/README.md).

## Want to help?
We are looking for hands, especially if you have experience with:
* Old-school Unity 2.x and 3.x pipelines
* Asset bundle extraction, parsing, and tooling
* General reverse engineering

Drop a line in the [Discord server]([https://discord.gg](https://discord.gg/dQbXXAzWxg)) to coordinate, and take a quick look at [`CONTRIBUTING.md`](CONTRIBUTING.md) before jumping in.

## Repository Layout
```text
Build_Infos/    Temporary reconstructed BuildInfos.xml outputs (incomplete/experimental)
Server/         Stub server implementations and networking experiments
data/           Processed bundle metadata and reference catalogs
docs/findings/  Documented research, reverse engineering notes, and system analysis
```

*(Note: This is a pure preservation project. We do not distribute original game assets, nor do we possess original server code. All reverse engineering is built entirely out of client-side data. Original game developed by Punchers Impact and published by Mindscape in 2010. See LICENSE for details.)*

