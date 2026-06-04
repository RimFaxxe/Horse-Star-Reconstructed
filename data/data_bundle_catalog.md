# Horse Star - Bundle Catalog

This is a record of every `.unity3d` bundle that has been processed so far.
Each entry includes the filename, file size, MD5 hash, category, and any identifying
detail that could be extracted from the bundle contents.

**Current coverage: around 110 of roughly 1087 bundles.**

This file will be updated as more bundles are processed.

---

## Category Summary

| Category | Count | What it is |
|----------|-------|------------|
| PROP_MESH | 33 | General prop mesh (fences, vehicles, objects) |
| TERRAIN_TEX | 23 | Terrain splat texture pack, one per world chunk |
| MATERIAL_STUB | 10 | Tiny material-only dependency bundle |
| WORLD_PROP | 10 | Environment prop (trees, plants, rocks) |
| CHAR_ANIM | 8 | Character skeleton and animation rig |
| TEXTURE | 5 | Standalone texture asset |
| VFX | 4 | Particle and visual effect |
| WORLD_CHUNK | 4 | Terrain chunk scenes (camargue_X_Y) |
| AVATAR_ASSET | 3 | Rider clothing and body part mesh |
| LD_BUNDLE | 3 | Level design obstacle and NPC prefab |
| QUEST_SCENE | 3 | Quest and dialog scene bundle (Sc_DLT_) |
| UNKNOWN | 2 | Could not classify yet |
| UI_TEXTURE | 1 | UI and HUD texture |
| AUDIO | 1 | Audio bundle |

---

## World Chunks

These are the terrain scene bundles that make up the open world.
Each one has a paired terrain texture bundle listed in the next section.

| Bundle name | sceneName (internal) | Size (bytes) | MD5 |
|-------------|----------------------|--------------|-----|
| camargue_0_4 | camargue_0_5_0_1024 | 24358 | 559aca7f0036b5018dd867c3ea77b3c7 |
| camargue_0_5 | camargue_0_5_0_1024 | 25268 | 66f108c19359adeeb77095207487542f |
| camargue_2_0 | camargue_1_3_512_0 | 5014 | 499f8dc22fbbc7a4c9265cf271d03df8 |
| camargue_5_1 | camargue_2_3_1024_0 | 4783 | 57a7af89e1d4d467f2c933482748ab12 |

---

## Terrain Texture Packs

One texture bundle per world chunk. The filename is the bundle's own MD5 hash.
The `assetBundleInfoLink` field in the config should point back to the paired geometry bundle.

