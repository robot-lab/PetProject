#!/bin/bash
if [[ "$TRAVIS_BRANCH" = "$STAGING_BRANCH" ]]
then
    if [[ "$TRAVIS_PULL_REQUEST" != false ]]
    then
        HEROKU_APP_NAME="$HEROKU_APP_NAME-debug"
    else
        HEROKU_APP_NAME="$HEROKU_APP_NAME-staging"
    fi
    wget -qO- https://toolbelt.heroku.com/install-ubuntu.sh | sh
    heroku container:login
    heroku create $HEROKU_APP_NAME
    heroku container:push web -a $HEROKU_APP_NAME
    heroku container:release web -a $HEROKU_APP_NAME
fi