RHOAI-Snapshot-Generator
====================

Purpose
----------
* To produce consistent snapshots based on builds marked as "nightly"

Setup & Prerequisites
------
* Create a file “~/.ssh/.quay_devops_application_token” with the contents as the secret value from of the quay application token
* cd into `tools/rhoai-release-helper` 
* run `python -m venv venv` (or `python3 -m venv venv`)
* `source venv/bin/activate`
* `pip install -r requirements.txt`
* run `bash generate-nightly-override-snapshot.sh`
