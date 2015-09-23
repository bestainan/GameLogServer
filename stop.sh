
PDIR=$PWD/apps
LDIR=$PWD/logs

echo ">> shutdown qq_car_pc on `hostname` ..."

for ((i=3316; i<=3316; i++))
do
  kill -9 `cat $LDIR/django-$i.pid`
  rm -rf -- "$LDIR/django-$i.pid"
done

log_file=$PWD/logs/new_rekoo.out
lsof -t $log_file | xargs -I{} kill -9 {}
#ps aux|grep python| grep zgame | grep runserver |grep -v grep |kill -9 `awk -F' ' '{print $2}'`

