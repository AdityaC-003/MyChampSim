import os

replacement_policies = ["adc", "mockingjay", "hawkeye", "lru"]
# replacement_policies = ["adc" + "_" + str(th) + "_" + str(td) for th in [6,8,9] for td in [12,16,20]]

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


def main():
    '''
    Builds executable files for each replacement policy.
    '''
    for replacement_policy in replacement_policies:
        if not build_executable(replacement_policy):
            continue


if __name__ == "__main__":
    main()
    