import subprocess
from datetime import datetime

from flask import Blueprint

home_api = Blueprint('views.home', __name__)


def get_commit_rev() -> str:
    return check_output_wrapper("git rev-parse --short=8 HEAD")


def check_output_wrapper(cmd: str) -> str:
    return subprocess.check_output(cmd.split(' ')).decode().strip()


def get_last_commit_datetime() -> datetime:
    return datetime.strptime(check_output_wrapper(
        "git show --no-patch --no-notes --pretty=%cd " + get_commit_rev()
    ), "%a %b %d %X %Y %z")


@home_api.route("/")
def index():
    version = get_commit_rev()
    github_commit_link = f"https://github.com/kujyp/stockprice_crawler/commit/{version}"
    return f"""\
Version(Git rev): <a href="{github_commit_link}">{version}</a>\
({get_last_commit_datetime().strftime("%Y-%m-%d %X %z")})"""
