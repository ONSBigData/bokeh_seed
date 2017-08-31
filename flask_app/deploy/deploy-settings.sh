#!/bin/bash

cur_dir=`dirname $0`

APP_TITLE='flask-app-seed'
DIRS_TO_DEPLOY="flask_app common"

DEPLOY_ROOT="$cur_dir/../../deploydir-$APP_TITLE"
DEPLOY_FILES_LOCATION=$cur_dir


