RHODS-DevOps-Infra
====================

Auto-Merge Workflow
----------
* Execute each day at UTC 0:0 from the [github workflow](https://github.com/red-hat-data-services/rhods-devops-infra/blob/auto-merge/.github/workflows/auto-merge.yaml)
* syncs and merges changes from upstream repos to downstream repos based on the [auto-merge config yaml](https://github.com/red-hat-data-services/rhods-devops-infra/blob/auto-merge/src/config/source_map.yaml)
* automerge can be set to 'no' to disable auto-merge for any of the configured repos
* Can we manually executed when needed from github actions tab
* the workflow automatically creates required number of job to auto-merge each configured repo and runs all the jobs in parallel


