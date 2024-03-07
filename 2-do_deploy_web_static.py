#!/usr/bin/python3
""" A script that distributes archive to web servers """
from fabric.api import env, put, run
import os


env.user = 'ubuntu'
env.key_filename = /.ssh/school
env.hosts = ["35.168.3.169", "52.3.243.207"]


def do_deploy(archive_path):
    """ Function to distribute the archive """
    if not os.path.exists(archive_path):
        print("Error: Archive path does not exist")
        return False

    try:
        # Upload the archive to /tmp/ directory on the web servers
        put(archive_path, '/tmp/')

        # extract archive to /data/web_static/releases/arc filename no ext
        filename = os.path.basename(archive_path)
        file_no_ext = os.path.splitext(file_name)[0]
        run("sudo mkdir -p /data/web_static/releases/{}".format(file_no_ext))
        run("sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(
            file_name, file_no_ext))

        # Delete the uploaded archive
        run("sudo rm /tmp/{}".format(file_name))

        # Delete the symbolic link /data/web_static/current
        run("sudo rm -rf /data/web_static/current")

        # Create a new symbolic link linked to the new version of the code
        run("sudo ln -s /data/web_static/releases/{}/ "
            "/data/web_static/current".format(file_no_ext))

        return True
    except Exception as e:
        print("Error:", e)
        return False
