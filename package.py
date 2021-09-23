name = "scoopz"
version = "2020.11.26.0"
requires = ["python-2.7+,<4", "bleeding_rez-2.29+"]

# Each version of Scoop of heavily coupled with whatever its
# repository of available packages look like at the time. It
# is an informal relationship, enforced by Scoop's automatic
# update mechanism.
_buckets = {
    "main": (
        "https://github.com/ScoopInstaller/Main/archive/"
        "716e231704fd96a8a8b8a80e3d13934ebda4c687.zip"
    ),
    "versions": (
        "https://github.com/ScoopInstaller/Versions/archive/"
        "31444d45647831655ff8b5ec7a89854d8f8c3786.zip"
    )
}

build_command = "python {root}/install.py %s" % version
build_command += " --overwrite"
build_command += " --bucket %s" % _buckets["main"]
build_command += " --bucket %s" % _buckets["versions"]

variants = [
    ["platform-windows", "arch-AMD64"]
]


def commands():
    global env
    global alias

    env.PATH.prepend("{root}/home/apps/scoop/current/bin")  # Expose scoop.ps1
    env.PYTHONPATH.prepend("{root}/python")

    alias("install", "python -u -m scoopz")

    env.SCOOP = "{root}/home"
    env.SCOOP_HOME = "{root}/home"
