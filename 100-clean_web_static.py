#!/usr/bin/python3
""" A fabfile script that cleans out-of-date archives """
from fabric.api import env, run, local
import os

env.hosts = ["35.168.3.169", "52.3.243.207"]


def do_clean(number=0):
    """ Deletes out-of-date archives """
    try:
        number = int(number)
        if number < 0:
            return False

        # Clean local archives
        local("ls -1t versions | tail -n +{} | xargs -I {{}} rm versions/{{}}"
              .format(number + 1))

        # Clean remote archives
        run("ls -1t /data/web_static/releases | tail -n +{} | xargs -I {{}}  rm -rf /data/web_static/releases/{{}}".format(number + 1))
        run("ls -1t /data/web_static | grep -v 'releases' | tail -n +{} | xargs -I {{}} rm -rf /data/web_static/{{}}".format(number + 1))

        return True
    except Exception as e:
        return False
