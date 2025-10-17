export KRAFT_CLUSTER_ID=$(uuidgen | tr -d '-')
echo "$KRAFT_CLUSTER_ID"

create a network 

multipass exec swarm-mgr -- sudo docker network create -d overlay --attachable --opt encrypted kafka_net