ansible-playbook -i hosts --ask-pass ./hadoop/initial.yml --user $1
ansible-playbook -i hosts --ask-pass ./hadoop/setup_ssh.yml --user $1
ansible-playbook -i hosts --ask-pass ./hadoop/setup_hadoop.yml --user $1