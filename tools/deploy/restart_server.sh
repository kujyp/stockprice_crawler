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

function info_msg() {
    echo -e "${yellow}[INFO] ${1-}${nocolor}"
}

function error_msg() {
    echo -e "${red}[ERROR] ${1-}${nocolor}"
}

function usage() {
    info_msg "Usage:
$0 --port 80 --docker-tag latest --mysql-account root --mysql-password 1111 --mysql-host 192.168.1.1 --mysql-port 3306 --mysql-database dbname
$0 --port 8000 --docker-tag develop-latest --mysql-account root --mysql-password 1111 --mysql-host 192.168.1.1 --mysql-port 3306 --mysql-database test
"
}


# Main
while true; do
    if [[ $# -eq 0 ]]; then
        break
    fi

    case $1 in
        --port)
            shift

            case $1 in (-*|"") usage; exit 1; esac
            port="$1"
            shift; continue
            ;;
        --docker-tag)
            shift

            case $1 in (-*|"") usage; exit 1; esac
            docker_tag="$1"
            shift; continue
            ;;
        --mysql-account)
            shift

            case $1 in (-*|"") usage; exit 1; esac
            mysql_account="$1"
            shift; continue
            ;;
        --mysql-password)
            shift

            case $1 in (-*|"") usage; exit 1; esac
            mysql_password="$1"
            shift; continue
            ;;
        --mysql-host)
            shift

            case $1 in (-*|"") usage; exit 1; esac
            mysql_host="$1"
            shift; continue
            ;;
        --mysql-port)
            shift

            case $1 in (-*|"") usage; exit 1; esac
            mysql_port="$1"
            shift; continue
            ;;
        --mysql-database)
            shift

            case $1 in (-*|"") usage; exit 1; esac
            mysql_database="$1"
            shift; continue
            ;;
    esac
    shift
done

if [[ -z ${port} ]] || [[ -z ${docker_tag} ]] || [[ -z ${mysql_account} ]] || [[ -z ${mysql_password} ]] || [[ -z ${mysql_host} ]] || [[ -z ${mysql_port} ]] || [[ -z ${mysql_database} ]]; then
    usage
    exit 1
fi

/usr/local/bin/docker pull kujyp/stockprice_crawler:"$docker_tag"
if [[ ! -z "$(/usr/local/bin/docker ps -f name=^stockprice_crawler$ -q)" ]]; then
  /usr/local/bin/docker stop stockprice_crawler
  sleep 2
fi


/usr/local/bin/docker run -d --rm -p "$port":80 -e SQLALCHEMY_DATABASE_URI="mysql://${mysql_account}:${mysql_password}@${mysql_host}:${mysql_port}/${mysql_database}?charset=utf8" --name stockprice_crawler kujyp/stockprice_crawler:"$docker_tag"