| Paired with | Texture bundle filename | Size (bytes) | MD5 |
|-------------|------------------------|--------------|-----|
| camargue_0_5 | 077b4143ea30c794ca0194f755f28174 | 85815 | 3b5a73d22b5cef439f8e932858e7df4e |
| camargue_0_9 | 1e324b5ef975f0b478255eeeced4dc46 | 37070 | bb2f609206a3f0bfb9b955d9c8b4408b |
| camargue_1_0 | 2ba40887b00016f4182c8dd0287e2c72 | 2221 | 4a61a44139596ddd79d1412c23a36dc3 |
| camargue_1_4 | 0d52d829e5b04eb44ba8538ede323bcd | 150310 | 6c09b053ce6fbaf8af6f2b817f3682f4 |
| camargue_2_0 | 20cba32e9e550ad48850b10c44867f16 | 3686 | 2554346a540b04f3c760708670c5fa53 |
| camargue_2_3 | 01a23459af6fd6c40a314112a3803f46 | 74250 | 94ed8dff4b0b081ff877041f9d878919 |
| camargue_2_6 | 3b099967d371a8740ac78d6fde2acd2e | 104672 | 8f5fa36885477cfd3acc4a48e0ead6c5 |
| camargue_3_8 | 1c269a38af8a1da46983eec235b46580 | 81852 | b4cc14e0603d1178c006ed2c68a51672 |
| camargue_4_5 | 2dc91653acf360a40ad00a9aef123927 | 25682 | f7c687ee60732e9be355e5814efda9a0 |
| camargue_5_1 | da6d3e6bad071dc4d89da074a72573b4 | 2046 | 4d10702ddd855f3727b228bb7976fa2b |
| camargue_5_5 | 04f006acd323ed642ae18374324e0590 | 17455 | a1fc2e1e22a6255b07bd3a592d5f2bf4 |
| camargue_7_0 | 2d801c6f8be8cba4db4f02e254ed5058 | 174895 | 0e89c8a6be745797b6bd906304f51d0e |
| camargue_7_6 | 1f2db723581bcdc45b64fa2e07ea0e48 | 51349 | 7277d5646dbe0ac01ac4176b23fece44 |
| camargue_8_5 | 2cbaa92e71984b245bac037b4da5db37 | 98282 | fca10d18379cf5c99cf7812a57dbce9e |
| camargue_9_1 | 0a0e95632aee9c04590e12c3b5ac2c70 | 46623 | 6f3a1348cb1c360ac707e22836226839 |
| camargue_10_7 | 003f4a98c1b140d4087c4fb3b0fa24ed | 134572 | 0291b5f8b322a9b610a655d5b14a646d |
| camargue_11_1 | 1beefea8d0d72524caa69248f58dd336 | 190496 | e8afca97620d844053d1e8789b75357b |
| camargue_11_7 | 1b52ce754529d774a8b52221de44ce4f | 102047 | 8a1622b029d59c43ebcf4d25a346ae8b |
| camargue_12_4 | 3cb1c9d367fa68e438d310fdb7f3441d | 56819 | af20341dd6c9e966cf1649056445bcd0 |
| camargue_14_0 | 1ea1fb8dcb88ed6458dab835c6f2d7c8 | 82250 | b32dc859c542a01d99d55cd18e405331 |
| camargue_17_2 | 2a5245aec1b58ce418b7ff48fd81389c | 44976 | 58023c85c760dc09b805702167577e6e |
| camargue_17_3 | 2aa085569efa3a1479ee6b076a3f8ed8 | 8102 | c71b8a7b8a0e593561b487036ecbdab0 |
| camargue_18_0 | 0ad46907a99b5a34cb1d3436fe0fd7cc | 117923 | 9ede990660f01b86852047fac9e21674 |

---

## Quest and Dialog Scenes

These are complete gameplay scenes, not placeholders.
They contain full geometry, race paths, obstacles, and trigger logic.

| Bundle name | Size (bytes) | MD5 |
|-------------|--------------|-----|
| Sc_DLT_Q00010_B | 6438 | dbc1a5a79e665af78bb5cdbb3e271b07 |
| Sc_DLT_Q00016_A | 95846 | 2db7072a8957fe05b6c9c0c684815b3b |
| Sc_DLT_Q00023 | 1549 | 8363b28a20933ac95b94fceb976cda36 |

---

## Character Skeletons and Rigs

Core character bundles for riders, horses, and NPCs.

| Content | Size (bytes) | MD5 |
|---------|--------------|-----|
| HORSE full rig + animation clips (41MB decompressed) | 5284232 | dd88209969c9a3b4b60390d5f50c2b47 |
| Adulte_F full skeleton rig (female rider biped) | 583674 | f85dca023e9f059b831478e4fa056492 |
| NPC_PecheurVieux | 506048 | 3d0c4cb456a26a191516db3099907e34 |
| Palefrenier (stable NPC) | 500502 | 0ab31e28d0cf001319af2baebb3fe118 |
| NPC_Instructeur_1 | 475707 | b9d3f7745fe907a54a035b98be4f9e8e |
| Palefrenier_Bip | 471856 | 30c574f43b8d08a8a73eee5c7402ea4d |
| Palefrenier + Vendeur1 NPC rigs (stable hand + vendor) | 14154 | f79fc4ac1251bf28e5f9c0df9c7e70bb |
| Adulte_F skeleton/rig | 10223 | 2fa1a60e6e650450f69cd5a97211c447 |

---

## Avatar and Horse Asset Bundles

| Type | Content | Size (bytes) | MD5 |
|------|---------|--------------|-----|
| AVATAR_ASSET | AVT_F_Buste_Tshirt2_Bras2_Type01_A | 31745 | 8697d11e2f2eca44f29a2856b3230210 |
| AVATAR_ASSET | AVT_F_Buste_Polo_Bras2_Type01_A | 48850 | b6c29c18bf52642fccfc7fc789b82c4f |
| AVATAR_ASSET | AVT_M_Buste_Chemise_Bras2_Type01_A | 72781 | 8ffe54411b0f63d7a1406a10c3e0f85b |

