# coding: utf-8
# Copyright (c) 2019, Taku MURAKAMI. All rights reserved.
# Distributed under the terms of the BSD 3-clause License.

import logging
import sys
import os
import subprocess

"""
Automation script of VASP calculation.
"""

logger = logging.getLogger(__name__)

# calculation configurations
n_jobs = 16
backup_files = ["POSCAR", "CONTCAR", "OUTCAR", "OSZICAR"]
output_path = "./output/"


def read_struct_list(file_path):
    """
    Reads structure list from the file at file_path.
    
    Arguments
    ---------
    file_path: str
        Path to the file which includes the list of name of structures.
    
    Returns
    -------
    struct_list: list
        List of name of structures.
    """
    struct_list = []
    with open(file_path, mode="r") as file:
        for struct_name in file:
            struct_list.append(struct_name)
    return struct_list

def run_vasp():
    """
    Runs VASP for list of structure.
    """
    cmd = "mpirun -np " + str(n_jobs) + " vasp &"
    devnull = open("/dev/null", "w")
    subprocess.run(cmd.split(), stdout=devnull)

def mv_output_files():
    """
    Moves output files to output path.
    """
    for file in backup_files:
        if not os.path.exists(output_path+struct_name):
            os.makedirs(output_path+struct_name, exist_ok=True)
        cmd = "mv " + file + " " + output_path+struct_name
        subprocess.run(cmd.split())


if __name__ == "__main__":
    struct_list = read_struct_list(sys.argv[1])
    for struct_name in struct_list:
        cmd = "mv POSCAR_" + struct_name + " POSCAR"
        subprocess.run(cmd.split())
        run_vasp()
        mv_output_files(struct_name)
