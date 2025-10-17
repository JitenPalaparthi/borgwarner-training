# manager
multipass launch 24.04 --name swarm-mgr --cpus 2 --memory 4G --disk 20G --cloud-init docker-ci.yaml

# worker
multipass launch 24.04 --name swarm-wkr1 --cpus 2 --memory 4G --disk 20G --cloud-init docker-ci.yaml