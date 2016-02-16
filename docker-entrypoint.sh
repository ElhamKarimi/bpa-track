#!/bin/bash

COMMAND=$1

# wait for a given host:port to become available
dockerwait() {
    host=$1
    port=$2
    while ! exec 6<>/dev/tcp/${host}/${port}
    do
        echo "$(date) - waiting to connect ${host} ${port}"
        sleep 5
    done
    echo "$(date) - connected to $host $port"

    exec 6>&-
    exec 6<&-
}


# wait for services to become available
# this prevents race conditions using fig
wait_for_services() {
    if [[ "$WAIT_FOR_QUEUE" ]] ; then
        dockerwait $QUEUESERVER $QUEUEPORT
    fi
    if [[ "$WAIT_FOR_DB" ]] ; then
        dockerwait $DBSERVER $DBPORT
    fi
    if [[ "$WAIT_FOR_CACHE" ]] ; then
        dockerwait $CACHESERVER $CACHEPORT
    fi
    if [[ "$WAIT_FOR_WEB" ]] ; then
        dockerwait $WEBSERVER $WEBPORT
    fi
}


defaults() {

    : ${ENV_PATH:="/env/bin"}

    : ${DBSERVER:="db"}
    : ${DBPORT:="5432"}
    : ${WEBSERVER="web"}
    : ${WEBPORT="8000"}
    : ${CACHESERVER="cache"}
    : ${CACHEPORT="11211"}

    : ${DBUSER="webapp"}
    : ${DBNAME="${DBUSER}"}
    : ${DBPASS="${DBUSER}"}

    . ${ENV_PATH}/activate

    export DBSERVER DBPORT DBUSER DBNAME DBPASS
}


django_defaults() {
    : ${DEPLOYMENT="dev"}
    : ${PRODUCTION=0}
    : ${DEBUG=1}
    : ${MEMCACHE="${CACHESERVER}:${CACHEPORT}"}
    : ${WRITABLE_DIRECTORY="/data/scratch"}
    : ${STATIC_ROOT="/data/static"}
    : ${MEDIA_ROOT="/data/static/media"}
    : ${LOG_DIRECTORY="/data/log"}
    : ${DJANGO_SETTINGS_MODULE="bpatrack.config.settings.production"}
    : ${DJANGO_MAILGUN_API_KEY:="NOTSET"}
    : ${DJANGO_MAILGUN_SERVER_NAME:="mg.ccgapps.com.au"}


    echo "DEPLOYMENT is ${DEPLOYMENT}"
    echo "PRODUCTION is ${PRODUCTION}"
    echo "DEBUG is ${DEBUG}"
    echo "MEMCACHE is ${MEMCACHE}"
    echo "WRITABLE_DIRECTORY is ${WRITABLE_DIRECTORY}"
    echo "STATIC_ROOT is ${STATIC_ROOT}"
    echo "MEDIA_ROOT is ${MEDIA_ROOT}"
    echo "LOG_DIRECTORY is ${LOG_DIRECTORY}"
    echo "DJANGO_SETTINGS_MODULE is ${DJANGO_SETTINGS_MODULE}"
    export DEPLOYMENT PRODUCTION DEBUG DBSERVER MEMCACHE WRITABLE_DIRECTORY STATIC_ROOT MEDIA_ROOT LOG_DIRECTORY DJANGO_SETTINGS_MODULE DJANGO_MAILGUN_API_KEY DJANGO_MAILGUN_SERVER_NAME
}

echo "HOME is ${HOME}"
echo "WHOAMI is $(whoami)"

defaults
django_defaults
wait_for_services

if [ "${COMMAND}" = 'nuclear' ]
then
    django-admin.py reset_db --router=default --traceback --settings=${DJANGO_SETTINGS_MODULE}
    django-admin.py migrate --traceback --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee /data/ingest.log
    exit $?
fi

if [ "${COMMAND}" = 'runscript' ]
then
    echo "Runscript $2"
    django-admin.py runscript $2 --traceback --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee /data/runscript.log
    exit $?
fi

if [ "${COMMAND}" = 'admin' ]
then
    echo "admin"
    if [ "$2" = "" ]
    then 
        admincmd="help"
    else
        admincmd=$2
    fi
    django-admin.py $admincmd --settings=${DJANGO_SETTINGS_MODULE}
    exit $?
fi

# set superuser 
if [ "${COMMAND}" = 'superuser' ]
then
    echo "Setting superuser (admin)"
    django-admin.py  createsuperuser --email="admin@ccg.com" --settings=${DJANGO_SETTINGS_MODULE}
    exit $?
fi

# security by django checksecure
if [ "$COMMAND" = 'checksecure' ]
then
    echo "[Run] Running Django checksecure"
    django-admin.py checksecure --traceback --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee /data/checksecure.log

    exit $?
fi

# uwsgi entrypoint
if [ "$COMMAND" = 'uwsgi' ]
then
    echo "[Run] Starting uwsgi"

    : ${UWSGI_OPTS="/app/uwsgi/docker.ini"}
    echo "UWSGI_OPTS is ${UWSGI_OPTS}"

    django-admin.py collectstatic --noinput --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee /data/uwsgi-collectstatic.log
    django-admin.py migrate --noinput --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee /data/uwsgi-migrate.log
    exec uwsgi --die-on-term --ini ${UWSGI_OPTS}
fi

# runserver entrypoint
if [ "$COMMAND" = 'runserver' ]
then
    echo "[Run] Starting runserver"

    : ${RUNSERVER_OPTS="runserver_plus 0.0.0.0:${WEBPORT} --settings=${DJANGO_SETTINGS_MODULE}"}
    echo "RUNSERVER_OPTS is ${RUNSERVER_OPTS}"

    echo "Django collectstatic"
    django-admin.py collectstatic --noinput --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee /data/runserver-collectstatic.log
    echo "Django migrate"
    django-admin.py migrate --noinput --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee /data/runserver-migrate.log
    
    echo "Django runserver"
    exec django-admin.py ${RUNSERVER_OPTS}
fi

# runtests entrypoint
if [ "$COMMAND" = 'runtests' ] 
then
    echo "Django test"
    cd /app/
    exec django-admin.py test --traceback --settings=${DJANGO_SETTINGS_MODULE}
fi

# lettuce entrypoint
if [ "$COMMAND" = 'lettuce' ]
then
    echo "[Run] Starting lettuce"
    exec django-admin.py run_lettuce --with-xunit --xunit-file=/data/tests.xml
fi

# prepare a tarball of build
if [ "$COMMAND" = 'tarball' ]
then
    echo "[Run] Preparing a tarball of build"

    cd /app
    rm -rf /app/*
    echo $GIT_TAG
    set -x
    git clone --depth=1 --branch=$GIT_TAG https://github.com/muccg/bpa-track.git .

    # install python deps
    # Note: Environment vars are used to control the bahviour of pip (use local devpi for instance)
    pip install ${PIP_OPTS} --upgrade -r requirements/production.txt
    pip install -e .
    set +x
    
    # create release tarball
    DEPS="/env /app/uwsgi /app/docker-entrypoint.sh /app/bpatrack"
    cd /data
    exec tar -cpzf bpatrack-${GIT_TAG}.tar.gz ${DEPS}
fi

echo "[RUN]: Builtin command not provided [lettuce|runtests|runserver|uwsgi|checksecure|superuser|nuclear|ingest|runscript]"
echo "[RUN]: $@"

exec "$@"
