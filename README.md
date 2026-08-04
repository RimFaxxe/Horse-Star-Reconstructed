# Horse Star Reconstructed

A reverse engineering and preservation project for the 2010 MMO *Horse Star*. 

The game never left beta and was killed off alongside *Mission Equitation Online*. While the official servers and source code are entirely lost, we have partially recoverable client data. This repo is dedicated to documenting and tearing down the game's internal data structures to figure out how it worked and eventually get it running again.

For context on the game itself, check out the [TMQ Horse Game Database wiki page]([https://miraheze.org](https://horsegamedatabase.miraheze.org/wiki/Horse_Star).

## Goals
* Crack and document all core data formats.
* Reverse and rebuild the asset bundle configuration system including `Build_infos.xml`, `Build_infos_generated.xml`, and `.picf`.
* Map out asset bundle dependencies and how the client handles loading.
* Stand up a precise private server based entirely on client-side data.

## What's working so far
Some progress has been made in understanding how the client behaves:

* **Schemas and Compression:** XML schemas are present in `Assembly-CSharp.dll`, and `.picf` files appear to use zlib compression (`Ionic.Zlib`).
* **World Mechanics:** The world seems to be divided into asset bundle chunks using a `camargue_X_Y_subX_subY` naming pattern, likely representing a grid system (possibly 512-unit cells). These appear to be split into geometry and texture bundles.
* **Assets and Logic:** Several scenes (login, character creation, stables, grooming) are identifiable and still contain geometry and scripts.
* **Rigs and Renders:** NPC rigs (instructor, stable hand, etc.) and a horse animation rig with ~60 clips are present in the data.
* **Progress:** Around 110 out of ~1,087 asset bundles have been looked at in more detail, though all bundles have been extracted.

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

## Current blocker

Client crashes on login because rdvIP is null:

System.Net.IPAddress.Parse(ipString)

I suspect config/init issue but not sure where rdvIP is supposed to be set. Any help tracing this would be appreciated.

*(Note: This is a pure preservation project. We do not distribute original game assets, nor do we possess original server code. All reverse engineering is built entirely out of client-side data. Original game developed by Punchers Impact and published by Mindscape in 2010. See LICENSE for details.)*

