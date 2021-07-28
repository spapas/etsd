from __future__ import with_statement
from fabric.api import env, cd, run, local, settings
import os


def black():
    "Run black"
    print("Running black...")
    local("black .")
    print("Black ok!")


def flake8():
    "Run flake8 checks"
    print("Check with flake8")
    local("flake8 .")
    print("flake8 ok!")


def commit():
    local("git add .")
    with settings(warn_only=True):
        local("git commit")
    with settings(warn_only=True):
        local("git push origin master")
    print("Commit ok")


def pull():
    with cd(env.directory):
        run("git fetch origin")
        run("git merge origin/master")
    print("fetch / merge ok")


def work():
    "Do work on server (copy settings, migrate and run collect static)"
    with cd(env.directory):
        requirements_txt = "requirements/" + env.env + ".txt"
        if os.stat(requirements_txt).st_size > 0:
            virtualenv("pip install -r {0}".format(requirements_txt))
        virtualenv("python manage.py migrate")
        virtualenv("python manage.py update_permissions")
        virtualenv("python manage.py collectstatic --noinput")
        if env.env == "prod":
            virtualenv("python manage.py compres")

def touch_wsgi():
    print("Restarting uwsgi")
    if env.env == "prod":
        run(r"cat /home/serafeim/aismanager/gunicorn.pid | xargs kill -HUP")


def full_deploy():
    "Reformat - check - commit - pull - do work - and restart uwsgi"
    black()
    flake8()
    commit()
    pull()
    work()
    touch_wsgi()


def virtualenv(command):
    run(env.activate + "&&" + command)


def uat():
    "UAT settings"
    env.env = "uat"
    env.user = "serafeim"
    env.hosts = ["uat1.hcg.gr"]
    env.directory = (
        "/home/serafeim/etsd/etsd"
    )
    env.activate = (
        "source /home/serafeim/etsd/venv/bin/activate"
    )


def prod():
    "PROD settings"
    env.env = "prod"
    env.user = "serafeim"
    env.hosts = [""]
    env.directory = (
        "/home/serafeim/etsd/etsd"
    )
    env.activate = (
        "source /home/serafeim/etsd/venv/bin/activate"
    )
