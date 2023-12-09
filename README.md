## Thanks sepehrsb & EchoStretch!

This code replaces step 2 to 6 from the game dump process by automating it.

Run this on Linux or in WSL2:
````bash
python3 dumper.py <ps5 ip> <ftp port> <PPSA title_id> 
```
This will grab all the required files from ftp including the NPWR files. They are a placed in the script directory in a folder named dumps.

ex: usage `python3 dumper.py 192.168.1.92 1337 PPSA02739`
```

### Steps for dumping game files
At This time it seems digital games and some physical games will work
**NOTE** PS5 SELF Dumper will only work on 4.03/4.50/4.51

1) Dump Game ( Opened Game ) /mnt/sandbox/pfsmnt
   https://github.com/logic-68/pfsmnt-dumper

2) Dump Game Files (copy folder content (files and folders))
   /system_data/priv/appmeta/PPSAXXXXX/ -->> PPSAXXXXX-app0\sce_sys\

3) Dump Game Files (copy folder content) 
   /user/appmeta/PPSAXXXXX -->> PPSAXXXXX-app0\sce_sys

4) Open npbind.dat to see uds and trophy folder 000000080->04->0F

5) uds00.ucp ( named uds.ucp )
   /user/np_uds/nobackup/conf/NPWRXXXXX_00/uds.ucp -->>PPSAXXXXX-app0\sce_sys\uds\uds00.ucp

6) trophy00.ucp (named TROPHY.UCP )
   /user/trophy2/nobackup/conf/NPWRXXXXX_00/TROPHY.UCP -->>PPSAXXXXX-app0\sce_sys\trophy2\trophy00.ucp

7) Decyrpt self files with sleirs ps5-self-dumper then copy files to game dir
   https://github.com/sleirsgoevy/ps4jb-payloads/tree/bd-jb/ps5-self-dumper
   1) Download socat
      https://github.com/tech128/socat-1.7.3.0-windows
   2) Place ps5-self-dumper payload in socat folder
      https://www.sendspace.com/file/k87zug
   3) Open PS5 browser to Specter host
   4) Open windows cmd in socat folder and type both commands
      socat -u FILE:dumpgame.bin TCP:<ps5 ip>:9020
      socat -u -d -d -d TCP:<ps5 ip>:9023,reuseaddr OPEN:game.tar,creat
   5) Open game.tar and copy/replace files in PPSAXXXXX-app0
```
