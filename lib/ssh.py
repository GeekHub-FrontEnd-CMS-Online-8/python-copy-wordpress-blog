#!/usr/bin/env/python

import paramiko


def ssh_init(parser, env):

    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.connect(
        hostname=parser.get(env, 'host').strip('"'),
        username=parser.get(env, 'ssh-user').strip('"'),
        key_filename=parser.get(env, 'ssh-key').strip('"')
    )

    return client


def ssh_exec(parser, env, cmd):

    ssh_client = ssh_init(parser, env)

    return ssh_client.exec_command(cmd)


def get_www_data_tgz(parser, env, remote_file, local_file):

    ssh_client = ssh_init(parser, env)

    sftp = ssh_client.open_sftp()
    sftp.get(remote_file, local_file)
    sftp.close()


def put_www_data_tgz(parser, env, local_path, remote_file):

    ssh_client = ssh_init(parser, env)

    sftp = ssh_client.open_sftp()
    sftp.put(local_path, remote_file)
    sftp.close()
