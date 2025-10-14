FROM ubuntu

# Run runs the commands while creating the image
RUN apt-get update -y && \
 apt-get install -y curl

 CMD [ "/bin/bash" ]