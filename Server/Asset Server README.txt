HORSE STAR - LOCAL REVIVAL PACKAGE
====================================
Written June 2026, updated August 2026. Based on DLL analysis and output_log.txt findings.

WHAT WE KNOW (from output_log.txt and Assembly-CSharp.dll analysis)
---------------------------------------------------------------------
1. The game uses CDN path /r16/ (NOT /r12/ as hardcoded in DLL)
   Full CDN base: http://assets01.horsestar.net/r16/

2. On startup the game immediately requests two config files:
   - /r16/Config/EN_Dialogs.txt       (if all UI text is missing = no button labels)
   - /r16/Config/InputDefinitions_QWERTY.txt  (input mapping missing = clicks do nothing)

3. The game also needs a LOCAL file at:
   <HorseStar install>\HorseStar_Data\Resources\Data\Client\Client.txt
   This is the network config file (server addresses, ports etc).
   Without it the game throws a NullReferenceException and the login
   button never works.

4. Client.txt is an XML file with these fields (found in DLL):
   - useSettings, useNetwork, useOnline, useAssetBundle
   - mapSize, displayDebugGUI
   - serverAddress, dxDiagAddress
   - StudServerName, RdvIP, RdvPort
   - ClientIP, ClientPort, ZoneSize
   - SynchronizeRemotePlayersTimePeriod
   - SynchronousRequestsMaxAttemps, SynchronousRequestsMaxWaitingTimeMs
   - LoginMaxAttemps

5. The network architecture uses:
   - A "Stud" server (login/session management)
   - A "Rendezvous" (RDV) server (peer discovery/matchmaking)
   - POM (Peeroman) protocol for peer-to-peer connections
   Both Stud and RDV need to be running for login to work.

FILES AND FOLDERS THE SERVER NEEDS
----------------------
Client.txt                   - Local network config (points everything to 127.0.0.1)
Build_infos.xml              - Reconstructed asset manifest (210 of 1087 bundles)
Build_infos_generated.xml    - Same file (game expects both copies)
Build_infos_generated.picf   - zlib-compressed copy of the above
local_server_v3.py           - HTTP server for asset bundles + config files
build_infos                  - folder for the build_infos XML files
bundles                      - folder for unity3d bundles the server needs to hand off to the game client
config                       - folder for the config files the game asks for

STEP 1 - INSTALL CLIENT.TXT
-----------------------------
Create this folder if it doesn't exist:
  <your HorseStar install location>\HorseStar_Data\Resources\Data\Client\

Copy Client.txt into that folder.

STEP 2 - INSTALL THE BUILD_INFOS FILES
----------------------------------------
Create this folder if it doesn't exist:
  <your HorseStar install location>\Editor Default Resources\Build Infos\

Copy these three files there:
  Build_infos.xml
  Build_infos_generated.xml
  Build_infos_generated.picf

STEP 3 - SET UP HOSTS FILE
----------------------------
Open Notepad as Administrator.
Open: C:\Windows\System32\drivers\etc\hosts
Add at the bottom:
  127.0.0.1 assets01.horsestar.net
Save and close.

STEP 4 - SET UP THE LOCAL SERVER
----------------------------------
Put your .unity3d bundle files in the 'bundles' folder.

Put EN_Dialogs.txt and InputDefinitions_QWERTY.txt in the 'config' folder.

Open Command Prompt AS ADMINISTRATOR and run:
  python local_server_v3.py

Leave it running.

STEP 5 - LAUNCH THE GAME
--------------------------
Launch Horse Star normally. Watch the server window - every file the
game requests will appear. Any [MISSING] line tells you what's still needed.

WHAT WILL AND WON'T WORK
--------------------------
WILL work (probably):
- Game launches and reaches login screen (already confirmed)
- Asset server intercepts bundle requests
- Build_infos.xml gives the engine a bundle index for 210 bundles (needs to be fixed to index all 1087 bundles)

WON'T work yet:
- Login button (needs Stud + RDV servers running, which are separate projects)
- Input (InputDefinitions_QWERTY.txt not yet fully recovered, only E or Enter will register as input but not mouse clicks)
- Most of the world (876 bundles still uncatalogued)

NEXT STEPS FOR FULL REVIVAL
-----------------------------
1. Continue reconstructing EN_Dialogs.txt and InputDefinitions_QWERTY.txt based on new findings
2. Implement a minimal Stud server that accepts login and returns a session (that still doesn't work)
3. Implement a minimal RDV server for peer discovery
4. Continue cataloguing the remaining 877 asset bundles
5. Open the Asset Ripper Unity project in Unity 3.1 to find missing XML schema details

KNOWN ARCHITECTURE (from DLL)
-------------------------------
Network namespaces:
  Com.Pi.Peeroman         - POM peer-to-peer protocol
  Com.Mindscape.Network   - Game network layer
  Com.Mindscape.MHC       - Main game logic (MHC = My Horse Club / HorseStar)

Login flow (inferred):
  1. Game reads Client.txt for server addresses
  2. Connects to Stud server (StudServerName + ClientPort)
  3. Sends LoginRequest with login + password
  4. Receives LoginResponse with sessionId + rdvId
  5. Connects to RDV server (RdvIP + RdvPort) for peer discovery
  6. Downloads asset bundles from CDN (assets01.horsestar.net/r16/)
  7. Reads Build_infos to know which bundles exist
  8. Streams world chunks as player moves

CDN VERSION NOTE
-----------------
The DLL hardcodes /r12/ but output_log.txt shows the game actually
requests /r16/ at runtime. This suggests the version path was updated
server-side and the client fetches the current version dynamically.
Watch the server log for the exact paths the game requests.
