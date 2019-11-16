ansible-playbook -i hosts --ask-pass ./k8s/initial.yml --user $1
ansible-playbook -i hosts --ask-pass ./k8s/master.yml --user $1
ansible-playbook -i hosts --ask-pass ./k8s/workers.yml --user $1