import logging
import os, sys
import subprocess
from datetime import datetime

import rcdb
from rcdb.log_format import BraceMessage as Lf

###################################################
# Collection of helper functions for Hall A RCDB
###################################################

def get_epics_avg(run, epics_name, rmin, rmax):
    """
    Get average epics values from epics db
    Inputs: db.run, name of epics variable, range [min, max]
    """
    
    this_value = None

    # First, get timestamps
    start_time_str = datetime.strftime(run.start_time, "%Y-%m-%d %H:%M:%S")
    if run.end_time is not None:
        end_time_str = run.end_time
    else:
        # Use time now instead
        now_time = datetime.now()
        end_time_str = now_time.strftime("%Y-%m-%d %H:%M:%S")
        
    try:
        range_str = str(rmin) + ":" + str(rmax)
        cmds = ["myStats", "-b", start_time_str, "-e", end_time_str, "-c", epics_name, "-r", range_str, "-l", epics_name]
        cond_out = subprocess.Popen(cmds, stdout=subprocess.PIPE)
        n = 0
        for line in cond_out.stdout:
            n += 1
            if n == 1: # skip header
                continue
            tokens = line.strip().split()
            if len(tokens) < 3:
                continue
            key = tokens[0]
            value = tokens[2]
            if value = "N/A":
                value = 0
            if key == epics_name:
                this_value = value
    except Exception as ex:
        print("ERROR: ", str(ex))
                
    return this_value

