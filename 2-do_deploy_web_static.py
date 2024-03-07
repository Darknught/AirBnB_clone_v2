#!/usr/bin/python3
""" A script that distributes archive to web servers """
from fabric.api import env, put, run
import os

env.hosts = ["35.168.3.169", "52.3.243.207"]


def do_deploy(archive_path):
    """ Function to distribute the archive """
    if not os.path.isfile(archive_path):
        print("Error: Archive path does not exist")
        return False

    filename = os.path.basename(archive_path)
    file_no_ext = os.path.splitext(filename)[0]

    if put(archive_path, '/tmp/{}'.format(filename)).failed:
        print("Error: failed to upload archive")
        return False

    commands = [
            "sudo rm -rf /data/web_static/releases/{}/".format(file_no_ext),
            "sudo mkdir -p /data/web_static/releases/{}/".format(file_no_ext),
            "sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(
                filename, file_no_ext),
            "sudo rm /tmp/{}".format(filename),
            "sudo mv /data/web_static/releases/{}/web_static/* "
            "/data/web_static/releases/{}/".format(file_no_ext, file_no_ext),
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
