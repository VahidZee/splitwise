# copy nginx_config files
if [ -z $2 ]; then
  PREFIX="dev-"
else
  PREFIX=""
fi
if [ -z $1 ]; then
  echo "Specify branch name in the first argument"
fi

# setup .env variables
printenv >~/$PREFIX$1/.env

# setup django
# exporting environmental variables
set -a
source ~/venvs/$PREFIX$1/bin/activate
pip install -r ../backend/requirements.txt
python ../backend/manage.py collectstatic --no-input
python ./backend/manage.py migrate --no-input
deactivate

# uwsgi
for i in $(ls uwsgi/"${PREFIX}"*.ini); do
  echo setting up uwsgi $i
  # restarting uwsgi processes
  sudo uwsgi --stop /tmp/$(basename $i .ini).pid
  sudo uwsgi --ini $i --uid $USER
done

# nginx
for i in $(ls nginx/"${PREFIX}"*.conf); do
  echo setting up nginx configuration $i
  # move new server config
  sudo yes | cp $i /etc/nginx/sites-available/
  # enable new server config
  sudo rm /etc/nginx/sites-enabled/$(basename $i)
  sudo ln -s /etc/nginx/sites-available/$(basename $i) /etc/nginx/sites-enabled/
done
# restart nginx
sudo service nginx restart
