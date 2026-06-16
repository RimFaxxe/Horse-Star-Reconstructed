# Horse Star - Bundle Catalog

This is a record of every `.unity3d` bundle that has been processed so far.
Each entry includes the filename, file size, MD5 hash, category, and any identifying
detail that could be extracted from the bundle contents.

**Current coverage: around 210 of roughly 1087 bundles.**

This file will be updated as more bundles are processed.

---

## Category Summary

| Category | Count | What it is |
|----------|-------|------------|
| PROP_MESH | 77 | General prop mesh (fences, vehicles, buildings, triggers, collectables) |
| TERRAIN_TEX | 42 | Terrain splat texture pack, one per world chunk |
| MATERIAL_STUB | 20 | Tiny material-only dependency bundle |
| WORLD_PROP | 19 | Environment prop (trees, plants, rocks) |
| CHAR_ANIM | 16 | Character skeleton, animation rig, or named clip bundle |
| TEXTURE | 6 | Standalone texture asset |
| AVATAR_ASSET | 5 | Rider clothing and body part mesh |
| LD_BUNDLE | 5 | Level design obstacle prefab (with entry/exit triggers) |
| VFX | 5 | Particle and visual effect |
| WORLD_CHUNK | 4 | Terrain chunk scenes (camargue_X_Y) |
| QUEST_SCENE | 3 | Quest and dialog scene bundle (Sc_DLT_) |
| UNKNOWN | 2 | Could not classify yet |
| SCRIPT | 2 | Network or UI script bundle |
| SHADER | 2 | Custom shader bundle |
| UI_TEXTURE | 1 | UI and HUD texture |
| AUDIO | 1 | Audio bundle |

---

## World Chunks

Terrain scene bundles that make up the open world. Each has a paired terrain texture bundle.

| Bundle name | sceneName (internal) | Size (bytes) | MD5 |
|-------------|----------------------|--------------|-----|
| camargue_0_4 | camargue_0_5_0_1024 | 24358 | 559aca7f0036b5018dd867c3ea77b3c7 |
| camargue_0_5 | camargue_0_5_0_1024 | 25268 | 66f108c19359adeeb77095207487542f |
| camargue_2_0 | camargue_1_3_512_0 | 5014 | 499f8dc22fbbc7a4c9265cf271d03df8 |
| camargue_5_1 | camargue_2_3_1024_0 | 4783 | 57a7af89e1d4d467f2c933482748ab12 |

---

## Terrain Texture Packs

One texture bundle per world chunk. The filename is the bundle's own MD5 hash.
Note: some chunk coordinates use negative Y values, indicating the world grid extends below row 0.

