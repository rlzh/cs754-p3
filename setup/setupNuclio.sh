# playbooks based on https://github.com/nuclio/nuclio/blob/master/docs/setup/k8s/getting-started-k8s.md

export DOCKER_USER=$1
export DOCKER_PASS=$2

ansible-playbook -i hosts ./nuclio/nuclio.yml