import argparse

from tarball_deploy import __version__
from tarball_deploy.workdir import WorkdirType


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.add_argument("--workdir", required=True, type=WorkdirType())
    action = parser.add_mutually_exclusive_group()
    action.add_argument(
        "--from", dest="tar_file", type=argparse.FileType(), default="-"
    )
    action.add_argument("--rollback", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()
    if args.rollback:
        args.workdir.rollback()
    else:
        args.workdir.deploy(args.tar_file)
