# Horse Star Reconstructed

Horse Star Reconstructed is a reverse engineering and preservation project focused on reconstructing the data and systems of the 2010 Mindscape MMO *Horse Star*.

The game never left beta and was shut down alongside *Mission Equitation Online*, leaving behind partially recoverable client data but no official server or source code.

This project aims to document, reconstruct, and make sense of the game's internal structure so that it can be understood and potentially made functional again.

For more information about Horse Star, please check out this wiki page: https://horsegamedatabase.miraheze.org/wiki/Horse_Star

---

## Project Goals

* Reconstruct the game's asset bundle configuration system
* Document the structure of all core data formats
* Rebuild `Build_infos.xml`, `Build_infos_generated.xml`, and `.picf` files
* Map asset bundle relationships, dependencies, and loading behavior
* Preserve as much of the original game data as possible

---

## Current Status

Significant progress has already been made:

* Full XML schema recovered from Assembly-CSharp.dll
* `.picf` format identified as standard zlib compression (Ionic.Zlib)
* Asset bundle container structure mapped
* World streaming system identified (`camargue_X_Y_subX_subY`)
* Terrain system confirmed (geometry + texture bundle pairing)
* Built-in scenes identified (login, avatar creation, stable, etc.)
* Quest scenes verified to contain full geometry and logic elements
* Partial bundle analysis completed (~90 out of 1000+ files)

The system is no longer a black box. Reconstruction is possible.

---

## Data Availability

A full dataset of asset bundles exists, but is not hosted in this repository due to size constraints.

Metadata, extracted findings, and sample data are available here.

If you are interested in working with the full dataset, see the `data/README.md` file.

---

## What Still Needs Work

* Processing remaining asset bundles
* Mapping full bundle dependency graph
* Reconstructing `<unityPath>` values
* Extracting object GUIDs and metadata
* Identifying full world grid dimensions
* Rebuilding complete config files from real data

---

## Contributing

Contributions are welcome, especially from people with experience in:

* Unity (2.x / 3.x era pipelines)
* Asset bundle extraction and analysis
* Reverse engineering
* Data reconstruction and tooling

Please read `CONTRIBUTING.md` before starting.

---

## Project Structure

* `docs/` - Clean documentation and confirmed findings
* `research/` - Raw analysis and working notes
* `data/` - Metadata and dataset references
* `tools/` - Scripts for extraction and reconstruction
* `reconstructed/` - Rebuilt config outputs
* `meta/` - Roadmap and task tracking

---

## Important Note

This project is focused on research and preservation. This repository does not include or distribute original game assets. 
Any references to game data are for research and preservation purposes only.

No original server code is available. Any reconstruction effort is based entirely on client-side data and reverse engineering.

If you are interested in contributing, please join this Discord server: https://discord.gg/aEhUVBnSzH and share what you want to work on.
---

## Credits

Original game developed by Mindscape (2010).

This repository exists to document and preserve a piece of lost MMO history.

---

## License

See LICENSE file for details.
