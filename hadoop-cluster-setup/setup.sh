ansible-playbook -i hosts --ask-pass ./playbooks/initial.yml --user $1
ansible-playbook -i hosts --ask-pass ./playbooks/setup_ssh.yml --user $1
ansible-playbook -i hosts --ask-pass ./playbooks/setup_hadoop.yml --user $1