| Paired with | Texture bundle filename | Size (bytes) | MD5 |
|-------------|------------------------|--------------|-----|
| camargue_0_0 | 4fbd33dd140516440ad932679cd33670 | 2041 | 272b02c1fa1f6163c377e46df74808c3 |
| camargue_0_2 | 6f28f0381a21dd14395fa5ab3017e341 | 126802 | e3f5138245036ddbdd982185ab5375ea |
| camargue_0_5 | 077b4143ea30c794ca0194f755f28174 | 85815 | 3b5a73d22b5cef439f8e932858e7df4e |
| camargue_0_7 | 5a109a8bb966e834181434dca1fc9bcd | 88437 | abebf528f6e8d5ba4dd2c895b140688a |
| camargue_0_9 | 1e324b5ef975f0b478255eeeced4dc46 | 37070 | bb2f609206a3f0bfb9b955d9c8b4408b |
| camargue_10_2 | 7b10da28a0380634b872d1297004246e | 169397 | ec6196b4b64cda1e15bc37af7098494a |
| camargue_10_7 | 003f4a98c1b140d4087c4fb3b0fa24ed | 134572 | 0291b5f8b322a9b610a655d5b14a646d |
| camargue_11_1 | 1beefea8d0d72524caa69248f58dd336 | 190496 | e8afca97620d844053d1e8789b75357b |
| camargue_11_5 | 4a346d1cb069e18428cdb787bcd5ed42 | 68550 | 7cb074a4d448191500d24daf6c5e5281 |
| camargue_11_7 | 1b52ce754529d774a8b52221de44ce4f | 102047 | 8a1622b029d59c43ebcf4d25a346ae8b |
| camargue_12_-3 | 5d407f9db90d1804c83c89917e17f76a | 77647 | 8739dcec95dff9abf52d800e65c47e7d |
| camargue_12_2 | 5cc0e991b9b215a43b49e62295aaee66 | 66602 | fd21b775fe6c939e9b38025cf38ef580 |
| camargue_12_4 | 3cb1c9d367fa68e438d310fdb7f3441d | 56819 | af20341dd6c9e966cf1649056445bcd0 |
| camargue_13_-3 | 4f1690b08e2f16843bb913a85cadd6df | 88810 | 32799356b2e1df9bfe40a93d87d4182d |
| camargue_14_0 | 1ea1fb8dcb88ed6458dab835c6f2d7c8 | 82250 | b32dc859c542a01d99d55cd18e405331 |
| camargue_15_-3 | 4a64ea16979c21c4288935c022d51692 | 155645 | 658c2814e0aaeef33f069faa44963419 |
| camargue_17_0 | 5e2d26f7609f0a8409331dfb3e9309af | 174724 | d6b9a199e69fab3276d7e198521a7fe4 |
| camargue_17_2 | 2a5245aec1b58ce418b7ff48fd81389c | 44976 | 58023c85c760dc09b805702167577e6e |
| camargue_17_3 | 2aa085569efa3a1479ee6b076a3f8ed8 | 8102 | c71b8a7b8a0e593561b487036ecbdab0 |
| camargue_18_0 | 0ad46907a99b5a34cb1d3436fe0fd7cc | 117923 | 9ede990660f01b86852047fac9e21674 |
| camargue_1_0 | 2ba40887b00016f4182c8dd0287e2c72 | 2221 | 4a61a44139596ddd79d1412c23a36dc3 |
| camargue_1_2 | 5e6a2582800f3a1429f9551683d72591 | 162818 | 182d702f12e66c99fd1dfe3a99925c47 |
| camargue_1_4 | 0d52d829e5b04eb44ba8538ede323bcd | 150310 | 6c09b053ce6fbaf8af6f2b817f3682f4 |
| camargue_1_6 | 6f40e653a899dcb4e899e58d1a41c3fa | 141337 | e1ce29182f24bba03bb8432f42e9bd07 |
| camargue_1_7 | 6f467a17bab8a6f4f840c8b20722f385 | 94632 | 3ae5bdc720e69e5213793061f00f68b1 |
| camargue_2_0 | 20cba32e9e550ad48850b10c44867f16 | 3686 | 2554346a540b04f3c760708670c5fa53 |
| camargue_2_3 | 01a23459af6fd6c40a314112a3803f46 | 74250 | 94ed8dff4b0b081ff877041f9d878919 |
| camargue_2_5 | 7a20e6271b171ff4f9b2067d5eb1a321 | 60729 | 9dd81a33769b0772974865182a314527 |
| camargue_2_6 | 3b099967d371a8740ac78d6fde2acd2e | 104672 | 8f5fa36885477cfd3acc4a48e0ead6c5 |
| camargue_3_8 | 1c269a38af8a1da46983eec235b46580 | 81852 | b4cc14e0603d1178c006ed2c68a51672 |
| camargue_4_5 | 2dc91653acf360a40ad00a9aef123927 | 25682 | f7c687ee60732e9be355e5814efda9a0 |
| camargue_5_1 | da6d3e6bad071dc4d89da074a72573b4 | 2046 | 4d10702ddd855f3727b228bb7976fa2b |
| camargue_5_5 | 04f006acd323ed642ae18374324e0590 | 17455 | a1fc2e1e22a6255b07bd3a592d5f2bf4 |
| camargue_5_6 | 7df1d92f4802bc14cb5171216cb70d4d | 15127 | bbd9d8bb3e458a5fe08a2956f1a51120 |
| camargue_7_0 | 2d801c6f8be8cba4db4f02e254ed5058 | 174895 | 0e89c8a6be745797b6bd906304f51d0e |
| camargue_7_2 | 4cd155e023b3439438929535adb1ede2 | 80487 | 020ff120a8301e9296efe91508fbe34d |
| camargue_7_3 | 4edd021f7285a5045a7d562b5127b7a9 | 58347 | 1fa9b432bd87d93ddeff171a1594c426 |
| camargue_7_6 | 1f2db723581bcdc45b64fa2e07ea0e48 | 51349 | 7277d5646dbe0ac01ac4176b23fece44 |
| camargue_8_5 | 2cbaa92e71984b245bac037b4da5db37 | 98282 | fca10d18379cf5c99cf7812a57dbce9e |
| camargue_8_6 | 5b4eb605d4600764aab0d4c2546862c1 | 66640 | 61f4220b498380f5bfef551659fca7ef |
| camargue_9_1 | 0a0e95632aee9c04590e12c3b5ac2c70 | 46623 | 6f3a1348cb1c360ac707e22836226839 |
| camargue_9_6 | 7b268a59a9980034c959b07ecd4ab563 | 58902 | f84d498721171b2e51a305f17cfd63ef |

