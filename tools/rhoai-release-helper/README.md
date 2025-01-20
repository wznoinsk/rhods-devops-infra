RHOAI-Release-Helper
====================

Objectives
----------
* To prepare all the required artifacts for stage and prod release
* To validate the consistency of all the artifacts
* To ensure the correct sequence of release process through automated flow

Pros
------
* To avoid manual efforts during the stage/prod release process
* To eliminate any possible errors with the manual work
* To avoid inconsistency with any artifacts


Setup & Prerequisites
------
* Make sure you have “yq” installed
* Create a file “~/.ssh/.quay_devops_application_token” with the contents as the secret value from of the quay application token
* Clone https://github.com/rhoai-rhtap/RHOAI-Konflux-Automation to your machine

Nightly Override Snapshot Generator
-----
* cd into `tools/rhoai-release-helper` 
* run `python -m venv venv` (or `python3 -m venv venv`)
* `source venv/bin/activate`
* `pip install -r requirements.txt`
* make sure you have the quay token set up according to the section above
* run `bash generate-nightly-override-snapshot.sh`
