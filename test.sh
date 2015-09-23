PDIR=$PWD/apps
LDIR=$PWD/logs
PYTHON=/usr/bin/python
IMPORT_TEST=import_test
SETTINGS=apps.settings.test
MANAGE=manage


#
if test $# -ne 1; then
    echo 'usage: ./test.sh port'
    exit 1
fi

port=$1

#Import test
check() {
echo "Start python check: import_test.py ..."
($PYTHON $PDIR/$IMPORT_TEST.py $SETTINGS)
}

#Fastcgi start
start() {
$PYTHON $PDIR/$MANAGE.py runserver --settings=$SETTINGS 0.0.0.0:$port
}

#Main
start

