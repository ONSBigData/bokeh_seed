#!/bin/bash

settings_file=$1
source $settings_file

cur_dir=`dirname $(readlink -f $BASH_SOURCE)`

cd $cur_dir/../
cp -r $DIRS_TO_DEPLOY "$DEPLOY_ROOT/"
cp $DEPLOY_FILES_LOCATION/* "$DEPLOY_ROOT/"

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




