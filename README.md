# ClouDNS-Sync
 Sync BIND named dir to cloudns api. 

# Installation
 - Run following command. It will install python3, pip3 and packages.
```
./install.sh
```

# Usage
 create shellscript like this and run it simply. 
```
export CLOUDNS_API_AUTH_ID=****
export CLOUDNS_API_AUTH_PASSWORD=*******
export CLOUDNS_API_DEBUG=True
export BIND_NAMED_PATH=/var/named/chroot/var/
export SYNC_AFTER_SECONDS=15

python3 main.py 
```

# Scheduling ways
- cron
- EventManager (plesk)