---

## Environment Props

| Content | Size (bytes) | MD5 |
|---------|--------------|-----|
| Grass_Lotier_01 | 86159 | 36429d650487ce316718a8376c64bf96 |
| Mur01 (wall) | 121191 | 90d50338c9a2923fe10f8d2078a1466f |
| Peuplier_Blanc_01 (white poplar tree) | 19263 | 6ce0acaf183d14cbe1a77f3ad136144b |
| bamboos04 / Bambous_tunnel | 40662 | 82f83612254dc1ae6b14d24bbb07654b |
| massette_02 (cattail / marsh plant) | 81985 | 9a9e59fef115613b6402555fd66452d1 |
| pin_alep_01 (Aleppo pine tree) | 24010 | f09c1d27b6295e577e7c0add6c653082 |
| pres_sale_02 (salt marsh) | 9583 | 70da6c8b987a33634b03ccb1b7f61f72 |
| rock_compo_01 | 1439 | ae2b5545dbdb76947dfcb1d3331262c7 |
| treetrunk / tree_trunk (large tree mesh + normal map) | 1287113 | 66cf001061669968221e8fcc6d78341c |
| verseau01 | 153864 | e839ca3003c5a83738cbb5af09d4cce8 |

---

## General Props

| Content | Size (bytes) | MD5 |
|---------|--------------|-----|
| Barriere_obstacle_cross_poteau_00 | 2963 | 7607c80e4b379c4e6ffb7488f39fa543 |
| Camepement_tente_01 | 10243 | f0b11ad28157b2d55ec34695894071a1 |
| Cylinder01 | 5969 | 1aab7e41b579b8fff722623c86d8dd58 |
| Cylinder02 | 4618 | 6bd95396aed632d5349ecad52dab8278 |
| Fountain_plane | 1670 | c29cfeccd3dcbc127355a6c21d8e7f3a |
| GameObject | 6283 | 000c80ec9cbd3f910214b71b119caa78 |
| Juncusacutusold_08 | 3460 | f207844199243db099f227812d9e504a |
| Lis_Maritime | 30483 | 08ad2883014156630f19cf9b0a8bffc3 |
| MainTex | 348200 | 7a400d35962102762e73a274bc552784 |
| MainTex | 2044 | ebd02f9f8a0ee0ab423326c0c1604540 |
| MainTex | 125529 | 26dc340630868114c1391f635d480d18 |
| MonoBehaviour | 1559 | bdd04fe46e12ae38e64e01603450e388 |
| MonoBehaviour | 1588 | d024d359197951fbf2d18c2e87f6a891 |
| MonoBehaviour | 2388 | 2e14a3925f2fda392baa8909035dabca |
| Object05 | 24745 | 20dbbe355d1df1b274338345dbffd524 |
| Object145 | 3692 | 65b8b397c8df47324dc9d0078ea317a6 |
| Object2214 | 68834 | c994ceae1efab8b61ca5811d8e69ec2b |
| Oyat_groupe_1 | 7697 | 88b0b783e34194faed5b4ba074486793 |
| Passerelle_45_Barriere | 7769 | 28072e82b3fd724f92da36b658de5c7c |
| Pelle_sot_00 | 34580 | ff4197aa3a1443ba3285c23f4706eb00 |
| Photographable | 22244 | 3c059b847f3b680ccd142c3316192ef3 |
| Pres_sale_clairseme_01 | 20020 | cce361fa7995ac8ec0aec9609895722a |
| Vespa (scooter) | 154742 | 19ec593a3ab8d6ee8804dd6a5b8e13e0 |
| barriere_poteau_double | 2963 | f695087ad525aaac579287b136349866 |
| chicore_tige | 5408 | 9f4c8f64bd1e213866fe8210c5d950db |
| curseur_jet | 3117 | 22416fae2aa9c3efd53910a9c99ae7de |
| flacon_shampooing / etale_nourriture (stable props) | 146002 | ffe0931ef3d0317f570954d949f98a43 |
| mesh_Barriere01 | 17608 | cf399ef4166064dfa94b861785a356d0 |
| passerelle_elevation | 2089 | 58fe5345d2480fdce79bf75fc8e3d4fd |
| stake/post prop | 12874 | 03464bde860b071db33f61a0baf08da1 |
| voiture_rouge | 398848 | 62a8214528bd24db358f4f105243b792 |
| world prop ~10KB | 10056 | 6167182f2d9af5e6de646c47041979b9 |
| world prop ~13KB | 13514 | cdc3b87191ee411e807e0d19f4e001e8 |

