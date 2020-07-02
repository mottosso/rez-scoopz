import os
import errno
import shutil
import tempfile

from rez.package_maker__ import PackageMaker

from . import lib


def init():
    """Virtualise the Scoop home directory

    Due to symlinks, this is fast, less than 200 ms
    despite the resulting directory being ~30 mb.

    """

    package_root = os.path.join(os.path.dirname(__file__), "..", "..")
    package_root = os.path.abspath(package_root)
    package_root = os.path.normpath(package_root)
    package_home = os.path.join(package_root, "home")

    scoop_home = tempfile.mkdtemp()

    for subdir in ("apps", "shims", "cache"):
        os.makedirs(os.path.join(scoop_home, subdir))

    lib.junction(
        os.path.join(package_home, "apps", "scoop"),
        os.path.join(scoop_home, "apps", "scoop"),
    )

    lib.junction(
        os.path.join(package_home, "buckets"),
        os.path.join(scoop_home, "buckets"),
    )

    for shim in os.listdir(os.path.join(package_home, "shims")):
        src = os.path.join(package_home, "shims", shim)
        dst = os.path.join(scoop_home, "shims", shim)
        shutil.copyfile(src, dst)

    return scoop_home


def install(home, request, verbose=False):
    # TODO: This does not convert a Rez-like request to Scoop
    # E.g. python>=3.6 --> python-3.6.9

    lib.call([
        "powershell", "-ExecutionPolicy", "Bypass",
        "scoop", "install"
    ] + request,
        env=dict(os.environ, **{
            "SCOOP": home,
            "SCOOP_HOME": home,
        }),
        verbose=verbose
    )


def parse(home):
    apps = os.path.join(home, "apps")
    installed = list()

    for app in os.listdir(apps):
        if app.lower() == "scoop":
            continue

        dist = lib.Distribution(home, app)
        installed += [dist]

    return installed


def deploy(distribution, target):
    """Convert `distribution` into Rez package at `target`"""

    name = distribution.name

    maker = PackageMaker(name)
    maker.version = distribution.version
    maker.requires = distribution.requirements
    maker.url = distribution.url
    maker.description = distribution.description
    maker.variants = distribution.variants

    commands = set()
    for relpath, alias, args in distribution.binaries():

        # Temporarily expose app dir to PATH
        # TODO: Implement Scoop's "shims" for this purpose
        # Reason they aren't implemented at the moment is
        # because shims carry an absolute path to their
        # executable, which we can't put into a package as
        # packages may come from differently mounted paths
        # or network locations at any given time.
        dirname = os.path.dirname(relpath).replace("\\", "/")
        commands.add("env.PATH.prepend(r'{root}/app/%s')" % dirname)

    # Handle PATH environment variables
    # NOTE: This presumes all environment variables are paths,
    # and that they branch out from the app/ directory. There may(?)
    # be variables that aren't paths too
    for key, value in distribution.envs():
        commands.add("env.%s.prepend('{root}/app/%s')" % (key, value))

    # Handle the odd case of no commands being present
    # This is probably a bad package then
    if not commands:
        print("WARNING: No commands made by this package, "
              "inspect it to see if it's allright")
        commands.add("pass")

    maker.commands = "\n".join(commands)

    package = maker.get_package()
    variant = next(package.iter_variants())
    root = variant.install(target).root

    appdir = os.path.join(root, "app")
    bindir = os.path.join(root, "bin")

    try:
        os.makedirs(root)
        os.makedirs(bindir)
    except OSError as e:
        if e.errno == errno.EEXIST:
            # That's ok
            pass
        else:
            raise

    shutil.copytree(distribution.root, appdir)

    # NOTE: Currently unused, see note above
    for relpath, alias, args in distribution.binaries():
        fname = os.path.basename(relpath)
        name, ext = os.path.splitext(fname)
        args = " ".join(args)

        bat = os.path.join(bindir, (alias or name) + ".bat")
        with open(bat, "w") as f:
            f.write("\n".join([
                "@echo off",
                "call %~dp0../app/{relpath} {args} %*".format(**locals())
            ]))
