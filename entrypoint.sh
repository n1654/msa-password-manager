#!/bin/sh

# INSTALL PYTHON LIBRARIES
pip3 install Flask

# CONFIGURE OPENSSH
echo -e "Port 22\n\
AddressFamily any\n\
ListenAddress 0.0.0.0\n\
PermitRootLogin yes\n\
PasswordAuthentication yes" >> /etc/ssh/sshd_config

# CHANGE ROOT PASSWORD
echo root:root123 | chpasswd

# GENERATE KEYS
/usr/bin/ssh-keygen -A
ssh-keygen -t rsa -b 4096 -f  /etc/ssh/ssh_host_key

# RUN WEB API
/start/main.py &

# RUN SSH SERVER
/usr/sbin/sshd -D