---

## Level Design Prefabs

Obstacle course prefabs used by quest scenes.
The naming format `LD_Gabarit_Obstacle_length_height_width` gives physical dimensions.

| Content | Size (bytes) | MD5 |
|---------|--------------|-----|
| LD_Gabarit_Obstacle_250_145_60 | 2008 | 73d24d41a03bdcf5c5d62dea035848e3 |
| LD_Gabarit_Obstacle_250_40_60 | 1995 | 0167ce554184fb952cb103c8b09da2b0 |
| LD_Gabarit_Obstacle_400_110_60 | 2003 | e79e2f5940f26c57522e3f0acb04c5b3 |

---

## Material Stubs

Very small bundles containing only a material reference.
These are dependency bundles and do not need their own top-level config entry.

| Content | Size (bytes) | MD5 |
|---------|--------------|-----|
| barriere_porte-22 | 893 | d545d9280a39cad336d576d2a0bf8409 |
| female_rider_hr-material #136 | 891 | dae49b306c2ec2e106b1616581c1ce86 |
| female_rider_hr-material #33 | 854 | 8ea150aa94f9b48694f0b7874011d87e |
| female_rider_hr-standard_15 | 855 | 9c1543e47ed7f79ff81b7ee4dbd8fcc9 |
| fresne_leaves | 1019 | 9aaac80602a9d9db0e09c122a21a59bc |
| male_rider_hr-material #332 | 898 | c38c564b4510e6c1bbbca88f7407f7db |
| material stub ~1.2KB | 1248 | c7d0f57796ebfc1db0c169425965d766 |
| material stub ~1KB | 1025 | 77535ed793f570dfaf603cb0af0eecbc |
| material stub ~1KB | 1015 | 8af142d65ccefa9b036241de187b99dc |
| material stub ~900B | 901 | 56b154af5d3e0bda60b72bc2acb4226b |

---

## Other

Textures, audio, VFX, and bundles that could not yet be classified.

| Category | Content | Size (bytes) | MD5 |
|----------|---------|--------------|-----|
| UNKNOWN | 1db8f49229969d84c80902658c2e3223 | 18216 | f0127b3cec4e9a5d76a3defdf08ad717 |
| TEXTURE | 1dd4ccbeeb5d77f42ae27e643c6a70a6 | 110451 | b33697aabf5d7f8daaa5db94f5070f65 |
| UNKNOWN | 2b8c363c9fd5fec4c88c6ced34f6d78c | 851 | ea9933af01797a7f60d319c766c7051f |
| TEXTURE | 3c455f0af5b5f6843bd307bf68b5adf0 | 95820 | b52c2be0e43d2905cdadd16f97753f0a |
| TEXTURE | 3d0f5b21fede31147b4b7d9128ec7930 | 139372 | 3f05247ea627d3ffdf74fa778af807e5 |
| VFX | CustomAssetBundle | 2359 | b032c938402419e8aec596a65bbf07fe |
| VFX | CustomAssetBundle | 7687 | 2b52b86a19836f5e605ad12d959cce9b |
| UI_TEXTURE | FlechesIndirect | 1643 | c37b85bb4a46f3c32527ee636cae063b |
| VFX | PPtr<$ParticleEmitter> | 2362 | 0a9da0a4ee648aa5dcc3a790c42f8772 |
| TEXTURE | m_AlphaTex | 56866 | e78527eb6a40a0e1b261af1db90b4b14 |
| AUDIO | monticule_D (terrain audio / ambient) | 162518 | 552cb1fb351a92c9e7153f4f38d4acb6 |
| TEXTURE | roche_nuit_D (night rock texture) | 348631 | 98762daeadc4a35b77fdf3ddb6785e24 |
| VFX | rocher_torche (torch rock particle) | 156948 | c15e8486b85c2d5a04948ec35521663b |
