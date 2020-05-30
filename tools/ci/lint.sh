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
if ! command_exists flake8; then
    error_msg "Install flake8 first.
pip install flake8==3.6.0"
    exit 1
fi

(
cd_into_script_path
cd ../..

flake8 --exclude='venv*,migrations' --max-line-length=127 --show-source --statistics
)