---

## Quest and Dialog Scenes

Complete gameplay scenes containing geometry, race paths, obstacles, and trigger logic.

| Bundle name | Size (bytes) | MD5 |
|-------------|--------------|-----|
| Sc_DLT_Q00010_B | 6438 | dbc1a5a79e665af78bb5cdbb3e271b07 |
| Sc_DLT_Q00016_A | 95846 | 2db7072a8957fe05b6c9c0c684815b3b |
| Sc_DLT_Q00023 | 1549 | 8363b28a20933ac95b94fceb976cda36 |

---

## Character Skeletons, Rigs, and Animation Clips

| Content | Size (bytes) | MD5 |
|---------|--------------|-----|
| HORSE full rig + animation clips (41MB decompressed) | 5284232 | dd88209969c9a3b4b60390d5f50c2b47 |
| Adulte_F full skeleton rig (female rider biped) | 583674 | f85dca023e9f059b831478e4fa056492 |
| Adolescente full skeleton rig (female teen biped, full finger/facial/IK bones, HUD_Quete bone) | 530520 | f437f96079c772f794aebe3ce6353096 |
| NPC_PecheurVieux | 506048 | 3d0c4cb456a26a191516db3099907e34 |
| NPC_Adolescent_1 (Adolescent_Mesh, full rig + animal controller) | 501385 | e6b7ad7ab9aa65b386fe0550873c6b45 |
| Palefrenier (stable NPC) | 500502 | 0ab31e28d0cf001319af2baebb3fe118 |
| NPC_Instructeur_2 (Directeur_Mesh, full rig + animal controller) | 497252 | 7de5d447423850ca17ee708b0a182ad3 |
| NPC_Instructeur_1 | 475707 | b9d3f7745fe907a54a035b98be4f9e8e |
| Palefrenier_Bip | 471856 | 30c574f43b8d08a8a73eee5c7402ea4d |
| NPC_Gitan_2 (Adulte_M_gitan2 mesh, full rig, hoof sounds + camera mode) | 459574 | db9b647f99ae94a5fd39949bfce81318 |
| Adolescente2 + Instructeur5 combined rig (Adolescente2 full biped/facial/finger bones, Instructeur5_Mesh + Alpha_Mesh) | 112766 | 24fdf311a63fa0cd2a5fbdf05a951960 |
| Gitan2@MONTRER animation clip (NPC_Gitan_2 show/present gesture) | 18337 | 281d9d1e5104e902e6994319a0ae05b8 |
| animation clip bundle (unnamed, CompressedAnimationCurve) | 18234 | 90f5c00e212ac32b5c3bb04f2560534f |
| Palefrenier + Vendeur1 NPC rigs (stable hand + vendor) | 14154 | f79fc4ac1251bf28e5f9c0df9c7e70bb |
| Gitan2@TOURNER_GAUCHE + Directeur eyelid IK bone paths (NPC_Gitan_2 turn-left clip, Directeur full bone path data) | 12938 | 25d6e7302383e0387800a6d67fe89cb2 |
| Adulte_F skeleton/rig | 10223 | 2fa1a60e6e650450f69cd5a97211c447 |

