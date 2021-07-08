# copy nginx_config files
if [ -z $1 ]; then
  PREFIX="dev-"
else
  PREFIX=""
fi

# uwsgi
for i in $(ls uwsgi/"${PREFIX}"*.ini); do
  echo setting up uwsgi $i
  # restarting uwsgi processes
  sudo uwsgi --stop /tmp/$(basename $i .ini).pid
  sudo uwsgi --uid $user --ini $i
done

# nginx
for i in $(ls nginx/"${PREFIX}"*.conf); do
  echo setting up nginx configuration $i
  # move new server config
  sudo mv $i /etc/nginx/sites-available/
  # enable new server config
  sudo rm /etc/nginx/sites-enabled/$(basename $i)
  sudo ln -s /etc/nginx/sites-available/$(basename $i) /etc/nginx/sites-enabled/
done
# restart nginx
sudo service nginx restart
