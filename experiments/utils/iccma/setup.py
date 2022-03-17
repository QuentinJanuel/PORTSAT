import shutil
import os
from pathlib import Path
from utils.iccma.download import download


def setup():
    iccma15 = Path(__file__)\
        .parent\
        .joinpath("data")\
        .resolve()
    if iccma15.exists() and len(os.listdir(iccma15)) > 0:
        return
    zip = iccma15.joinpath("iccma15.zip")
    download(
        zip,
        "/".join([
            "http://argumentationcompetition.org",
            "2015",
            "iccma2015_benchmarks.zip"
        ]),
    )
    shutil.unpack_archive(zip, iccma15)
    if zip.exists():
        os.remove(zip)
