#!/usr/bin/env python2

import os

from lib import config
from lib import tar
from lib import ssh

"""

Config file example:

[production-source]
ssh-user = "user"
ssh-key = "/full/path/key.pem"
host = "aka-prod.rtfm.co.ua"
www-data-path = "/var/www/html/aka-prod.rtfm.co.ua"

[develop-dest]
ssh-user = "user"
ssh-key = "/full/path/key.pem"
host = "aka-dev.rtfm.co.ua"
www-data-path = "/var/www/html/aka-dev.rtfm.co.ua"

"""

parser = config.get_config('wp-clone-config.ini')

if __name__ == "__main__":

    prod_section = 'production-source'

    prod_ssh_user = parser.get(prod_section, 'ssh-user').strip('"')
    prod_ssh_key = parser.get(prod_section, 'ssh-key').strip('"')
    prod_host = parser.get(prod_section, 'host').strip('"')
    prod_www_data_source = parser.get(prod_section, 'www-data-path').strip('"')

    print('\nChecking [{}] config...\n'.format(prod_section))
    print('Using Prod SSH user: {}'.format(prod_ssh_user))
    print('Using Prod SSH key: {}'.format(prod_ssh_key))
    print('Using Prod server address: {}'.format(prod_host))
    print('Using Prod www data path: {}\n'.format(prod_www_data_source))

    dev_section = 'develop-dest'

    dev_ssh_user = parser.get(dev_section, 'ssh-user').strip('"')
    dev_ssh_key = parser.get(dev_section, 'ssh-key').strip('"')
    dev_host = parser.get(dev_section, 'host').strip('"')
    dev_www_data_source = parser.get(dev_section, 'www-data-path').strip('"')

    print('Checking [{}] config...\n'.format(dev_section))
    print('Using Dev SSH user: {}'.format(dev_ssh_user))
    print('Using Dev SSH key: {}'.format(dev_ssh_key))
    print('Using Dev server address: {}'.format(dev_host))
    print('Using Dev www data path: {}\n'.format(dev_www_data_source))

    # create removte archive
    # /home/admin/aka-prod.rtfm.co.ua.tgz
    remote_prod_tgz_path = "/home/" + prod_ssh_user + "/" + prod_host + ".tgz"
    tar.create_www_data_archive(parser, prod_section, prod_www_data_source, remote_prod_tgz_path)

    # download remote archive to local fs
    # /home/admin/aka-prod.rtfm.co.ua.tgz to local /tmp/aka-prod.rtfm.co.ua.tgz
    local_tgz_path = '/tmp/' + prod_host + ".tgz"
    print('Downloading www-data archive...')
    ssh.get_www_data_tgz(parser, prod_section, remote_prod_tgz_path, local_tgz_path)

    if os.path.isfile(local_tgz_path):
        print('Downloaded remote {} to local {}'.format(remote_prod_tgz_path, local_tgz_path))
    else:
        print('ERROR: can\'t download remote {} to local {}'.format(remote_prod_tgz_path, local_tgz_path))

    # upload local archive to remote Dev
    # /tmp/aka-prod.rtfm.co.ua.tgz to /home/admin/aka-dev.rtfm.co.ua.tgz
    remote_dev_tgz_path = "/home/" + dev_ssh_user + "/" + dev_host + ".tgz"
    print('\nUploading www-data archive...')
    ssh.put_www_data_tgz(parser, dev_section, local_tgz_path, remote_dev_tgz_path)
    print('Done.\n')

    # unpack /home/admin/aka-dev.rtfm.co.ua.tgz archive on Dev to /var/www/html/aka-dev.rtfm.co.ua
    print('Unpacking {} to {}...'.format(remote_dev_tgz_path, dev_www_data_source))
    tar.unpack_www_data_archive(parser, dev_section, remote_dev_tgz_path, dev_www_data_source)


