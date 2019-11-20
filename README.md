# cs754-p3


# CloudLab k8s/Hadoop Cluster Setup Instructions

This process is intended for setting up experiments using the 'cs754-k8s' profile on CloudLab. (i.e. 1 Master, 2 Workers, all running Ubuntu 18.04 LTS)

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
5. run either </br>
        './setupK8s.sh <ssh_username>' to setup k8s </br>
    OR </br>
        './setupHadoop.sh <ssh_username>' to setup Hadoop </br>
    (when prompted with "SSH_PASSWORD:" enter passphrase for ssh key or leave blank if no passphrase was set.)


# Nuclio Instructions

## Setup 

Pre-req on k8s:
* setup k8s cluster based on instructions above

Pre-req on minikube: 
* install minikube 
* install hyperkit 
* install docker-machine-driver-hyperkit?? (not sure about this for non-macOS)

1. cd to 'setup/' directory
2. run either </br>
        './setupNuclio <docker_username> <docker_password>' to setup Nuclio on k8s </br>
    OR </br>
        './setupMiniNuclio' to setup Nuclio on minikube locally </br>
3. (optional) run './nuclioDash.sh' to expose Nuclio Dashboard at http://localhost:8070


## Deploying Function

Note: nuctl doesn't seem to be able to parse the 'meta.namespace' attribute in the function config file. Need to specify 
'--namespace nuclio' when deploying function via nuctl!!


# Hadoop Instructions

Visit http://<master_node_ip>:9870 to verify setup.






