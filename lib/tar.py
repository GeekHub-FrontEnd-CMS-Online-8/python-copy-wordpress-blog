#!/usr/bin/env python

from lib import ssh


def check_source_dir(parser, prod_section, prod_www_data_source):

    """ check if source directory exist
        [[ -d /var/www/html/aka-prod.rtfm.co.ua ]]
    """

    check_dir_cmd = "[[ -d " + prod_www_data_source + " ]]"
    stdin, stdout, stderr = ssh.ssh_exec(parser, prod_section, check_dir_cmd)
    source_dir_exist_status = stdout.channel.recv_exit_status()

    return source_dir_exist_status


def create_tgz(parser, prod_section, prod_www_data_source, tgz_path):

    """ create tgz archive from prod_www_data_source
        tar czf /home/admin/aka-prod.rtfm.co.ua.tgz --directory="/var/www/html/aka-prod.rtfm.co.ua" .
    """

    create_tgz_cmd = "tar czf " + tgz_path + " --directory=\"" + prod_www_data_source + "\" ."
    ssh.ssh_exec(parser, prod_section, create_tgz_cmd)


def check_tgz(parser, prod_section, tgz_path):

    """check tgz after create
       [[ -e /home/admin/aka-prod.rtfm.co.ua.tgz ]]
    """

    check_tgz_cmd = "[[ -e " + tgz_path + " ]]"
    stdin, stdout, stderr = ssh.ssh_exec(parser, prod_section, check_tgz_cmd)
    tar_exist_status = stdout.channel.recv_exit_status()

    return tar_exist_status


def create_www_data_archive(parser, prod_section, prod_www_data_source, tgz_path):

    # check remote dir exist
    source_dir_exist_status = check_source_dir(parser, prod_section, prod_www_data_source)

    if source_dir_exist_status == 0:
        print('OK: remote dir {} found...'.format(prod_www_data_source))
    else:
        print('ERROR: remote directory {} seems does not exist.\n'.format(prod_www_data_source))
        exit(1)

    print('Using tgz path {}...'.format(tgz_path))
    create_tgz(parser, prod_section, prod_www_data_source, tgz_path)

    # check tgz exist
    tar_exist_status = check_tgz(parser, prod_section, tgz_path)

    if tar_exist_status == 0:
        stdin, stdout, stderr = ssh.ssh_exec(parser, prod_section, "file " + tgz_path)
        print('Tar created: {}\n'.format(stdout.read().decode('ascii').strip("\n")))
    else:
        print('\nERROR: remote archive {} seems does not exist.\n'.format(tgz_path))
        exit(1)

def unpack_www_data_archive(parser, dev_section, tgz_path, dev_www_data_source):

    """ unpack tgz archive from dev_www_data_source
        tar xzf /home/admin/aka-dev.rtfm.co.ua.tgz --directory="/var/www/html/aka-dev.rtfm.co.ua" .
    """

    unpack_tgz_cmd = "sudo tar xzf " + tgz_path + " --directory=\"" + dev_www_data_source + "\""
    stdin, stdout, stderr = ssh.ssh_exec(parser, dev_section, unpack_tgz_cmd)
    tar_unpack_status = stdout.channel.recv_exit_status()

    if tar_unpack_status == 0:
        stdin, stdout, stderr = ssh.ssh_exec(parser, dev_section, "ls -l " + dev_www_data_source)
        print('\nDone: \n\n{}\n'.format(stdout.read().decode('ascii').strip("\n")))
    else:
        print('\nERROR: can\'t unpack.')
        exit(1)

