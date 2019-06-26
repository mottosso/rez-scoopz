<img width=500 src=https://user-images.githubusercontent.com/2152766/59205156-2eecb500-8b9a-11e9-8ad9-2ef1e167b7b8.png>

Install anything from [Scoop](https://scoop.sh/) as a Rez package.

**See also**

- [rez-pipz](https://github.com/mottosso/rez-pipz)

<br>

### Features

- **Large selection** Install any of the [500+ available packages](https://github.com/ScoopInstaller/Main/tree/master/bucket) from Scoop, like `python` and `git`
- **Try before you buy** Like `apt-get` and `yum`, no packages are actually installed until you've witnessed and confirmed what Scoop comes up with, including complex dependencies.

<br>

### Installation

This repository is a Rez package, here's how you can install it.

```bash
$ git clone https://github.com/mottosso/rez-scoopz.git
$ cd rez-scoopz
$ rez build --install
```

<br>

### Usage

![scoopz](https://user-images.githubusercontent.com/2152766/59216542-bbf03800-8bb3-11e9-85a0-421df2b85f37.gif)

`scoopz` is used like any other Rez package, and comes with a handy `install` executable for convenient access.

```bash
$ rez env scoopz -- install python
$ rez env python -- python --version
Python 3.7.3
```

Which is the equivalent of calling..

```bash
$ rez env scoopz
> $ install python
```

And, for the advanced user, it may also be used as a Python package. Note that it requires Rez itself to be present as a package, along with a copy of Python that isn't coming from Rez.

> Try before I buy?

Prior to creating a package and polluting your package repository, packages are prepared and presented to you for confirmation.

```bash
rez env scoopz -- install curl
Initialising Scoop 2019.05.15.6... ok - 0.04s
Reading package lists... ok - 21.38s
Parsing Scoop apps... ok - 0.01s
Discovering existing packages... ok - 0.00s
The following NEW packages will be installed:
  7zip    19.00     platform-windows/arch-AMD64
  curl    7.64.1_1  platform-windows/arch-AMD64
Packages will be installed to C:\Users\manima\packages
After this operation, 12.36 mb will be used.
Do you want to continue? [Y/n]
```

> How does this work?

```bash
$ rez env python rez scoopz
> $ python -m scoopz --help
usage: __main__.py [-h] [--verbose] [--release] [--prefix PATH] [-y] [-q]
                   request

positional arguments:
  request        Packages to install, e.g. python curl

optional arguments:
  -h, --help     show this help message and exit
  --verbose      Include Scoop output amongst scoopz messages.
  --release      Write to REZ_RELEASE_PACKAGES_PATH
  --prefix PATH  Write to this exact path
  -y, --yes      Do not ask to install, just do it
  -q, --quiet    Do not print anything to the console
```

<br>

### FAQ

> Why rez-scoopz? Why not X?

This project came about as a requirement for a separate project, here are the developer "journal" from there.

- https://gist.github.com/mottosso/0945b2d19a1920e999fbfb61f4f301a3
- https://gist.github.com/mottosso/5492d55f20b1f38979c8577fc5f5cfbc

Beyond that, packaging external software with Rez is a pain. Some software is available through Scoop, such as `python` so that you won't have to worry about packaging it yourself.

- [Full list](https://github.com/ScoopInstaller/Main/tree/master/bucket)

> Why is initialisation of Scoop taking so long?

For each new package installed, a kind of virtual environment is created for Scoop. This environment is generated using directory symlinks where possible, and plain copies elsewhere. If you experience a delay in initialising Scoop (anywhere beyond 1 second), test whether you are able to perform a `mklink /D`. If not, you may want to consider enabling it to save between 5-20 seconds of time spent installing new packages.

- https://superuser.com/questions/104845/permission-to-make-symbolic-links-in-windows-7

Control this behavior using the these environment variables.

- `SCOOPZ_JUNCTION=1` Use Junction rather than directory symlinks. These are supported by non-privileged users, but does not work across disk partitions.
- `SCOOPZ_COPY=1` Do not use symlinks, perform a plain file-copy. This is the safest option, but also the slowest (roughly 10 additional seconds per invokation)

> How come Scoop's package repository is referenced by commit ID?

The current version of this package, and in effect Scoop, is `2019-05-15` (see `package.py`).

Because each Rez package is idempotent, an effort is made to disable Scoops native auto-update functionality, along with maintaining a fixed relationship between the version of Scoop and version of "bucket", which is what Scoop calls its package repository. Scoop is only ever compatible with a single version of a repository, as both packages and API changes frequently over time.

To update to a newer version, specify either a tag, such as `2019-05-15` or commit SHA for *both Scoop and bucket*. This is important, else Scoop may not work.

> How does this work?

Rez wraps Scoop, forwarding any call made and parsing its response. Whenever an "app" is installed from one of its "buckets", the app is later converted into a Rez package and installed like any other.

```
$ rez env scoopz -- install python
     |
     |                        .-------------------> ~/packages/python/3.7.3
     |                        |
.----o-------- scoopz --------o----.
|    |                        |    |
| .--v-------- Scoop ---------o--. |
| |                              | |
| |                              | |
| |                              | |
| |                              | |
| |______________________________| |
|                                  |
`----------------------------------`

```

<br>
