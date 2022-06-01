sudo yum install httpd
cd /var/www/html/
sudo cat "<html><h1>Hello world!</h1></html>" > index.html
sudo service httpd start
chkconfig on
