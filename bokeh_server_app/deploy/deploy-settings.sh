#!/bin/bash

cur_dir=`dirname $(readlink -f $BASH_SOURCE)`

APP_TITLE='bokeh-server-app-seed'  # change this to a name of your choice
DIRS_TO_DEPLOY="bokeh_server_app common"

DEPLOY_ROOT="$cur_dir/../../deploydir-$APP_TITLE"
DEPLOY_FILES_LOCATION=$cur_dir

