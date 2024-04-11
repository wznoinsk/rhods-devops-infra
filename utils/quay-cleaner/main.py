
from quay_controller import quay_controller
import json, traceback
def main():
    orgs = ['opendatahub', 'modh']
    repos_to_be_deleted = []
    repos_plain_list = ""


    for org in orgs:
        qc = quay_controller(org)
        repos = qc.get_all_repos()
        try:
            for repo in repos:
                repo_obj = {}
                repo_obj['repo'] = f'{org}/{repo}'
                tags = qc.get_all_tags_between_given_dates(repo)
                repo_obj['tags'] = []
                for tag in tags:
                    qc.delete_tag(repo, tag)
                    repo_obj['tags'].append(tag)
                    repos_plain_list += f'quay.io/{org}/{repo}@{tag["digest"]}\n'
                if repo_obj['tags']:
                    repos_to_be_deleted.append(repo_obj)
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            print(f'Exception while processing {repo} for tag {tag}')


    open('images_to_be_deleted.json', 'w').write(json.dumps(repos_to_be_deleted, indent=4))
    open('images_plain_list.txt', 'a').write(repos_plain_list)



if __name__ == '__main__':
    main()

