set -ex

# Download fragments image directory
wget https://vasegen-matched-512.s3.us-east-2.amazonaws.com/latest_net_G.pth


# Copy and enable the daemon
sudo cp server/vasegen.service /etc/systemd/system/vasegen.service

sudo systemctl start vasegen
sudo systemctl status vasegen
sudo systemctl enable vasegen

# Setup the public facing server (NGINX)
sudo apt install nginx

# CAREFUL HERE. If you are using default, maybe skip this
# rm /etc/nginx/sites-enabled/default

sudo cp server/vasegen.nginx /etc/nginx/sites-enabled/vasegen.nginx
sudo update-rc.d nginx enable
sudo service nginx restart

# Optionally add SSL support via Let's Encrypt:
# https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-18-04

# add-apt-repository ppa:certbot/certbot
# apt install python-certbot-nginx
# certbot --nginx -d vasegen.com
