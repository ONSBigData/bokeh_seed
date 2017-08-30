#!/bin/bash

cur_dir=`dirname $0`
source "$cur_dir/deploy-common.sh"

# copy in some data to bundle with the app -----------------------------------
cp -r $cur_dir/../src/* "$DEPLOY_ROOT/"
cp "$cur_dir/Procfile" "$DEPLOY_ROOT/Procfile"

# deploy to Heroku -----------------------------------
cd $DEPLOY_ROOT

git add -A
dt=`date +"%Y-%m-%d_%H-%M"`
git commit -m "$dt"

if [[ $1 == 'local' ]]
then
    heroku local
else
    echo "deploying $APP_TITLE"
    git push $APP_TITLE master
    heroku open -a $APP_TITLE
fi




