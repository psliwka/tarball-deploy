tarball-deploy - atomically deploy your code from tarballs
==========================================================
[![Build status](https://travis-ci.org/psliwka/tarball-deploy.svg?branch=master)](https://travis-ci.org/psliwka/tarball-deploy)
[![PyPI page](https://img.shields.io/pypi/v/tarball-deploy.svg)](https://pypi.python.org/pypi/tarball-deploy/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

`tarball-deploy` is an utility to facilitate deploying code (or any files, for
that matter) packed into TAR archives. It handles unpacking received archives,
and switching to new releases atomically (using a little bit of symlink magic).

Use cases
---------

`tarball-deploy` has been written with shared web hosting services in mind,
which usually grant you SSH access to a shared server, and one or more
`public_html` directories, where you're expected to put your website files (eg.
static HTML, or PHP scripts). This tool attempts to address the following
problems:
* How to copy new release of your website from your CI/CD pipeline (you have
  one, right?) to your server.
* How to switch to the new release atomically, so that the site is in
  consistent state all the time.
* How to call securely additional hooks before and after deployment (f.ex.
  restarting your web server), in a way which does not allow your CI runner to
  execute arbitrary commands on the server.

Requirements
------------

* A decent UNIX-like system, which will let you install custom Python scripts
* A `tar` implementation. GNU Tar and libarchive (FreeBSD) tar are known to
  work.

Installation
------------

Remember that `tarball-deploy` is expected to be installed on your server. The
easiest way is to install it with `pip`:
```sh
$ pip install tarball-deploy
```

You might, however, want or need to install it in a virtualenv and symlink
somewhere in your `$PATH`.

Usage
-----

To use `tarball-deploy`, you need to pack your code into a TAR archive first.
This is out of scope of this project, but usually you can do something like:
```sh
$ tar cf release.tar index.html style.css images/**
```

Then you can proceed with your preferred deployment method from below.

### Deploy from local machine
```sh
$ ssh your-username@your-host tarball-deploy --workdir=/your/remote/deployment/dir < release.tar
```
Should things go wrong, you can quickly revert to the previous deployment:
```sh
$ ssh your-username@your-host tarball-deploy --workdir=/your/remote/deployment/dir --rollback
```

### Deploy from CI
For every website you want to manage, you will need to:
* Generate an SSH keypair for your CI runner
* Edit `.ssh/authorized_keys` on your server and add something similar to:
  ```
  restrict,command="tarball-deploy --workdir=/your/remote/deployment/dir" ssh-rsa AAAAB3Nza...
  ```
* Symlink `/your/remote/deployment/dir/current` to a place where your web
  server is expected to find your site content (usually something like
  `~/domains/example.com/public_html`)

### Calling additional hooks
Put your `pre-deploy` and `post-deploy` scripts inside
`/your/remote/deployment/dir/hooks`. They need to be marked as executable.

Credits
-------

Created by [Piotr Śliwka](https://github.com/psliwka)

License
-------

MIT
