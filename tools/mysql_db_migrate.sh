#!/bin/bash -e

yellow="\033[0;33m"
red="\033[0;31m"
nocolor="\033[0m"


function get_script_path() {
    local _src="${BASH_SOURCE[0]}"
    while [[ -h "${_src}" ]]; do
        local _dir="$(cd -P "$( dirname "${_src}" )" && pwd)"
        local _src="$(readlink "${_src}")"
        if [[ "${_src}" != /* ]]; then _src="$_dir/$_src"; fi
    done
    echo $(cd -P "$(dirname "$_src")" && pwd)
}

function cd_into_script_path() {
    local script_path=$(get_script_path)
    cd ${script_path}
}

function command_exists() {
    command -v "$@" 1> /dev/null 2>&1
}

function error_msg() {
    echo -e "${red}[ERROR] ${1-}${nocolor}"
}


# Main

(
cd_into_script_path
cd ..

if [[ ! -z "$(docker ps -f name=mysql_migrate -q)" ]]; then
  echo "stop mysql_migrate container..."
  docker stop mysql_migrate
fi

echo "mysql initialize..."
docker run -d --rm -p 3307:3306 --name mysql_migrate -e MYSQL_ROOT_PASSWORD=1234 -e MYSQL_DATABASE=test mysql:5.7.28
while ! mysqladmin ping -h"127.0.0.1" -P3307 --silent; do
  echo "mysql initialize..."
  sleep 1
done

export SQLALCHEMY_DATABASE_URI="mysql://root:1234@127.0.0.1:3307/test?charset=utf8"
export FLASK_APP=wsgi.py
flask db upgrade
flask db migrate
docker stop mysql_migrate
)
