# cs754-p3


# Cloudlab K8s Cluster Setup Instructions

## Install sshpass

1. Extract 'sshpass.tar.gz' and cd into the directory
2. run './configure'
3. run 'sudo make install'

## Setup cluster

0. (optional) create virtualenv
1. cd to 'kube-cluster-setup/' dir
2. run 'pip install -r requirements.txt' 
3. update 'ansible_host' values in 'hosts' file
4. run './addHosts.sh' to add master & workers to ~/.ssh/known_hosts
5. run './setup.sh <ssh username>' to setup cluster 