---

## Avatar and Rider Asset Bundles

| Content | Size (bytes) | MD5 |
|---------|--------------|-----|
| AVT_F_Pieds_Baskets_Mollet1_Type01_A (female sneaker boots) | 90092 | a03346fadfd03ebcbcf79410c92713a6 |
| AVT_M_Buste_Chemise_Bras2_Type01_A | 72781 | 8ffe54411b0f63d7a1406a10c3e0f85b |
| AVT_F_Buste_Polo_Bras2_Type01_A | 48850 | b6c29c18bf52642fccfc7fc789b82c4f |
| AVT_F_Jambes_Baggy_NoMollet_Type01_B (female baggy trousers no calf, variant B) | 44297 | f16413be5ec43b86731d5a1efeeb6183 |
| AVT_F_Buste_Tshirt2_Bras2_Type01_A | 31745 | 8697d11e2f2eca44f29a2856b3230210 |

---

## Environment Props

| Content | Size (bytes) | MD5 |
|---------|--------------|-----|
| arbre_pin_parasol_Dune (umbrella / parasol pine tree) | 1409 | 786a29a99c3ea06e12e9a2cd869e43b7 |
| bamboos04 / Bambous_tunnel | 40662 | 82f83612254dc1ae6b14d24bbb07654b |
| bambous_pousse (bamboo shoots / young bamboo) | 6180 | e1d1ccc188a6193a29e5901b94b7c8bd |
| Grass_Jonc_03 (rush grass) | 75702 | 8604e3d6d3606d812d6799017e4bab67 |
| Grass_Lotier_01 | 86159 | 36429d650487ce316718a8376c64bf96 |
| Grass_Lotier_02 (bird's-foot trefoil grass variant 2) | 96948 | 19ac22e7a22a9d92973656c3870b78b8 |
| Grass_Mouron_02 (scarlet pimpernel / mouron grass) | 184462 | a88b1e71957d25027e3a642e88e9710a |
| Grass_Saladelle_01 (sea lavender / statice plant) | 73410 | 3ab061e892ec04854b67ac1122bb677e |
| massette_02 (cattail / marsh plant) | 81985 | 9a9e59fef115613b6402555fd66452d1 |
| Mur01 (wall) | 121191 | 90d50338c9a2923fe10f8d2078a1466f |
| Peuplier_Blanc_01 (white poplar tree) | 19263 | 6ce0acaf183d14cbe1a77f3ad136144b |
| Peuplier_Blanc_03 (white poplar tree variant 3) | 26788 | d55970ff9150d71aa1b1b43e243f8c22 |
| pin_alep_01 (Aleppo pine tree) | 24010 | f09c1d27b6295e577e7c0add6c653082 |
| pres_sale_02 (salt marsh) | 9583 | 70da6c8b987a33634b03ccb1b7f61f72 |
| rock_compo_01 | 1439 | ae2b5545dbdb76947dfcb1d3331262c7 |
| sansouire_3 (Camargue saltmarsh shrubland vegetation) | 172893 | ced1a29c2ebfb277c05160c5a81b02b5 |
| sansouire_block_1 (Camargue saltmarsh block variant 1) | 11021 | be2886dd931d2852c995f7809b7da52a |
| treetrunk / tree_trunk (large tree mesh + normal map) | 1287113 | 66cf001061669968221e8fcc6d78341c |
| verseau01 | 153864 | e839ca3003c5a83738cbb5af09d4cce8 |

---

## General Props

| Content | Size (bytes) | MD5 |
|---------|--------------|-----|
| aqueduc_collider (aqueduct with Photographable component, largest prop so far ~1.5MB) | 1498196 | 1a7fde8477ecba45261aeda5288755a3 |
| barriere_base (fence base post, dep: clotures_murs) | 4309 | fb4c4f40f4a5d8e4d05c9a8f55d2ca11 |
| Barriere_obstacle_cross_00 | 4310 | 136d6424c245a911b1e18dfd56afade0 |
| Barriere_obstacle_cross_poteau_00 | 2963 | 7607c80e4b379c4e6ffb7488f39fa543 |
| Barriere_Pecheur_00 / barriere_pecheur_neuf_00 (fisherman's fence, BoxCollider trigger) | 15702 | 9153461a52fe75ae78440eea8f8dff51 |
| barriere_porte_fermee (closed gate, lightmap ref camargue_2_6_1024_1536, BoxCollider trigger) | 10679 | 3cfa8aa9c9f57ca1832b058693ea6cfd |
| barriere_poteau_double | 2963 | f695087ad525aaac579287b136349866 |
| barriere_sable (sand/beach barrier, BoxCollider trigger, dep: clotures_murs) | 1578 | d2851298ddbdb096bf852dc2dae20e1b |
| building prop (unnamed, dep: buildings + scripts) | 9476 | b974599961f499c9cdba74e2e775e15a |
| building prop with sceneTag (unnamed ~70KB, dep: buildings) | 69978 | f919b490f5c53f000c94d8e3195fb171 |
| Camepement_tente_01 | 10243 | f0b11ad28157b2d55ec34695894071a1 |
| chicore_tige | 5408 | 9f4c8f64bd1e213866fe8210c5d950db |
| collectable object (m_collectableObjectType, m_isHighlightEnabled, SphereCollider trigger) | 85108 | 6c569249935025f780fe749ed85c90e6 |
| curseur_jet | 3117 | 22416fae2aa9c3efd53910a9c99ae7de |
| Cylinder01 | 5969 | 1aab7e41b579b8fff722623c86d8dd58 |
| Cylinder02 | 4618 | 6bd95396aed632d5349ecad52dab8278 |
| Cylinder02 (variant, dep: 7d09aef + 4af4fc vegetation mat) | 19737 | f3f48800886439f775b685fecbbd140b |
| dortoir (manège dormitory building with ivy / lierre) | 537798 | 86b00a2715a40f23c4f6770a41cea2ad |
| flacon_shampooing / etale_nourriture (stable props) | 146002 | ffe0931ef3d0317f570954d949f98a43 |
| Fountain_plane | 1670 | c29cfeccd3dcbc127355a6c21d8e7f3a |
| GameObject | 6283 | 000c80ec9cbd3f910214b71b119caa78 |
| Juncusacutusold_08 | 3460 | f207844199243db099f227812d9e504a |
| Lis_Maritime | 30483 | 08ad2883014156630f19cf9b0a8bffc3 |
| MainTex | 348200 | 7a400d35962102762e73a274bc552784 |
| MainTex | 2044 | ebd02f9f8a0ee0ab423326c0c1604540 |
| MainTex | 125529 | 26dc340630868114c1391f635d480d18 |
| mesh_Barriere01 | 17608 | cf399ef4166064dfa94b861785a356d0 |
| MonoBehaviour | 1559 | bdd04fe46e12ae38e64e01603450e388 |
| MonoBehaviour | 1588 | d024d359197951fbf2d18c2e87f6a891 |
| MonoBehaviour | 2388 | 2e14a3925f2fda392baa8909035dabca |
| Object03 (dep: scripts) | 10780 | 8a44de13096563c9bb546990790ef3b9 |
| Object05 | 24745 | 20dbbe355d1df1b274338345dbffd524 |
| Object143 (dep: 7f1501d2 + 7d09aef) | 6082 | 261e1581419c2842a366f7bb5ffaca56 |
| Object145 | 3692 | 65b8b397c8df47324dc9d0078ea317a6 |
| Object2211 (dep: 4fdb14db vegetation mat) | 66168 | 8d2f5586b5a46267a3d1b28ec0d57ae5 |
| Object2214 | 68834 | c994ceae1efab8b61ca5811d8e69ec2b |
| Oyat_groupe_1 | 7697 | 88b0b783e34194faed5b4ba074486793 |
| Passerelle_45_Barriere | 7769 | 28072e82b3fd724f92da36b658de5c7c |
| passerelle_elevation | 2089 | 58fe5345d2480fdce79bf75fc8e3d4fd |
| Pecheur_Cabane_02_00 (fisherman's hut) | 1422 | 5ea06f87bc892445b39964981238c024 |
| Pecheur_CannePeche_00 (fisherman's fishing rod) | 4740 | 0a4ef9bc01d747dcfca85948f874f5c5 |
| Pecheur_Epuisette_00 (fisherman's landing net / dip net) | 5793 | 47883e0c97f444e4149762f790942556 |
| Pecheur_FeuCamp_00 (fisherman's campfire, dep: mobilier + scripts) | 11485 | b3245451a7b12df6f159046064399083 |
| Pecheur_Filet_00 (fisherman's net with MeshCollider) | 8905 | fd6ee0311a06a266a20fbf313cc8ed34 |
| Pelle_sot_00 | 34580 | ff4197aa3a1443ba3285c23f4706eb00 |
| Photographable | 22244 | 3c059b847f3b680ccd142c3316192ef3 |
| Pres_sale_clairseme_01 | 20020 | cce361fa7995ac8ec0aec9609895722a |
| prop mesh (unnamed ~111KB, dep: fca327533bf3d2b41bfe2fff58e34a3e) | 110992 | 871c5092ef609e0b18ebc58b519a5b2b |
| prop mesh (unnamed ~22KB, dep: 7d09aef + 67c90f4d) | 21829 | 38da0cab82950ee0a33a70f320480133 |
| prop mesh (unnamed ~23KB, dep: 7d09aef + d11f0e79) | 22917 | 1bd6c88015a90ad24b849b75178afa96 |
| prop mesh (unnamed ~5KB, dep: 73112f0e10698034eb7b18842592860e) | 4726 | 84c9e1d82d24d544d97988032c94de3a |
| prop mesh (unnamed ~6KB, dep: mobilier) | 6132 | 0de293aa5bcc8dc498a989a33bf134fb |
| prop mesh (unnamed ~8KB, dep: mobilier + scripts) | 8481 | af8879254ee62433b40edcf3e7d71136 |
| prop mesh (unnamed, dep: 4fdb14db521d9e54ab4d62369d32cd91) | 65247 | 7d964252546dc28666db980673182436 |
| prop mesh with BoxCollider trigger (unnamed ~2KB, dep: 62e97f64 + shaders) | 2038 | 00b568cfc501d0d05cb279844cb03131 |
| prop mesh with BoxCollider trigger + texture + lightmap (unnamed ~30KB, dep: shaders + scripts + 7af17543) | 30303 | 73e2e8af1c2d5968e921ae67fedb7199 |
| prop mesh with BoxCollider trigger + texture + lightmap (unnamed ~48KB) | 47698 | 60d50be1c8813b280e57b072bd0119d8 |
| prop mesh with CapsuleCollider trigger (unnamed ~28KB, dep: 7d09aef + fresne_leaves mat) | 27670 | b88d4e93dab34853f6cf0672820b74ba |
| prop mesh with CapsuleCollider trigger + _BaseLight texture (unnamed ~21KB) | 21434 | 76a8209198ba8f796dd9aa4a4228ee49 |
| prop mesh with lightmap + sceneTag (unnamed ~45KB) | 44760 | e5332ee2c184949311a3941efaf22a57 |
| prop mesh with texture + lightmap (unnamed ~43KB) | 43440 | e27996c9d768843b8118e7beb59bb780 |
| prop mesh with texture + lightmap (unnamed ~77KB) | 76689 | 84430714e4949daa7755880bd8819769 |
| prop mesh with texture + lightmap + sceneTag (unnamed ~111KB) | 110617 | cabbd7088ac6141fed3c3922e00e08b1 |
| prop mesh with texture + lightmap + sceneTag (unnamed ~150KB) | 149613 | a40416e4b8bf6a986a2f85ab9495a4cf |
| Rock 12 / rock_13 (rock prop, dep: scripts + d7c42031) | 6352 | a531ecabe78734845cf7ba63f28aa5c2 |
| rock_1 | 10601 | 3333a7dc1a4368c50f71416d216e5294 |
| SceneLauncher / Sc_Ecurie (stable scene trigger object) | 59820 | 6b78b725e39dead2a15499526428d0b9 |
| shop vendor object (m_isSellingRiderCloth, m_riderLevelMin, m_horseLevelMin, m_disposable, icon/texture asset bundle refs, lightmap camargue_1_5_512_1024) | 113080 | e1bb0c0835504ed01da59c85af669bd7 |
| stake/post prop | 12874 | 03464bde860b071db33f61a0baf08da1 |
| trigger (pure invisible BoxCollider trigger volume, dep: scripts) | 1135 | 3e8d70ab6029e92867fd779a1261d8fc |
| vehicle mesh with MeshCollider (unnamed ~52KB, dep: 88d3e21f + scripts + 5bee21ae vehicle tex) | 52259 | 0d8cc16134ebd3764c316f58cf9539b6 |
| vehicle prop (unnamed ~1.4KB, dep: aa72e012 + scripts + vehicules) | 1431 | 174344e94dc7dea14d6891d00587ac18 |
| vehicle prop with MeshCollider (unnamed ~1.4KB, dep: vehicules + scripts) | 1368 | c3f585fc9851522d4f7e7a03a05b08ed |
| Vespa (scooter) | 154742 | 19ec593a3ab8d6ee8804dd6a5b8e13e0 |
| voiture_rouge | 398848 | 62a8214528bd24db358f4f105243b792 |
| world prop ~10KB | 10056 | 6167182f2d9af5e6de646c47041979b9 |
| world prop ~13KB | 13514 | cdc3b87191ee411e807e0d19f4e001e8 |

---

## Level Design Prefabs

Obstacle course prefabs. The format `LD_Gabarit_Obstacle_length_height_width` gives physical dimensions.
Newer bundles include `Trigger_Entree` and `Trigger_Sortie` BoxColliders for timing gates.

| Content | Size (bytes) | MD5 |
|---------|--------------|-----|
| LD_Gabarit_Obstacle_250_145_60 | 2008 | 73d24d41a03bdcf5c5d62dea035848e3 |
| LD_Gabarit_Obstacle_250_40_60 | 1995 | 0167ce554184fb952cb103c8b09da2b0 |
| LD_Gabarit_Obstacle_400_110_60 | 2003 | e79e2f5940f26c57522e3f0acb04c5b3 |
| LD_Gabarit_Obstacle_400_145_60 (with Trigger_Entree + Trigger_Sortie, dep: cso + scripts) | 2003 | 67a4a4002e9beae2deadcf583d3846ab |
| LD_Gabarit_Obstacle_600_40_100 (with Trigger_Entree + Trigger_Sortie, dep: cso + scripts) | 1997 | f6d51e137b93ee974021c3a5adeba492 |

---

## Material Stubs

Very small bundles containing only a material reference. Dependency bundles, no top-level config entry needed.

| Content | Size (bytes) | MD5 |
|---------|--------------|-----|
| barriere_porte-22 | 893 | d545d9280a39cad336d576d2a0bf8409 |
| female_rider_hr-material #136 | 891 | dae49b306c2ec2e106b1616581c1ce86 |
| female_rider_hr-material #21 | 857 | 61219d7aadc3de52faf72bfcdffc0ee5 |
| female_rider_hr-material #29 | 855 | fc2f5cb0cfa9ce859b718635768d31cc |
| female_rider_hr-material #33 | 854 | 8ea150aa94f9b48694f0b7874011d87e |
| female_rider_hr-standard_15 | 855 | 9c1543e47ed7f79ff81b7ee4dbd8fcc9 |
| fresne_leaves | 1019 | 9aaac80602a9d9db0e09c122a21a59bc |
| fumee_Mat (smoke material, dep: fxs) | 943 | d1333bb3ac2bb61a36619d14e36758ba |
| male_rider_hr-bermuda (shorts material) | 892 | fb26632e5cbd50f6904abc5b7d54b9e0 |
| male_rider_hr-material #332 | 898 | c38c564b4510e6c1bbbca88f7407f7db |
| male_rider_hr-standard_5 | 854 | 70ab8d6946da803bdf4b3c8bb03c591d |
| male_rider_hr-tshirt2 (dep: shaders + c1bc8e31 texture) | 889 | 95eeb2913912235b995bf0c00ea92dee |
| material stub (dep: 76270de9 + vegetation bundle) | 1083 | d89405955c51be18ca5611e5a6709c2b |
| material stub (dep: buildings bundle) | 868 | 5eb84f189b5a2741b1da5084fdc9f362 |
| material stub (dep: vegetation bundle) | 1026 | b022ac189a597d71f3f54b02cd72bb45 |
| material stub ~1.2KB | 1248 | c7d0f57796ebfc1db0c169425965d766 |
| material stub ~1KB | 1025 | 77535ed793f570dfaf603cb0af0eecbc |
| material stub ~1KB | 1015 | 8af142d65ccefa9b036241de187b99dc |
| material stub ~900B | 901 | 56b154af5d3e0bda60b72bc2acb4226b |
| vegetation material stub with _BaseLight texture (dep: 675fb414 + vegetation) | 979 | 6957d9d814cdae0b5e4e74383216a555 |

---

## Shaders

Custom HorseStar shader bundles containing GLSL/Cg source.

| Content | Size (bytes) | MD5 |
|---------|--------------|-----|
| HorseStar/WrapBlinnPhong/Diffuse Bump SpecCol Halo mask shader | 7047 | abf9d725457e80bbef573146c13c9e85 |
| Diffuse Bumped Specular Alpha shader (DiffSpecBumpM, with _BumpMap + alpha cutoff + light power controls) | 1155 | e942dd2d0810fd792ce12ba37a94b0d6 |

---

## Other

Textures, audio, VFX, scripts, and bundles not yet classified.

| Category | Content | Size (bytes) | MD5 |
|----------|---------|--------------|-----|
| TEXTURE | 1dd4ccbeeb5d77f42ae27e643c6a70a6 | 110451 | b33697aabf5d7f8daaa5db94f5070f65 |
| TEXTURE | 3c455f0af5b5f6843bd307bf68b5adf0 | 95820 | b52c2be0e43d2905cdadd16f97753f0a |
| TEXTURE | 3d0f5b21fede31147b4b7d9128ec7930 | 139372 | 3f05247ea627d3ffdf74fa778af807e5 |
| TEXTURE | m_AlphaTex | 56866 | e78527eb6a40a0e1b261af1db90b4b14 |
| TEXTURE | roche_nuit_D (night rock texture) | 348631 | 98762daeadc4a35b77fdf3ddb6785e24 |
| TEXTURE | vehicle texture (dep: 607cb454 + vehicules bundle) | 121105 | 880e173cdad49dd9bc8262cff3dd40f3 |
| VFX | CustomAssetBundle | 2359 | b032c938402419e8aec596a65bbf07fe |
| VFX | CustomAssetBundle | 7687 | 2b52b86a19836f5e605ad12d959cce9b |
| VFX | Particle System x5 (EllipsoidParticleEmitter, UV animated) | 2962 | a9c71293ac14c2d37efdd4251a667ed1 |
| VFX | PPtr<$ParticleEmitter> | 2362 | 0a9da0a4ee648aa5dcc3a790c42f8772 |
| VFX | rocher_torche (torch rock particle) | 156948 | c15e8486b85c2d5a04948ec35521663b |
| AUDIO | monticule_D (terrain audio / ambient) | 162518 | 552cb1fb351a92c9e7153f4f38d4acb6 |
| UI_TEXTURE | FlechesIndirect | 1643 | c37b85bb4a46f3c32527ee636cae063b |
| SCRIPT | MonoBehaviour with iconTexture + sceneTag (UI/scene script stub) | 1259 | a7a1158d771b224ce7cc5091ee3f0a97 |
| SCRIPT | Network_RemoteHorseRiderMessageHandler (multiplayer network script) | 636 | e4b63bd896b8ac4fdc8a7baab7a267cc |
| UNKNOWN | 1db8f49229969d84c80902658c2e3223 | 18216 | f0127b3cec4e9a5d76a3defdf08ad717 |
| UNKNOWN | 2b8c363c9fd5fec4c88c6ced34f6d78c | 851 | ea9933af01797a7f60d319c766c7051f |
