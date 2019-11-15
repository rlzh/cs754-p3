ansible-playbook -i hosts --ask-pass ./playbooks/initial.yml --user $1
ansible-playbook -i hosts --ask-pass ./playbooks/master.yml --user $1
ansible-playbook -i hosts --ask-pass ./playbooks/workers.yml --user $1