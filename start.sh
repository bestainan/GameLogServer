PDIR=$PWD/apps
LDIR=$PWD/logs
PYTHON=/usr/bin/python
IMPORT_TEST=import_test
SETTINGS=apps.settings.test
MANAGE=manage

#Fastcgi start
start() {
nohup $PYTHON $PDIR/$MANAGE.py runserver --settings=$SETTINGS 0.0.0.0:8083  > $LDIR/new_rekoo.out 2>&1 &
}

#Main
start
