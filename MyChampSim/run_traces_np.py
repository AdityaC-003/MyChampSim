import os
import sys
from tqdm import tqdm

replacement_policies = ["dbp_mock_lru_final"]
# replacement_policies = ["adc" + "_" + str(th) + "_" + str(td) for th in [6,8,9] for td in [12,16,20]]
tracefiles = os.listdir("./tracefiles/")
tracefiles = [
    tracefile.split(".")[0]
    for tracefile in tracefiles
    if tracefile.split(".")[1] == "trace"
]

warmup_instructions_in_millions = 200
simulation_instructions_in_millions = 500


def run_executable(replacement_policy, tracefile):
    """
    Runs the executable for the given replacement policy and tracefile.
    """
    print(
        f"Running executable for {replacement_policy} replacement policy and {tracefile} tracefile..."
    )

    try:
        os.system(
            f"./run_champsim.sh bimodal-no-no-{replacement_policy}-1core-ni-no-no-no-no-no {warmup_instructions_in_millions} {simulation_instructions_in_millions} {tracefile}"
        )
    except Exception as e:
        print(
            f"Failed to run executable for {replacement_policy} replacement policy and {tracefile} tracefile."
        )
        print("Exception: ", e)
        return False

    print(
        f"Successfully ran executable for {replacement_policy} replacement policy and {tracefile} tracefile."
    )
    return True


def main():
    """
    Runs the executable for each replacement policy and each tracefile.
    """
    tracekey = "astar_23B"
    if len(sys.argv) > 1:
        tracekey = sys.argv[1]

    print(f"TRACE = {tracekey}")
    for replacement_policy in replacement_policies:
        print(f"Testing {replacement_policy} replacement policy...")

        key_list = ['astar_313B', 'bzip2_281B', 'bwaves_1609B', 'cactusADM_1495B', 'h264ref_178B', 'lbm_126B', 'leslie3d_1186B', 'libquantum_964B', 'wrf', 'soplex_271B', 'xalancbmk_99B']

        astar_tracefiles = [tracefile for tracefile in tracefiles if any(key in tracefile for key in key_list)]

        for i in tqdm(range(len(astar_tracefiles))):
            tracefile = astar_tracefiles[i]
            if "core" in tracefile:
                continue
            run_executable(replacement_policy, tracefile)
            print(
                f"Successfully started executable for {replacement_policy} replacement policy and {tracefile} tracefile."
            )
            print("-" * 40)

        print(f"Finished testing {replacement_policy} replacement policy.")
        print("*" * 40)


if __name__ == "__main__":
    main()
