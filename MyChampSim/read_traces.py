'''
    read every file in results_filepath
    in each file, look for the line starting with LLC TOTAL, and extract that line
'''

import os
import matplotlib.pyplot as plt
import numpy as np

results_filepath = "./results_500M/" 
baseline_policy = "lru"

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


def get_ratio(filename):
    dbp, mock = 0, 0
    with open(filename, "r") as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("DBP Decisions:"):
                dbp = float(line.split(" ")[-1])
            elif line.startswith("Mockingjay Decisions:"):
                mock = float(line.split(" ")[-1])
    return dbp / (mock+1)


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


def add_key(dict, tracefile, replacement_policy, value):
    if tracefile not in dict.keys():
        dict[tracefile] = {}
    if replacement_policy == 'adc':
        replacement_policy = 'new_policy'
    dict[tracefile][replacement_policy] = value
    return dict

def main():

    ipc_dict = {}
    mpki_dict = {}
    ratio_dict = {}

    policies = ['lru', 'dbp_mm']
    tracefiles = ['astar_313B', 'bzip2_281B', 'bwaves_1609B', 'cactusADM_1495B', 'h264ref_178B', 'lbm_126B', 'leslie3d_1186B', 'libquantum_964B', 'soplex_271B', 'xalancbmk_99B']

    folder = sorted(os.listdir(results_filepath))

    for filename in folder:

        tracefile = get_tracefile(filename)
        replacement_policy = get_replacement_policy(filename)
    
        if(tracefile not in tracefiles or replacement_policy not in policies):
            continue

        print(f"{tracefile}\t{replacement_policy}")

        stats_dict = get_llc_stats(f"{results_filepath}{filename}")
        ipc_dict = add_key(ipc_dict, tracefile, replacement_policy, stats_dict['ipc'])
        mpki_dict = add_key(mpki_dict, tracefile, replacement_policy, stats_dict['miss'] / stats_dict['access'] * 1000)
        if replacement_policy == 'adc':
            ratio_dict[tracefile] = get_ratio(f"{results_filepath}{filename}")

    for tracefile in ipc_dict.keys():
        print(f"{tracefile}")
        # print(f"{ratio_dict[tracefile]}")
        for replacement_policy in sorted(ipc_dict[tracefile].keys()):
            ipc_wrt_lru = ipc_dict[tracefile][replacement_policy] / ipc_dict[tracefile][baseline_policy]
            ipc_wrt_lru = (ipc_wrt_lru - 1) * 100
            if replacement_policy != baseline_policy:
                print(f"{replacement_policy}\t{ipc_dict[tracefile][replacement_policy]}\t{ipc_wrt_lru}")
                # print(f"{replacement_policy}\t{ipc_wrt_lru}")
        print()
        
    # for tracefile in mpki_dict.keys():
    #     print(f"{tracefile}")
    #     print(f"{ratio_dict[tracefile]}")
    #     for replacement_policy in sorted(mpki_dict[tracefile].keys()):
    #         mpki_wrt_lru = mpki_dict[tracefile][replacement_policy] / mpki_dict[tracefile][baseline_policy]
    #         if replacement_policy != baseline_policy:
    #             # print(f"{replacement_policy}\t{mpki_dict[tracefile][replacement_policy]}\t{mpki_wrt_lru}")
    #             print(f"{replacement_policy}\t{mpki_wrt_lru}")
        print()

 

def stats_summary():
    avg_miss_rate = {}
    weighted_avg_miss_rate = {}
    replacement_policy_trace_count = {}
    replacement_policy_weighted_trace_count = {}

    folder = sorted(os.listdir(results_filepath))
    folder = [f for f in folder if "dbp_mock" in f]

    for filename in folder:

        tracefile = get_tracefile(filename)
        replacement_policy = get_replacement_policy(filename)
        
        stats_dict = get_llc_stats(f"{results_filepath}{filename}")

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
        # print(f"{replacement_policy}\t{avg_miss_rate[replacement_policy]}")
        print(f"{replacement_policy}\t{weighted_avg_miss_rate[replacement_policy] / replacement_policy_weighted_trace_count[replacement_policy]}")

if __name__ == "__main__":
    main()
    # stats_summary()
