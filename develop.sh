#!/bin/sh
# Script to control ${PROJECT_NAME} in dev and test

set -o nounset
set -o errexit

readonly TOPDIR=$(cd $(dirname $0); pwd)
readonly PROGNAME=$(basename $0)
readonly PROGDIR=$(readlink -m $(dirname $0))
readonly ARGS="$@"
readonly ACTION=$1
readonly DATE=$(date +%Y.%m.%d)

: ${PROJECT_NAME:='bpatrack'}
: ${DOCKER_BUILD_OPTIONS:="--pull=true"}


ci_docker_login() {
    if [ -n "$bamboo_DOCKER_USERNAME" ] && [ -n "$bamboo_DOCKER_EMAIL" ] && [ -n "$bamboo_DOCKER_PASSWORD" ]; then
        docker login  -e "${bamboo_DOCKER_EMAIL}" -u ${bamboo_DOCKER_USERNAME} --password="${bamboo_DOCKER_PASSWORD}"
    else
        echo "Docker vars not set, not logging in to docker registry"
    fi
}

pythonlint() {
   flake8 bpam --exclude=migrations,.ropeproject --ignore=E501,E303 --count
}


unit_tests() {
   mkdir -p data/tests
   chmod o+rwx data/tests
   docker-compose --project-name ${PROJECT_NAME} -f fig-test.yml up
}

up() {
   mkdir -p data/dev
   chmod o+rwx data/dev

   docker-compose --project-name ${PROJECT_NAME} up
}


selenium() {
   mkdir -p data/selenium
   chmod o+rwx data/selenium

   docker-compose --project-name ${PROJECT_NAME} -f fig-selenium.yml up
}


build() {
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
