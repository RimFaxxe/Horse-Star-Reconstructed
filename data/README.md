# Data

This folder contains structured reference data produced by the bundle analysis pipeline. It is meant to be useful to contributors without them needing to run any tools themselves.

---

## What Is Here

### bundle_catalog.json

A machine-readable catalog of every `.unity3d` bundle that has been processed so far. Each entry includes the filename, MD5 hash, file size, category, and any identifying detail extracted from the bundle contents.

This is the primary reference for reconstructing `Build_infos.xml`. As more bundles are processed, this file will be updated.

### bundle_catalog.md

A human-readable version of the same catalog, organized by category with tables for each bundle type. Easier to browse than the JSON if you just want to look something up.

---

## What Is Not Here

The actual `.unity3d` bundle files are not stored in this repository. They are too large to host here and are being shared separately with active contributors. If you need access to the full dataset, please ask in the Discord.

---

## How the Catalog Was Built

Bundles were decompressed and their contents analyzed to determine type and extract identifying information. MD5 hashes and file sizes were recorded directly from the files. No data here is estimated or reconstructed - everything comes from the actual bundle binaries.

---

## Current Coverage

Around 110 of roughly 1087 bundles have been processed so far. This file will be updated as analysis continues.
