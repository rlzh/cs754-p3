# cs754-p3


# CloudLab K8s Cluster/Hadoop Setup Instructions

This process is intended for setting up experiments using the 'cs754-k8s' profile on CloudLab

To begin first cd to 'setup/' directory

## Install sshpass

1. Extract 'sshpass.tar.gz' and cd into the directory
2. run './configure'
3. run 'sudo make install'

## Setup cluster

0. (optional) create virtualenv
1. cd to 'setup/' dir
2. run 'pip install -r requirements.txt' 
3. update 'ansible_host' values in 'hosts' file
4. run './addHosts.sh' to add master & workers to ~/.ssh/known_hosts
5. run either 
        './setupK8s.sh <ssh_username>' to setup k8s 
    OR  
        './setupHadoop.sh <ssh_username>' to setup hadoop

# K8s

# Hadoop

Visit http://<master_node_ip>:9870 

