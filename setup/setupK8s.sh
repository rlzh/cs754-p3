# playbooks based on https://www.digitalocean.com/community/tutorials/how-to-create-a-kubernetes-cluster-using-kubeadm-on-ubuntu-18-04

ansible-playbook -i hosts --ask-pass ./k8s/main.yml --user $1