# Entrar no vm

- Utilizador: rasbet
- utilizar id_rsa como private key
- ssh -i id_rsa rasbet@rasbet.duckdns.org

# commands

- sudo apt update
- sudo apt upgrade
- sudo apt install wget
- wget https://dev.mysql.com/get/mysql-apt-config_0.8.20-1_all.deb
- sudo dpkg -i mysql-apt-config_0.8.20-1_all.deb
- sudo apt-get update
- sudo apt-get install mysql-server
- mysql -u root -p
- sudo apt install git
- git clone https://github.com/MrZeLee/RASBet.git
- sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev curl libbz2-dev
- curl -O https://www.python.org/ftp/python/3.8.12/Python-3.8.12.tar.xz
- tar -xf Python-3.8.12.tar.xz
- cd Python-3.8.12
- ./configure --enable-optimizations
- make -j 4
- sudo make altinstall
- cd ../RASBet/
- python3.8 -m venv .
- pip3.8 install pipenv
- source bin/activate
- sudo apt install default-libmysqlclient-dev
- pipenv install

- mkdir ~/duckdns
- echo "echo url=\"https://www.duckdns.org/update?domains=rasbet&token=b1c9464c-96ae-4f21-bc91-dd466b8670ae&ip=\" | curl -k -o ~/duckdns/duck.log -K -" > ~/duckdns/duck.sh
- chmod 700 ~/duckdns/duck.sh
- line="*/5 * * * * /home/rasbet/duckdns/duck.sh >/dev/null 2>&1"
- (crontab -u $(whoami) -l; echo "$line" ) | crontab -u $(whoami) -