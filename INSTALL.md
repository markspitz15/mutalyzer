Mutalyzer installation instructions
===================================


Default configuration notes
---------------------------

The instructions in this file are quite specific to the standard Mutalyzer
environment. This consists of a Debian stable (Squeeze) system with Apache
and Mutalyzer using its mod_wsgi module. Debian conventions are used
throughout.

The following is an overview of default locations used by Mutalyzer:

    Package files           /usr/local/lib/python2.6/dist-packages/...
    Configuration           /etc/mutalyzer/config
    Log file                /var/log/mutalyzer.log
    Cache directory         /var/cache/mutalyzer
    Batchd init script      /etc/init.d/mutalyzer-batchd
    Mapping update crontab  /etc/cron.d/mutalyzer-mapping-update
    Apache configuration    /etc/apache2/conf.d/mutalyzer.conf
    Static website files    /var/www/mutalyzer/base

The default database user is 'mutalyzer' with no password and the database
names are 'mutalyzer', 'hg18', and 'hg19'.

By default, Mutalyzer is exposed under the '/mutalyzer' url by Apache.

All Mutalyzer processes run under the www-data user and files created and/or
modified by Mutalyzer are owned by this user.

If you have a different environment, or want to customize the default
locations, you can read through these instructions and modify them to your
needs.


Short version
-------------

Run the following commands:

    git clone https://git.lumc.nl/mutalyzer/mutalyzer
    cd mutalyzer
    sudo bash extras/pre-install.sh
    sudo python setup.py install
    sudo bash extras/post-install.sh
    sensible-browser http://localhost/mutalyzer

Or follow the more detailed instructions below.


Automated deployment on a remote host
-------------------------------------

For deploying Mutalyzer on a remote (production or testing) host, we recommend
to automate the steps described below by using Fabric and the included
fabfile. You need Fabric installed on your local machine:

    easy_install fabric

To do a deployment on a server with an existing configured Mutalyzer
installation:

    fab deploy -H server1.mutalyzer.nl

To do a fresh deployment on a new server:

    fab deploy:boostrap=yes -H server1.mutalyzer.nl


Get Mutalyzer
-------------

Since you are reading this, you can probably skip this step. Otherwise, get
your hands on a tarball and:

    tar -zxvf mutalyzer-XXX.tar.gz
    cd mutalyzer-XXX

Or get the source from GitLab directly:

    git clone https://git.lumc.nl/mutalyzer/mutalyzer
    cd mutalyzer


Install dependencies
--------------------

If you are on Debian or Ubuntu, you can use the following command to install
all dependencies:

    sudo bash extras/pre-install.sh

Otherwise, install them manually (perhaps have a look in the above script for
a useful dependency list).


Install Mutalyzer
-----------------

Mutalyzer can be installed using Python setuptools. For a production
environment:

    sudo python setup.py install

Alternatively, if you want to have a development environment, use:

    sudo python setup.py develop

The development environment uses symlinks to this source directory, so you can
develop directly from here. This command should be re-issued whenever the
version number of Mutalyzer is updated.


Setup Mutalyzer
---------------

This step creates configuration files and populates the database:

    sudo bash extras/post-install.sh

You can now edit /etc/mutalyzer/config and /etc/apache2/conf.d/mutalyzer.conf
to your likings.


Test the installation
---------------------

You should always test the installation. The tests (for now at least) need
the batch daemon and the webserver (the SOAP part) running.

Now run the tests:

    nosetests


Upgrade Mutalyzer
-----------------

Unless you installed Mutalyzer in a development environment as described
above, you can upgrade Mutalyzer to a new version by running from the source
directory:

    sudo python setup.py install
    sudo bash extras/post-upgrade.sh

If you installed Mutalyzer in a development environment, you don't have to
do anything usually, except for the following situations.

* If the database has changed, run:

    for M in extras/migrations/*.migration; do sudo $M migrate; done

* If the Mutalyzer version has changed, run:

    sudo python setup.py develop