import os
import sys
from tqdm import tqdm

replacement_policies = ["mockingjay", "lru"]
# replacement_policies = ["adc" + "_" + str(th) + "_" + str(td) for th in [6,8,9] for td in [12,16,20]]
tracefiles = os.listdir("./tracefiles/")
tracefiles = [tracefile.split(".")[0] for tracefile in tracefiles if tracefile.split(".")[1] == "trace"]

warmup_instructions_in_millions = 200
simulation_instructions_in_millions = 800


def run_executable(replacement_policy, tracefile):
    '''
    Runs the executable for the given replacement policy and tracefile.
    '''
    print(f"Running executable for {replacement_policy} replacement policy and {tracefile} tracefile...")
    
    try:
        os.system(f"./run_champsim.sh bimodal-no-no-{replacement_policy}-1core-ni-no-no-no-no-no {warmup_instructions_in_millions} {simulation_instructions_in_millions} {tracefile}")
    except Exception as e:
        print(f"Failed to run executable for {replacement_policy} replacement policy and {tracefile} tracefile.")
        print("Exception: ", e)
        return False
    
    print(f"Successfully ran executable for {replacement_policy} replacement policy and {tracefile} tracefile.")
    return True


def main():
    '''
    Runs the executable for each replacement policy and each tracefile.
    '''
    tracekey = "astar_23B"
    if len(sys.argv) > 1:
        tracekey = sys.argv[1]

    print(f"TRACE = {tracekey}")
    for replacement_policy in replacement_policies:
        print(f'Testing {replacement_policy} replacement policy...')
        
        astar_tracefiles = [tracefile for tracefile in tracefiles if tracekey in tracefile]
        
        for i in tqdm(range(len(astar_tracefiles))):
            tracefile = astar_tracefiles[i]
            if "core" in tracefile:
                continue
            run_executable(replacement_policy, tracefile)    
            print(f"Successfully started executable for {replacement_policy} replacement policy and {tracefile} tracefile.")
            print("-" * 40)

        print(f'Finished testing {replacement_policy} replacement policy.')
        print( "*" * 40)


if __name__ == "__main__":
    main()
    