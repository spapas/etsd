from __future__ import with_statement
from fabric.api import env, cd, run, local, settings
import os

from etsd.settings.local import FAB_PROXY, UAT_HOSTS, PROD_HOSTS


def black():
    "Run black"
    print("Running black...")
    local("black .")
    print("Black ok!")


def commit():
    local("git add .")
    with settings(warn_only=True):
        local("git commit")
    with settings(warn_only=True):
        local("git push origin master")
    print("Commit ok")


def pull():
    with cd(env.directory):
        run("https_proxy={0} git fetch origin".format(FAB_PROXY))
        run("git merge origin/master")
    print("fetch / merge ok")


def work():
    "Do work on server (copy settings, migrate and run collect static)"
    with cd(env.directory + "/etsd/branding"):
        run("https_proxy={0} git fetch origin".format(FAB_PROXY))
        run("git merge origin/master")

    with cd(env.directory):
        requirements_txt = "requirements/" + env.env + ".txt"
        if os.stat(requirements_txt).st_size > 0:
            virtualenv(
                "https_proxy={0} pip install -r {1}".format(FAB_PROXY, requirements_txt)
            )
        virtualenv("python manage.py migrate")
        virtualenv("python manage.py update_permissions")
        virtualenv("python manage.py collectstatic --noinput")
        virtualenv("python manage.py compress")


def touch_wsgi():
    print("Restarting uwsgi")
    if env.env == "prod":
        run(r"cat /home/serafeim/etsd/gunicorn.pid | xargs kill -HUP")


def full_deploy():
    "Reformat - commit - pull - do work - and restart gunicorn"
    black()
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
    env.hosts = UAT_HOSTS
    env.directory = "/home/serafeim/etsd/etsd"
    env.activate = "source /home/serafeim/etsd/venv/bin/activate"


def prod():
    "PROD settings"
    env.env = "prod"
    env.user = "serafeim"
    env.hosts = PROD_HOSTS
    env.directory = "/home/serafeim/etsd/etsd"
    env.activate = "source /home/serafeim/etsd/venv/bin/activate"
