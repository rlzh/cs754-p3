# playbooks based on https://sparkbyexamples.com/hadoop/apache-hadoop-installation/

ansible-playbook -i hosts --ask-pass ./hadoop/main.yml --user $1
