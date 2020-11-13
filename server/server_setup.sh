set -ex

# Copy and enable the daemon
cp server/vasegen.service /etc/systemd/system/vasegen.service

systemctl start numart
systemctl status numart
systemctl enable numart

# Setup the public facing server (NGINX)
apt install nginx

# CAREFUL HERE. If you are using default, maybe skip this
rm /etc/nginx/sites-enabled/default

cp server/vasegen.nginx /etc/nginx/sites-enabled/vasegen.nginx
update-rc.d nginx enable
service nginx restart


# Optionally add SSL support via Let's Encrypt:
# https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-18-04

# add-apt-repository ppa:certbot/certbot
# apt install python-certbot-nginx
# certbot --nginx -d vasegen.com
