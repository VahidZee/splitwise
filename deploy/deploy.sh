# copy nginx_config files
if [ -z $1 ]; then
  echo "Specify branch name in the first argument"
  exit
fi
BRANCH_NAME=$1
# setup .env variables
printenv >~/$BRANCH_NAME/.env

# setup django
# exporting environmental variables
set -a
source ~/venvs/$BRANCH_NAME/bin/activate
pip install -U pip
pip install -r ../backend/requirements.txt
python ../backend/manage.py collectstatic --no-input
python ../backend/manage.py migrate --no-input
deactivate

# uwsgi
for i in $(ls uwsgi/"${BRANCH_NAME}"*.ini); do
  echo setting up uwsgi $i
  # restarting uwsgi processes
  sudo uwsgi --stop /tmp/$(basename $i .ini).pid
  sudo uwsgi --ini $i --uid $USER
done

# nginx
for i in $(ls nginx/"${BRANCH_NAME}"*.conf); do
  echo setting up nginx configuration $i
  # create media and static files directory
  sudo mkdir -p /var/files/$BRANCH_NAME
  sudo chown -R 777 /var/files/$BRANCH_NAME
  # move new server config
  sudo yes | cp $i /etc/nginx/sites-available/
  # enable new server config
  sudo rm /etc/nginx/sites-enabled/$(basename $i)
  sudo ln -s /etc/nginx/sites-available/$(basename $i) /etc/nginx/sites-enabled/
done
# restart nginx
sudo service nginx restart
