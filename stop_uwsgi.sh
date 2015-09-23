#! /bin/bash
stop_nginx(){
	echo "STOP NGINX....."	
	sudo service nginx stop
}

stop_uwsgi(){
	echo "STOP UWSGI....."
	sudo service uwsgi stop
}

stop_uwsgi && stop_nginx

sudo netstat -ntlp
