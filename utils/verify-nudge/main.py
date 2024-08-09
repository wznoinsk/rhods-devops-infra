
import util
import validator


def main():
    
    # Use RHOAI release versions from command-line arguments, or fetch from URL if not provided.
    rhoai_releases = util.get_rhoai_releases()
    util.colored_print(text=f"\n[For Debug] Releases: {rhoai_releases}\n", color="magenta")
    mismatch_found = False
    for release in rhoai_releases['releases']:
        configs = util.parse_yaml(file_path="config.yaml")
        for config in configs:
            
            util.colored_print("===================================================================================", "white")
            util.colored_print(text="Nudge Verification In Progress", color="white", isBold=True)
            util.colored_print(text=f"-> Repo      : {config.get('name')}", color="white")
            util.colored_print(text=f"-> Branch    : {release}", color="white")
            util.colored_print(text=f"-> Verify    : {config.get('verify-components', 'all')}", color="white")
            util.colored_print(text=f"-> File Path : {config.get('nudged-file-path')}", color="white")
            util.colored_print(text=f"-> Repo URL  : {config.get('repo-url')}", color="white")
            util.colored_print("===================================================================================", "white")
            #util.colored_print(text=f"\n[For Debug] Config: '{config}' \n", color="white"))
    
            if validator.validate_config_yaml(config):
                
                # Skip, if the component was not onboarded in the current release
                if not util.is_component_onboarded(release, config.get('onboarded-since', '')):
                        util.colored_print(f"'[{config.get('name')}]' nudge started in release '{release}'. Skipping nudge verification! ", "yellow")
                        print()
                        continue
                
                if util.verify_nudge(release, config):
                    mismatch_found = True

    if mismatch_found:
        util.colored_print("Mismatch Found. Sending Slack Notification! ", "red")
        exit(1)



if __name__ == '__main__':
    main()
