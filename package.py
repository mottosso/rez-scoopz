name = "scoopz"
version = "2019.10.23.3"
requires = ["python-2.7+,<4", "bleeding_rez-2.29+"]

# Each version of Scoop of heavily coupled with whatever its
# repository of available packages look like at the time. It
# is an informal relationship, enforced by Scoop's automatic
# update mechanism.
_buckets = {
    "main": (
        "https://github.com/ScoopInstaller/Main/archive/"
        "cdd254db8f13e4d24dad4999296404bfae168bcf.zip"
    ),
    "versions": (
        "https://github.com/ScoopInstaller/Versions/archive/"
        "a3cf544c40082857f160cb7df55ae99093381dcd.zip"
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
