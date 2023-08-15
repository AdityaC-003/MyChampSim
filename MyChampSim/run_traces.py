import os
from tqdm import tqdm

replacement_policies = ["adc", "mockingjay", "hawkeye", "lru"]
# replacement_policies = ["adc" + "_" + str(th) + "_" + str(td) for th in [6,8,9] for td in [12,16,20]]
tracefiles = os.listdir("./tracefiles/")
tracefiles = [tracefile.split(".")[0] for tracefile in tracefiles if tracefile.split(".")[1] == "trace"]

warmup_instructions_in_millions = 200
simulation_instructions_in_millions = 500


def build_executable(replacement_policy):
    '''
    Builds the executable for the given replacement policy.
    '''
    print(f"Building executable for {replacement_policy} replacement policy...")
    
    try:
        os.system(f"./build_champsim.sh bimodal no no {replacement_policy} 1 ni no no no no no")
    except Exception as e:
        print(f"Failed to build executable for {replacement_policy} replacement policy.")
        print("Exception: ", e)
        return False
    
    print(f"Successfully built executable for {replacement_policy} replacement policy.")
    return True


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
    for replacement_policy in replacement_policies:
        if not build_executable(replacement_policy):
            continue
        print(f'Testing {replacement_policy} replacement policy...')
        
        astar_tracefiles = [tracefile for tracefile in tracefiles if "astar" in tracefile]
        
        for i in tqdm(range(len(astar_tracefiles))):
            tracefile = astar_tracefiles[i]
            if "core" in tracefile:
                continue

            n = os.fork() # parent process continues loop, child process runs executable
            if n > 0:
                continue
            run_executable(replacement_policy, tracefile)    
            print(f"Successfully started executable for {replacement_policy} replacement policy and {tracefile} tracefile.")
            print("-" * 40)

        print(f'Finished testing {replacement_policy} replacement policy.')
        print( "-" * 40)
        print( "-" * 40)
        print( "-" * 40)


if __name__ == "__main__":
    main()
    