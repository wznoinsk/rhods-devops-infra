RHOAI-DevOps-Infra
====================

Downstream main to rhoai-x.y Auto-Merge Infra
----------
* The infra is responsbile for following tasks:
   * **On Sprint Start** - Automatically create rhoai-x.y branches for all the repos and enable the auto-merge
   * **Till code-freeze (RC day)** - daily sync from main to rhoai-x.y
   * **On code-freeze (RC day)** - disable the auto-merge from main to rhoai-x.y 
* Execute each day at UTC 1:0 from the [github workflow](https://github.com/red-hat-data-services/rhods-devops-infra/blob/main/.github/workflows/main-release-auto-merge.yaml)
* Daily syncs the changes from downstream main to rhoai-x.y branch based on the configuration [auto-merge config yaml](https://github.com/red-hat-data-services/rhods-devops-infra/blob/main/src/config/main-release-source-map.yaml)
* It is by default enabled for all the repos, but can be disabled using the same config file
* automerge can be set to 'no' to disable auto-merge for any of the configured repos
* The workflow automatically creates required number of job to auto-merge each configured repo and runs all the jobs in parallel

Enable Downstream main to rhoai-x.y Auto-Merge for a repo
-----------------------------
1. Update the [auto-merge config yaml](https://github.com/red-hat-data-services/rhods-devops-infra/blob/main/src/config/main-release-source-map.yaml) for required repo and raise a PR
   1. provide appropriate upstream and downstream URLs and branches
   2. set automerge to yes
2. Ensure that [DevOps bot](https://github.com/organizations/red-hat-data-services/settings/installations/36825452) has permission to the target downstream repo (this step needs admin access, here is the [list of members with admin access](https://github.com/orgs/red-hat-data-services/people?query=role%3Aowner))
3. Test it manually (optional):
   1. Go to [the workflow](https://github.com/red-hat-data-services/rhods-devops-infra/actions/workflows/main-release-auto-merge.yaml)
   2. Click on 'Run Workflow'
   3. Select branch as 'main'
   4. Select the repo name from dropdown
   5. Hit the 'Run Workflow' button

Upstream to Downstream Auto-Merge Infra
----------
* Execute each day at UTC 0:0 from the [github workflow](https://github.com/red-hat-data-services/rhods-devops-infra/blob/main/.github/workflows/upstream-auto-merge.yaml)
* syncs and merges changes from upstream repos to downstream repos based on the [auto-merge config yaml](https://github.com/red-hat-data-services/rhods-devops-infra/blob/main/src/config/upstream-source-map.yaml)
* automerge can be set to 'no' to disable auto-merge for any of the configured repos
* Can be manually executed when needed from github actions tab
* The workflow automatically creates required number of job to auto-merge each configured repo and runs all the jobs in parallel


Enable Upstream to Downstream Auto-Merge for a repo
-----------------------------
1. Update the [auto-merge config yaml](https://github.com/red-hat-data-services/rhods-devops-infra/blob/main/src/config/upstream-source-map.yaml) for required repo and raise a PR
   1. provide appropriate upstream and downstream URLs and branches
   2. set automerge to yes
2. Ensure that [DevOps bot](https://github.com/organizations/red-hat-data-services/settings/installations/36825452) has permission to the target downstream repo (this step needs admin access, here is the [list of members with admin access](https://github.com/orgs/red-hat-data-services/people?query=role%3Aowner))
3. Test it manually (optional):
   1. Go to [the workflow](https://github.com/red-hat-data-services/rhods-devops-infra/actions/workflows/upstream-auto-merge.yaml)
   2. Click on 'Run Workflow'
   3. Select branch as 'main'
   4. Select the repo name from dropdown
   5. Hit the 'Run Workflow' button


