# Home Lab Setup


## Kali Laptop

Configure Virtual Bridge virbr0
```
3: virbr0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN group default qlen 1000
    link/ether 52:54:00:b8:e9:81 brd ff:ff:ff:ff:ff:ff
    inet 10.23.58.30/24 brd 10.23.58.255 scope global virbr0
       valid_lft forever preferred_lft forever
```

### MicroK8s
Date: 2024-03-17
#### Create Disk
```console
sudo -iu root
cd /var/lib/libvirt/images
qemu-img create -f qcow2 umksn1.qcow2 20G
chown libvirt-qemu:libvirt-qemu umksn1.qcow2

ls -l umksn1.qcow2
-rw-r--r-- 1 libvirt-qemu libvirt-qemu      196928 Mar 17 13:43 umksn1.qcow2
```

#### Install Ubuntu Server
[Ubuntu Server](https://ubuntu.com/download/server)
Used for installation: Ubuntu Server 22.04.4 LTS

4 CPU
8GB RAM

Attach umksn1.qcow2 disk

Use network bridge virbr0  (allows to connect SSH to VM)

Install OpenSSH server
Install MicroK8s snap

After reboot


```
sudo apt upgrade
sudo apt install net-tools
```

#### MicroK8s
[MicroK8s](https://microk8s.io/docs/getting-started)
```
sudo usermod -a -G microk8s $USER
sudo chown -R $USER ~/.kube
sudo mkdir -p ~/.kube
newgrp microk8s
sudo reboot
```


Upgrade MicroK8s
```
sudo snap refresh microk8s --channel 1.29
```

Enable add-ons
```
microk8s enable hostpath-storage
microk8s enable ingress
microk8s enable dashboard
```

Configure Dashboard
```
microk8s kubectl port-forward -n kube-system service/kubernetes-dashboard 10443:443
```


