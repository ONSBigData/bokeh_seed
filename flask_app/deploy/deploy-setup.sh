#!/bin/bash

cur_dir=`dirname $0`
source "$cur_dir/deploy-common.sh"

rm -rf $DEPLOY_ROOT
mkdir $DEPLOY_ROOT
cd $DEPLOY_ROOT
git init

heroku apps:destroy $APP_TITLE --confirm $APP_TITLE
heroku create $APP_TITLE --buildpack https://github.com/arose13/conda-buildpack.git
git remote add $APP_TITLE https://git.heroku.com/$APP_TITLE.git
