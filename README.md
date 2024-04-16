# Home Lab Setup

## WSL Ubuntu
### Fix WSL Ubuntu to support python virtual environments
```
sudo apt-get update
sudo apt-get install libpython3-dev
sudo apt-get install python3-venv
```
Reference: [Installing venv for python3 in WSL (Ubuntu)](https://stackoverflow.com/questions/61528500/installing-venv-for-python3-in-wsl-ubuntu)

### install docker
```
 sudo apt install docker.io
``

### install net-tools
```
sudo apt install net-tools
```

## Linux Laptop

Configure Virtual Bridge virbr0
```
3: virbr0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN group default qlen 1000
    link/ether 52:54:00:b8:e9:81 brd ff:ff:ff:ff:ff:ff
    inet 10.23.58.30/24 brd 10.23.58.255 scope global virbr0
       valid_lft forever preferred_lft forever
```
![nm-connection-editor](pics/nm-connection-editor_virbr0.png)

### MicroK8s
Date: 2024-03-17
#### Network Bridge (virbr0) 
![nm-connection-editor](pics/virt-manager_virtual_networks_default.png)

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
[Ubuntu Server 22.04.4 LTS ISO media](https://releases.ubuntu.com/jammy/ubuntu-22.04.4-live-server-amd64.iso)

| Item | Value |
| ---- | --------------------- | 
| Name | Ubuntu-MicroK8S-Node1 |
| OS   | [Ubuntu Server 22.04.4 LTS ISO media](https://releases.ubuntu.com/jammy/ubuntu-22.04.4-live-server-amd64.iso) | 
| RAM  | 8 GB |
| CPU  | 4    |
| Disk | 20GB. Attach umksn1.qcow2 disk (see above) |
| Network | virbr0 | 


Install OpenSSH server

Install MicroK8s snap

After reboot
```
sudo apt upgrade
sudo apt install net-tools
```

Connect to console, and check assigned IP address
```
david@umksn1:~$ ip addr | head -n 10
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: enp1s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 52:54:00:c3:31:c4 brd ff:ff:ff:ff:ff:ff
    inet 10.23.58.134/24 metric 100 brd 10.23.58.255 scope global dynamic enp1s0
       valid_lft 2040sec preferred_lft 2040sec

```

Add entry to /etc/hosts on Host (Linux Laptop)
```
└─# tail -n 2 /etc/hosts

10.23.58.134 umksn1
```

From Host, install own ssh public key to Ubuntu Server VM
```
└─$ ssh-copy-id -i ~/.ssh/id_rsa david@umksn1
/usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/home/david/.ssh/id_rsa.pub"                                                              
/usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed                                       
/usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys                                     
david@umksn1's password:                                                                                                                                 
                                                                                                                                                         
Number of key(s) added: 1                                                                                                                                
                                                                                                                                                         
Now try logging into the machine, with:   "ssh 'david@umksn1'"                                                                                           
and check to make sure that only the key(s) you wanted were added.                                             
```




#### MicroK8s installation
[MicroK8s](https://microk8s.io/docs/getting-started)
In the Ubuntu Server Guest VM
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

Check status
```
david@umksn1:~$ microk8s status
microk8s is running
high-availability: no
  datastore master nodes: 127.0.0.1:19001
  datastore standby nodes: none
addons:
  enabled:
	dashboard        	# (core) The Kubernetes dashboard
	dns              	# (core) CoreDNS
	ha-cluster       	# (core) Configure high availability on the current node
	helm             	# (core) Helm - the package manager for Kubernetes
	helm3            	# (core) Helm 3 - the package manager for Kubernetes
	hostpath-storage 	# (core) Storage class; allocates storage from host directory
	ingress          	# (core) Ingress controller for external access
	metrics-server   	# (core) K8s Metrics Server for API access to service metrics
	storage          	# (core) Alias to hostpath-storage add-on, deprecated
  disabled:
	cert-manager     	# (core) Cloud native certificate management
	cis-hardening    	# (core) Apply CIS K8s hardening
	community        	# (core) The community addons repository
	gpu              	# (core) Automatic enablement of Nvidia CUDA
	host-access      	# (core) Allow Pods connecting to Host services smoothly
	kube-ovn         	# (core) An advanced network fabric for Kubernetes
	mayastor         	# (core) OpenEBS MayaStor
	metallb          	# (core) Loadbalancer for your Kubernetes cluster
	minio            	# (core) MinIO object storage
	observability    	# (core) A lightweight observability stack for logs, traces and metrics
	prometheus       	# (core) Prometheus operator for monitoring and logging
	rbac             	# (core) Role-Based Access Control for authorisation
	registry         	# (core) Private image registry exposed on localhost:32000
	rook-ceph        	# (core) Distributed Ceph storage using Rook
```

Add kubectl alias
```
echo alias kubectl=\"microk8s kubectl\" >> ~/.profile
```

Log off and log back in
```
$ kubectl get namespaces
NAME          	STATUS   AGE
default       	Active   9h
ingress       	Active   8h
kube-node-lease   Active   9h
kube-public   	Active   9h
kube-system   	Active   9h
```

Install KUBECONFIG file in MicroK8s VM
```
mkdir -p ~/.kube
microk8s config > ~/.kube/config
```

Install KUBECONFIG file in Host Linux Laptop.
```
mkdir -p ~/.kube
scp david@umksn1:/home/david/.kube/config ~/.kube/config
chmod 600 ~/.kube/config


┌──(david㉿kali-PF37QNB7)-[~]
└─$ kubectl auth whoami
ATTRIBUTE   VALUE
Username	admin
Groups  	[system:masters system:authenticated]
```

Create `homelab` namespace
```
kubectl create ns homelab
```

Create Secret to Docker Hub
```
kubectl create secret generic dockerhub -n homelab --from-file=.dockerconfigjson=/home/david/.docker/config.json --type=kubernetes.io/dockerconfigjson
```

Configure port forwarding for Dashboard on port 10443 (HTTPS)
```
kubectl port-forward -n kube-system service/kubernetes-dashboard 10443:443
```



### ArgoCD
Date: 2024-03-18

Check helm version on Host
```
└─$ helm version
version.BuildInfo{Version:"v3.14+unreleased", GitCommit:"", GitTreeState:"", GoVersion:"go1.21.6"}
```

Add ArgoCD Helm Repo
```
helm repo add argo-cd https://argoproj.github.io/argo-helm
helm dep update charts/argo-cd/
```

Install ArgoCD
```
kubectl create ns argocd
helm install -n argocd argo-cd charts/argo-cd
```

Retrieve ArgoCD admin password
```
┌──(david㉿kali-PF37QNB7)-[~/.kube]
└─$ kubectl get secret -n argocd argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

Configure port forwarding for ArgoCD on port 8080 (HTTP)
```
┌──(david㉿kali-PF37QNB7)-[~/.kube]
└─$ kubectl port-forward -n argocd svc/argo-cd-argocd-server 8080:80
Forwarding from 127.0.0.1:8080 -> 8080
Forwarding from [::1]:8080 -> 8080
```

Configure repository
in `homelab/configs/argocd/argocd-repositories.yaml`, add the current GitHub personal token (https://github.com/settings/tokens?type=beta)
Then, apply with
```
kubectl apply -n argocd -f argocd-repositories.yaml
```

![argocd-settings-repositories](pics/argocd_settings_repositories.png)


Configure project (from `homelab/configs/argocd/argocd-projects.yaml`)
```
kubectl apply -n argocd -f argocd-projects.yaml
```


Install argocd command line
```
curl -sSL -o argocd-linux-amd64 https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
sudo install -m 555 argocd-linux-amd64 /usr/local/bin/argocd
rm argocd-linux-amd64
```
Reference: [CLI installation](https://argo-cd.readthedocs.io/en/stable/cli_installation/)

Deploy App or Apps
```
└─$ argocd login localhost:8080
WARNING: server is not configured with TLS. Proceed (y/n)?            
Username: admin
Password:                                                                      
'admin:login' logged in successfully                                                                                                                                                                                                        
Context 'localhost:8080' updated                                                                        

argocd app create homelabapps \
    --project default \
    --dest-namespace argocd \
    --dest-server https://kubernetes.default.svc \
    --repo https://github.com/dmilet/homelab-deployments.git \
    --path apps  
```

![argocd_app-of-apps_1](pics/argocd_app-of-apps_1.png)



```
└─$ argocd app sync homelabapps
TIMESTAMP                  GROUP              KIND    NAMESPACE                  NAME    STATUS    HEALTH        HOOK  MESSAGE
2024-04-16T16:30:25-04:00  argoproj.io  Application     homelab     frontend-flaskapp  OutOfSync  Missing
2024-04-16T16:30:26-04:00  argoproj.io  Application     homelab     frontend-flaskapp  OutOfSync  Missing              application.argoproj.io/frontend-flaskapp created
2024-04-16T16:30:26-04:00  argoproj.io  Application     homelab     frontend-flaskapp    Synced  Missing              application.argoproj.io/frontend-flaskapp created

Name:               default/homelabapps
Project:            default
Server:             https://kubernetes.default.svc
Namespace:          homelab
URL:                https://argocd.example.com/applications/homelabapps
Repo:               https://github.com/dmilet/homelab-deployments.git
Target:                                                                                                                                                                         
Path:               apps                                        
SyncWindow:         Sync Allowed                                   
Sync Policy:        <none>                                        
Sync Status:        Synced to  (d695041)                             
Health Status:      Healthy                                        

Operation:          Sync                                        
Sync Revision:      d695041efd83e355d7ad2c4c172a183afd6b9647                                        
Phase:              Succeeded                                        
Start:              2024-04-16 16:30:25 -0400 EDT              
Finished:           2024-04-16 16:30:26 -0400 EDT              
Duration:           1s                                        
Message:            successfully synced (all tasks run)         

GROUP        KIND         NAMESPACE  NAME               STATUS  HEALTH  HOOK  MESSAGE
argoproj.io  Application  homelab    frontend-flaskapp  Synced                application.argoproj.io/frontend-flaskapp created
```
![argocd_app-of-apps_2](pics/argocd_app-of-apps_2.png)


Sync individual apps
```
argocd app sync -l argocd.argoproj.io/instance=homelabapps
```