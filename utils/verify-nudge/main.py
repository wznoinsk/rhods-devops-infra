from termcolor import colored
import util
import validator


def main():
    
    # Use RHOAI release versions from command-line arguments, or fetch from URL if not provided.
    rhoai_releases = util.get_rhoai_releases()
    print(colored(f"\n[For Debug] Releases: {rhoai_releases}\n", "cyan"))
    
    mismatch_found = False
    for release in rhoai_releases['releases']:
        configs = util.parse_yaml(file_path="config.yaml")
        for config in configs:
            
            print(colored("=======================================================", "white"))
            print(colored(text="Nudge Verification In Progress", color="white", attrs=['bold']))
            print(colored(text=f"-> Repo: '{config.get('name')}", color="white"))
            print(colored(text=f"-> Branch: '{release}'", color="white"))
            print(colored("=======================================================", "white"))
            #print(colored(text=f"\n[For Debug] Config: '{config}' \n", color="white"))
    
            if validator.validate_config_yaml(config):
                
                # Skip, if the component was not onboarded in the current release
                if not util.is_component_onboarded(release, config.get('onboarded-since', '')):
                        print(colored(f"'[{config.get('name')}]' nudge started in release '{release}'. Skipping nudge verification! ", "yellow"))
                        print()
                        continue
                else:
                    mismatch_found = util.verify_nudge(release, config)

    if mismatch_found:
        exit(1)



if __name__ == '__main__':
    main()
