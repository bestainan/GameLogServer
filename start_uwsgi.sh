#! /bin/bash
GAME_ERR_PATH="/opt/GameLogServer/logs/"

start_nginx(){
	echo "START NGINX....."
	if [ -f /etc/nginx/sites-enabled/game_nginx.conf ];
	then
		sudo rm /etc/nginx/sites-enabled/game_nginx.conf
	fi
	sudo ln -s /opt/GameLogServer/apps/game_nginx.conf /etc/nginx/sites-enabled/game_nginx.conf
	sudo service nginx start
}

start_uwsgi(){
	echo "START UWSGI....."
	sudo chmod -R 777 "$GAME_ERR_PATH"	
	
	if [ -f /etc/uwsgi/apps-enabled/game_wsgi.ini ];
	then
		sudo rm /etc/uwsgi/apps-enabled/game_wsgi.ini
	fi
	
	if [ -f /opt/GameLogServer/logs/.uwsgi_touch_restart ];
	then
		sudo touch /opt/GameLogServer/logs/.uwsgi_touch_restart
	fi
	
	sudo ln -s /opt/GameLogServer/apps/game_wsgi.ini /etc/uwsgi/apps-enabled/game_wsgi.ini
	sudo service uwsgi start
}

start_nginx && start_uwsgi

sudo netstat -ntlp
