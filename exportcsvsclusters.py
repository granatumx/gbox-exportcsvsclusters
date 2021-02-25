#!/usr/bin/env python

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from zipfile import ZipFile
from granatum_sdk import Granatum

import os
import traceback
import sys
from os import environ, path

from gbox_py_helpers import bug_report

def main():
    gn = Granatum()

    groups = gn.get_import("groups")
    df = gn.pandas_from_assay(gn.get_import("assay"))

    inv_map = {}
    for k, v in groups.items():
        inv_map[v] = inv_map.get(v, []) + [k]

    zipObj = ZipFile(path.join(gn.exports_dir, 'exportcsvs.zip'), 'w')

    for k, v in inv_map.items():
        fname = "{}.csv".format(k)
        cfile = path.join(gn.exports_dir, fname)
        with open(cfile, "w") as f:
            f.write(df.loc[:, v].to_csv())
        zipObj.write(cfile, fname)

    zipObj.close()
    self.dynamic_exports.append({"extractFrom": "exportcsvs.zip", "kind": None, "meta": None})

    for k, v in inv_map.items():
        fname = "{}.csv".format(k)
        cfile = path.join(gn.exports_dir, fname)
        os.remove(cfile)

    gn.commit()

if __name__ == "__main__":
    # Try except block to send an email about error #
    try:
        main()
    except:
        error_message = traceback.format_exc()
        sys.stderr.write(error_message) # Write the error to stderr anyway so the user can see what went wrong
        bug_report("Export CSVs", "lana.garmire.group@gmail.com", error_message)
