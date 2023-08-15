'''
    read every file in ./results_10M/
    in each file, look for the line starting with LLC TOTAL, and extract that line
'''

import os
import matplotlib.pyplot as plt
import numpy as np

def get_llc_stats(filename):
    with open(filename, "r") as f:
        ipc = 1e9
        lines = f.readlines()
        for line in lines:
            if line.startswith("Finished CPU"):
                # ipc is the first string that follows "IPC:"
                ipc = get_ipc(line)
            if line.startswith("LLC TOTAL"):
                return llc_stats_to_dict(line, ipc)
    return None


def llc_stats_to_dict(line, ipc):
    '''
    line is of the form LLC TOTAL     ACCESS:      50134  HIT:      24728  MISS:      25406
    '''
    data = line.split(" ")
    data = [d for d in data if d != ""]
    return {
        "access": float(data[3]),
        "hit": float(data[5]),
        "miss": float(data[7]),
        "miss_rate": float(data[7]) / float(data[3]),
        "ipc": ipc
    }


def get_replacement_policy(filename):
    '''
    filename is of the form tracefile-bimodal-no-no-{replacement_policy}-1core-ni-no-no-no-no-no
    '''
    return filename.split("-")[4]


def get_tracefile(filename):
    '''
    filename is of the form tracefile-bimodal-no-no-{replacement_policy}-1core-ni-no-no-no-no-no
    '''
    return filename.split("-")[0]


def get_ipc(line):
    '''
    ipc is the string that follows "IPC:"
    '''
    data = line.split(" ")
    data = [d for d in data if d != ""]
    ipc_pos = data.index("IPC:") + 1
    return float(data[ipc_pos])


def main():
    for filename in sorted(os.listdir("./results_10M/")):
        tracefile = get_tracefile(filename)
        replacement_policy = get_replacement_policy(filename)
        stats_dict = get_llc_stats(f"./results_10M/{filename}")
        print(f"{tracefile}\t{replacement_policy}\t{stats_dict['miss_rate']}")
        print(f"{tracefile}\t{replacement_policy}\t{stats_dict['ipc']}")
 

def stats_summary():
    avg_miss_rate = {}
    weighted_avg_miss_rate = {}
    replacement_policy_trace_count = {}
    replacement_policy_weighted_trace_count = {}

    for filename in sorted(os.listdir("./results_10M/")):

        tracefile = get_tracefile(filename)
        replacement_policy = get_replacement_policy(filename)
        stats_dict = get_llc_stats(f"./results_10M/{filename}")

        if replacement_policy not in avg_miss_rate:
            avg_miss_rate[replacement_policy] = 0
        avg_miss_rate[replacement_policy] += stats_dict['miss_rate']

        if replacement_policy not in replacement_policy_trace_count:
            replacement_policy_trace_count[replacement_policy] = 0
        replacement_policy_trace_count[replacement_policy] += 1
    
        if replacement_policy not in weighted_avg_miss_rate:
            weighted_avg_miss_rate[replacement_policy] = 0
        weighted_avg_miss_rate[replacement_policy] += stats_dict['miss']
        replacement_policy_weighted_trace_count[replacement_policy] = stats_dict['access']
    
    for replacement_policy in avg_miss_rate:
        avg_miss_rate[replacement_policy] /= replacement_policy_trace_count[replacement_policy]
        print(f"{replacement_policy}\t{avg_miss_rate[replacement_policy]}")
        print(f"{replacement_policy}\t{weighted_avg_miss_rate[replacement_policy] / replacement_policy_weighted_trace_count[replacement_policy]}")

if __name__ == "__main__":
    main()
    # stats_summary()
