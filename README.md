RHODS-DevOps-Infra
====================

Auto-Merge Workflow
----------
* Execute each day at UTC 0:0 from the [github workflow](https://github.com/red-hat-data-services/rhods-devops-infra/blob/main/.github/workflows/auto-merge.yaml)
* syncs and merges changes from upstream repos to downstream repos based on the [auto-merge config yaml](https://github.com/red-hat-data-services/rhods-devops-infra/blob/main/src/config/source_map.yaml)
* automerge can be set to 'no' to disable auto-merge for any of the configured repos
* Can we manually executed when needed from github actions tab
* the workflow automatically creates required number of job to auto-merge each configured repo and runs all the jobs in parallel

Enable Auto-Merge for a repo
-----------------------------
1. update the [auto-merge config yaml](https://github.com/red-hat-data-services/rhods-devops-infra/blob/main/src/config/source_map.yaml) for required repo and raise a PR
    1. provide appropriate upstream and downstream URLs and branches
   2. set automerge to yes
2. Ensure that [DevOps bot](https://github.com/organizations/red-hat-data-services/settings/installations/36825452) has permission to the target downstream repo (this step needs admin access, here is the [list of members with admin access](https://github.com/orgs/red-hat-data-services/people?query=role%3Aowner))
3. Test it manually (optional):
    1. Go to [the workflow](https://github.com/red-hat-data-services/rhods-devops-infra/actions/workflows/auto-merge.yaml)
   2. Click on 'Run Workflow'
   3. Select branch as 'main'
   4. Select the repo name from dropdown
   5. Hit the 'Run Workflow' button


