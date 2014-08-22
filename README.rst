Mesos-Master Install:

$ sudo apt-key adv --keyserver keyserver.ubuntu.com --recv E56151BF
$ DISTRO=$(lsb_release -is | tr '[:upper:]' '[:lower:]')
$ CODENAME=$(lsb_release -cs)
$ echo "deb http://repos.mesosphere.io/${DISTRO} ${CODENAME} main" |  sudo tee /etc/apt/sources.list.d/mesosphere.list
$ sudo apt-get -y update
$ sudo apt-get -y install mesos marathon

# so mesos-slave doesn't start on this node
echo 'manual' > /etc/init/mesos-slave.override


Mesos-Slave Install:

$ sudo apt-key adv --keyserver keyserver.ubuntu.com --recv E56151BF
$ DISTRO=$(lsb_release -is | tr '[:upper:]' '[:lower:]')
$ CODENAME=$(lsb_release -cs)
$ echo "deb http://repos.mesosphere.io/${DISTRO} ${CODENAME} main" |  sudo tee /etc/apt/sources.list.d/mesosphere.list
$ sudo apt-get -y update
$ sudo apt-get -y install mesos deimos


# so mesos-master doesn't start on this node
$ echo 'manual' > /etc/init/mesos-master.override

# we don't need zookeeper on the slave nodes
$ dpkg --purge zookeeper zookeeperd

Install Docker:
https://docs.docker.com/installation/ubuntulinux/#ubuntu-trusty-1404-lts-64-bit

$ sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 36A1D7869245C8950F966E92D8576A8BA88D21E9
$ sudo sh -c "echo deb https://get.docker.io/ubuntu docker main\
> /etc/apt/sources.list.d/docker.list"
$ sudo apt-get update
$ sudo apt-get install lxc-docker

Configure Mesos-slave:

HOSTNAME=`ifconfig eth0 | grep "inet addr" | awk -F: '{print $2}' | awk '{print $1}'`

cat << EOF > /etc/default/mesos-slave
MASTER=MASTER_IP:5050
hostname=$HOSTNAME
EOF

echo /usr/local/bin/deimos | sudo tee /etc/mesos-slave/containerizer_path
echo external | sudo tee /etc/mesos-slave/isolation


# db 
create database mesos; 
GRANT ALL PRIVILEGES ON mesos.* TO 'mesos'@'%' IDENTIFIED BY 'mesos';


# deploy demo
curl -X POST -H "Content-Type: application/json" http://10.0.0.4:8080/v2/apps -d @demo.json

