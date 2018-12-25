# Server Operations

## Install nfs server

```sh
$ sudo apt-get update
$ sudo apt-get install -y nfs-kernel-server
```

## Config nfs

```sh
$ sudo echo "/home/linux_fhb/NfsEdit *(rw,sync,no_root_squash)" >> /etc/exports
```
- `/home/linux_fhb/NfsEdit`: the directory you want to export
- `*`: all pc can visit this directory, you can also set like "10.0.2.0/24"
- `(rw,sync,no_root_squash)`: set file permission

## Restart nfs Server

```sh
$ sudo /etc/init.d/rpcbind restart
$ sudo /etc/init.d/nfs-kernel-server restart
```

## Change directory mode
```sh
$ chmod o+x /home/linux_fhb/NfsEdit
```
We visit this directory through nfs with user name **dialout**

# Client Operation

## Check NFS

```sh
$ showmount -e 192.168.1.250
```

## Mount directory
```sh
$ sudo mount -o resvport sihua:/home/linux_fhb/NfsEdit ./SihuaEdit
```
if you want unmount the directory, just run :
```sh
$ sudo umount ./SihuaEdit
```


