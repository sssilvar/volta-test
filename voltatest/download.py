import wfdb

from . import ROOT_DIR

# Download directory
dl_dir = ROOT_DIR / 'data' / 'mitdb'


def main():
    wfdb.dl_database('mitdb', dl_dir)
