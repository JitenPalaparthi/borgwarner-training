multipass exec swarm-mgr -- bash -lc 'ip -4 addr show ens3 | awk "/inet /{print \$2}"'
# Use that IP (e.g., 192.168.64.10) as the advertise address:

multipass exec swarm-mgr -- sudo docker swarm init --advertise-addr 192.168.64.9

# The output is 
# Swarm initialized: current node (1hit85pt67pf9ylc8q61dd3y5) is now a manager.

# To add a worker to this swarm, run the following command:

#     docker swarm join --token SWMTKN-1-3ldxtvnw6v8r0gncmq4ob8wnonfm6sv1jre840h553gwx6mw3n-7fs8gcvgwo1buonh9p6hvk76y 192.168.64.9:2377

# To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.

# can also have a look at the token 

multipass exec swarm-mgr -- sudo docker swarm join-token worker -q
# Or the full command:
multipass exec swarm-mgr -- sudo docker swarm join-token worker


multipass exec swarm-wkr1 -- sudo docker swarm join --token SWMTKN-1-3ldxtvnw6v8r0gncmq4ob8wnonfm6sv1jre840h553gwx6mw3n-7fs8gcvgwo1buonh9p6hvk76y 192.168.64.9:2377


## create a encrypted overlay network

multipass exec swarm-mgr -- sudo docker network create -d overlay --attachable --opt encrypted apps_net