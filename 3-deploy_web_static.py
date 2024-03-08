#!/usr/bin/python3
""" A script that creates and distributes archives """

from fabric.api import local, env, put, run
import os
from datetime import datetime

env.hosts = ["35.168.3.169", "52.3.243.207"]


def do_pack():
    """ The function to generate the .tgz archive """
    try:
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        local("mkdir -p versions")
        file_name = "versions/web_static_{}.tgz".format(now)
        local("tar -czvf {} web_static".format(file_name))
        return file_name
    except Exception as e:
        return None


def do_deploy(archive_path):
    """ Function to distribute the archive """
    if not os.path.exits(archive_path):
        return False

    try:
        filename = os.path.basename(archive_path)
        file_no_ext = os.path.splitext(filename)[0]

        if put(archive_path, '/tmp/{}'.format(filename)).failed:
            return False

        commands = [
                "sudo rm -rf /data/web_static/releases/{}/".format(
                    file_no_ext),

                "sudo mkdir -p /data/web_static/releases/{}/".format(
                    file_no_ext),

                "sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
                .format(filename, file_no_ext),

                "sudo rm /tmp/{}".format(filename),

                "sudo mv /data/web_static/releases/{}/web_static/* "
                "/data/web_static/releases/{}/".format(
                    file_no_ext, file_no_ext),

                "sudo rm -rf /data/web_static/releases/{}/web_static".format(
                    file_no_ext),

                "sudo rm -rf /data/web_static/current",

                "sudo ln -s /data/web_static/releases/{}/ "
                "/data/web_static/current".format(file_no_ext)

                ]

        for cmd in commands:
            if run(cmd).failed:
                print("Error: Command failed:", cmd)
                return False
        return True
    except Exception as e:
        print("Errr:", e)
        return False


def deploy():
    """ Create and dustribute the archive to web servers """
    archive_path = do_pack()
    if archive_path is None:
        return False

    return do_deploy(archive_path)
