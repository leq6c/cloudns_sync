sudo yum install -y epel-release
sudo yum install -y python-pip --enablerepo=epel
sudo yum install -y python3
pip3 install -r requirements.txt
mkdir -p /etc/cloudns_sync/
