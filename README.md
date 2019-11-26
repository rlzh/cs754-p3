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
        './setupK8s.sh <ssh_username>' to setup k8s 1.14.0 </br>
    OR </br>
        './setupHadoop.sh <ssh_username>' to setup Hadoop 3.1.3</br>
    (when prompted with "SSH_PASSWORD:" enter passphrase for ssh key or leave blank if no passphrase was set.)


# Nuclio

## Nuclio setup 

### Shared pre-reqs:
* install nuctl 1.2.2 
* install kubectl 1.14.0

### k8s only pre-reqs:
* setup k8s cluster based on instructions above

### minikube only pre-reqs:
* install minikube (working version 1.0.0. latest doesn't seem to work)
* install hyperkit (macOS) or virtualbox (linux)
* install docker-machine-driver-hyperkit?? (not sure about this for non-macOS)
* install rabbitmq 3+

### Steps
1. cd to 'setup/' directory
2. run either </br>
        './setupNuclio <docker_username> <docker_password>' to setup Nuclio on k8s </br>
    OR </br>
        './setupMiniNuclio <VM_DRIVER>' to setup Nuclio on minikube locally. '<VM_DRIVER>' should be 'hyperkit' (for macOS) or 'virtualbox' (for linux). </br>
3. add '<minikube_ip>:5000' to docker insecure registries and restart docker (see https://stackoverflow.com/questions/42211380/add-insecure-registry-to-docker)
4. create file 'nuclio/.env' and specify 'RMQ_HOST="<local/external network ip>"' for minikube OR 'RMQ_HOST="<master_node_ip>"' for k8s
5. (optional) run './nuclioDash.sh' to expose Nuclio Dashboard at http://localhost:8070
6. (only for k8s) run './setupRabbitMQ.sh <ssh_username>' to setup rabbitMQ server on master node. (visit http://<master_node_ip>:15672 for console. Login credentials [user: nuclio, password: nuclio] ) 

## Deploying function

Note: nuctl doesn't seem to be able to parse the 'meta.namespace' attribute in the function config file. Need to specify 
'--namespace nuclio' when deploying function via nuctl!!

## WordCount MapReduce

All settings related to MapReduce are found in 'nuclio/settings.py' and values are loaded from 'nuclio/.env' file at run time.

MapReduce functions can be deployed by executing 'nuclio/deploy.py'. (Run 'nuclio/deploy.py -h' for help)


# Hadoop

Visit http://<master_node_ip>:9870 to verify setup.






