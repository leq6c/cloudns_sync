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
export CLOUDNS_API_DEBUG=False
export BIND_NAMED_PATH=/var/named/chroot/var/

python3 main.py 
```
