#!/bin/bash
# Script to control ${PROJECT_NAME} in dev and test

readonly PROJECT_NAME='bpatrack'
readonly TOPDIR=$(cd $(dirname $0); pwd)
readonly PROGNAME=$(basename $0)
readonly PROGDIR=$(readlink -m $(dirname $0))
readonly ARGS="$@"
readonly ACTION=$1
readonly DATE=$(date +%Y.%m.%d)


VIRTUALENV="${HOME}/virt_${PROJECT_NAME}"
: ${DOCKER_BUILD_OPTIONS:="--pull=true"}


######### Logging ##########
readonly COLOR_NORMAL=$(tput sgr0)
readonly COLOR_RED=$(tput setaf 1)
readonly COLOR_YELLOW=$(tput setaf 3)
readonly COLOR_GREEN=$(tput setaf 2)

log_error() {
    echo ${COLOR_RED}ERROR: $* ${COLOR_NORMAL}
}

log_warning() {
    echo ${COLOR_YELLOW}WARNING: $* ${COLOR_NORMAL}
}

log_success() {
    echo ${COLOR_GREEN}SUCCESS: $* ${COLOR_NORMAL}
}

log_info() {
    echo INFO: $*
}

# no news is good news
log() {
    local error_code=$0
    local message=$1

    if [ ${error_code} != 0 ]
    then
        log_warning ${message}
    else
        log_success ${message}
    fi
 }

set -e
activate_virtualenv() {
   if [ ! -d ${VIRTUALENV} ]
   then
        log_warning "There is no ${VIRTUALENV} here, making it."
        virtualenv ${VIRTUALENV}
        . ${VIRTUALENV}/bin/activate
        # there's little point in ensuring docker-compose is available if docker 
        # isn't
        # pip install docker-compose
        pip install 'flake8>=2.0,<2.1'
   else
      source ${VIRTUALENV}/bin/activate
   fi
}

pythonlint() {
    activate_virtualenv
    # find . -type d -name ".ropeproject" -exec rm -fr {} \;
    ${VIRTUALENV}/bin/flake8 bpam --exclude=migrations,.ropeproject --ignore=E501,E303 --count
}


unit_tests() {
    activate_virtualenv

    mkdir -p data/tests
    chmod o+rwx data/tests
    docker-compose --project-name ${PROJECT_NAME} -f fig-test.yml up
}

up() {
    activate_virtualenv
    mkdir -p data/dev
    chmod o+rwx data/dev

    docker-compose --project-name ${PROJECT_NAME} up
}


selenium() {
    activate_virtualenv
    mkdir -p data/selenium
    chmod o+rwx data/selenium

    docker-compose --project-name ${PROJECT_NAME} -f fig-selenium.yml up
}


build() {
   activate_virtualenv
   docker-compose --project-name ${PROJECT_NAME} build
}

rm_containers() {
   docker-compose --project-name ${PROJECT_NAME} rm
}

entrypoint() {
   local entrypoint=${1:-bash}
   log_info "Entrypoint ${entrypoint}"
   docker exec -it ${PROJECT_NAME}_web_1 ${entrypoint} $2
}


dockerbuild() {
   log_info "Building containers"
   activate_virtualenv

   local image="muccg/${PROJECT_NAME}"
   local gitbranch=$(git rev-parse --abbrev-ref HEAD 2> /dev/null)
   local gittag=$(git describe --abbrev=0 --tags 2> /dev/null)

   # only use tags when on master (release) branch
   if [ ${gitbranch} != "master" ]
   then
      log_info "Ignoring tags, not on master branch"
      gittag=$gitbranch
   fi

   # if no git tag, then use branch name
   if [ -z ${gittag+x} ]
   then
      log_info "No git tag set, using branch name"
      gittag=$gitbranch
   fi

   log_info "Building ${PROJECT_NAME} ${gittag}"

   # attempt to warm up docker cache
   docker pull ${image} || true

   local tag
   for tag in "${image}:${gittag}" "${image}:${gittag}-${DATE}"
   do
      echo "Building tag ${PROJECT_NAME} ${tag}"
      set -x
      docker build ${DOCKER_BUILD_OPTIONS} --build-arg GIT_TAG=${gittag} -t ${tag} -f Dockerfile.release .
      docker push ${tag}
      set +x
   done
}


usage() {
cat << EOF
Usage: ${PROGNAME} options

Wrapper script to call common tools while developing ${PROJECT_NAME}

OPTIONS:
       build       Build all images
       dockerbuild Build and push new docker images from current checked out tag
       shell       Create and shell into a new web image, used for db checking with Django env available
       superuser   Create Django superuser
       runscript   Run one of the available scripts
       checksecure Run security check
       up          Spins up docker development stack
       rm          Remove all containers
       pythonlint  Run python lint
       unit_tests  Run unit tests
       selenium    Run selenium tests
       usage       Print this usage

Examples:
       ${PROGNAME} build
       ${PROGNAME} rm
EOF
}

case ${ACTION} in
pythonlint)
    pythonlint
    ;;
ci_staging)
    ci_ssh_agent
    ci_staging
    ;;
start)
    up
    ;;
build)
    build
    ;;
dockerbuild)
    dockerbuild
    ;;
rm)
    rm_containers
    ;;
clean)
    clean
    ;;
up)
    up
    ;;
shell)
    docker exec -it ${PROJECT_NAME}_web_1 /bin/bash
    ;;
admin)
    docker exec -it ${PROJECT_NAME}_web_1 /app/docker-entrypoint.sh admin $2
    ;;
superuser)
    docker exec -it ${PROJECT_NAME}_web_1 /app/docker-entrypoint.sh superuser
    ;;
runscript)
    docker exec -it ${PROJECT_NAME}_web_1 /app/docker-entrypoint.sh runscript $2
    ;;
nuclear)
    docker exec -it ${PROJECT_NAME}_web_1 /app/docker-entrypoint.sh nuclear
    ;;
checksecure)
    docker exec -it ${PROJECT_NAME}_web_1 /app/docker-entrypoint.sh checksecure
    ;;
*)
    usage
esac
