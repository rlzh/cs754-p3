# playbook based on https://computingforgeeks.com/how-to-install-latest-rabbitmq-server-on-ubuntu-18-04-lts/

ansible-playbook -i hosts --ask-pass ./rabbitmq/rabbitmq.yml --user $1