# Contributing to Horse Star Reconstructed

Thanks for checking out the project! Horse Star is a piece of lost media that never got the marketing or attention it deserved. We want to reconstruct the game servers so it can be played and preserved for the future.

Whether you're an experienced reverse-engineer, a Python dev, or just a fan of the game who has old client files on a hard drive, your help is welcome!

## How You Can Help

### 1. Reverse Engineering & Networking
The current milestone is fully reverse-engineering the **OUDP protocol** used by the Mindscape client.
* Look at the scripts in the `/Server` directory. We currently have a basic RDV STUD stub server and local asset serevr working, but the protocol states need to be strictly mapped.
* If you have experience with `Assembly-CSharp.dll` decompilation (using ILSpy/dnSpy) or packet sniffing, any findings regarding packet structures are highly valued. Please document them in `docs/findings`.

### 2. Testing & Game Assets
* We need to test the local asset server with different game clients. If you have different versions of the Horse Star client, please let us know.
* Help us populate the `/Data`, `/Configs`, and `/Build_Infos` folders with verified files to test if the client pulls them correctly.

## Getting Started
1. **Check the Issues tab**: Look for issues tagged with `good first issue` or `help wanted`.
2. **Fork the repo**: Make your changes in a separate branch.
3. **Submit a Pull Request (PR)**: Keep it concise. Explain what part of the server logic, routing, or documentation you fixed or improved.

## Community
If you want to discuss findings, coordinate packet dumps, or talk about old Mindscape horse games (like Mission Equitation), join our Discord!

