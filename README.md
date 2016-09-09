[![Build Status](https://travis-ci.org/alphagov/notifications-admin.svg)](https://travis-ci.org/alphagov/notifications-admin)
[![Requirements Status](https://requires.io/github/alphagov/notifications-admin/requirements.svg?branch=master)](https://requires.io/github/alphagov/notifications-admin/requirements/?branch=master)
[![Coverage Status](https://coveralls.io/repos/alphagov/notifications-admin/badge.svg?branch=master&service=github)](https://coveralls.io/github/alphagov/notifications-admin?branch=master)

[![Deploy to staging](https://notify-build-monitor.herokuapp.com/deploys/notifications-admin/master...staging.svg?prefix=Deploy%20to)](https://github.com/alphagov/notifications-admin/compare/staging...master?expand=1&title=Deploy%20to%20staging) [![Deploy to live](https://notify-build-monitor.herokuapp.com/deploys/notifications-admin/staging...live.svg?prefix=Deploy%20to)](https://github.com/alphagov/notifications-admin/compare/live...staging?expand=1&title=Deploy%20to%20live)

# notifications-admin

GOV.UK Notify admin application.

## Features of this application

 - Register and manage users
 - Create and manage services
 - Send batch emails and SMS by uploading a CSV
 - Show history of notifications

## First-time setup

Brew is a package manager for OSX. The following command installs brew:
```shell
    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

Languages needed
- Python 3.4
- [Node](http://nodejs.org/) 5.0.0 or greater
```shell
    brew install node
```

[NPM](npmjs.org) is Node's package management tool. `n` is a tool for managing
different versions of Node. The following installs `n` and uses the latest
version of Node.
```shell
    npm install -g n
    n latest
    npm rebuild node-sass
```

The app runs within a virtual environment. We use mkvirtualenv for easier working with venvs
```shell
    pip install virtualenvwrapper
    mkvirtualenv -p /usr/local/bin/python3 notifications-admin
```

Install dependencies and build the frontend assets:
```shell
    workon notifications-admin
    ./scripts/bootstrap.sh
```

## Rebuilding the frontend assets

If you want the front end assets to re-compile on changes, leave this running
in a separate terminal from the app
```shell
    npm run watch
```

## Create a local environment.sh file containing the following:

```
echo "
export NOTIFY_ENVIRONMENT='development'
export ADMIN_CLIENT_SECRET='notify-secret-key'
export API_HOST_NAME='http://localhost:6011'
export DANGEROUS_SALT='dev-notify-salt'
export SECRET_KEY='notify-secret-key'
export DESKPRO_API_HOST="some-host"
export DESKPRO_API_KEY="some-key"
"> environment.sh
```

## AWS credentials

Your aws credentials should be stored in a folder located at `~/.aws`. Follow [Amazon's instructions](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html#cli-config-files) for storing them correctly


## Generate the application version file

```shell
    make generate-version-file
```

## Running the application

```shell
    workon notifications-admin
    ./scripts/run_app.sh
```

Then visit [localhost:6012](http://localhost:6012)
