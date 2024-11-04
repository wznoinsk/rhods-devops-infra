import os
from datetime import datetime
import smartsheet
import re
from jira import JIRA

class MetricsTool:
    def __init__(self):
        access_token = os.getenv('SMARTSHEET_ACCESS_TOKEN')
        self.smart = smartsheet.Smartsheet(access_token)
        self.sheet_id = os.getenv('BUILD_SHEET_ID')
    
    def get_dates(self, keyword):
        sheet = self.smart.Sheets.get_sheet(self.sheet_id)
        return {
            row.cells[1].value: datetime.strptime(row.cells[3].value, '%Y-%m-%dT%H:%M:%S').date()
            for row in sheet.rows
            if row.cells[1].value and keyword in str(row.cells[1].value).lower() and row.cells[3].value
        } #row cells 1 is the release name and row cells 3 is the date

    def get_dates_by_version(self):
        releases = {}
        for keyword, title in [('sprint starts', 'Sprint Starts'), ('code freeze','Code Freeze'), ('rc available for testing', 'RC available for Testing'), ('ga target', 'GA Target')]: #search for sprint starts and code freeze
            for release, date in self.get_dates(keyword).items(): #get the dates for each keyword
                version = self.extract_version(release) #get the version number from the release name
                if version:
                    releases.setdefault(version, {})[title] = date #add the date to the dictionary
        return releases

    def extract_version(self, release_name): 
        match = re.match(r'(\d+\.\d+)\s', release_name) #look for a version number in the format "X.Y" at the start of the release_name string using regex.
        return match.group(1) if match else None

    def get_closest_future_code_freeze_version(self):
        today = datetime.now().date() 
        current_version, closest_date = None, None

        for version, dates in self.get_dates_by_version().items(): #iterate through the versions and dates
            code_freeze_date = dates.get('Code Freeze')
            if code_freeze_date and code_freeze_date >= today: #if the code freeze date is in the future
                if closest_date is None or code_freeze_date < closest_date: #if this is the first future code freeze date or if this code freeze date is closer than the previous closest code freeze date
                    closest_date, current_version = code_freeze_date, version #set the closest date and version to the current code freeze date and version

        return current_version
    
    def print_release_dates(self, version=None):
        releases = self.get_dates_by_version()
        if version: 
            releases = {key: value for key, value in releases.items() if version in key} #filter the releases to only include the specified version

        sprint_start_date, rc_date, ga_date = None, None, None
        for version, dates in releases.items(): #iterate through the releases
            for title, date in dates.items(): #iterate through the dates
                #assign start and end dates based on the title
                if title == "Sprint Starts":
                    sprint_start_date = date
                elif title == "RC available for Testing":
                    rc_date = date
                elif title == "GA Target":
                    ga_date = date
            
        return sprint_start_date, rc_date, ga_date

def main():
    metrics = MetricsTool()
    
    token = os.getenv('JIRA_TOKEN')
    current_version = metrics.get_closest_future_code_freeze_version()
    print("\nCurrent Version:", current_version)
    sprint_start_date, rc_date, ga_date = metrics.print_release_dates(version=current_version)
    print(f"{current_version} Sprint Starts: {sprint_start_date} and {current_version} RC available for Testing: {rc_date} and {current_version} GA Target: {ga_date}")

    # Set found_in_nightly label
    jira = JIRA('https://issues.redhat.com', token_auth=token)
    fixVersion = f"RHOAI_{current_version}.0"
    jql_query = (
        f'Project=RHOAIENG AND affectedVersion={fixVersion} AND '
        f'(type in (Bug)) AND '
        f'(component not in (Documentation, PXE)) AND '
        f'created >= "{sprint_start_date}" AND created < "{rc_date}" AND '
        f'(labels NOT IN ("found_in_nightly", "found_in_rc", "RHOAI-releases", "RHOAI-internal", "pre-GA", "pre-RC") OR labels IS EMPTY) AND '
        f'(summary !~ "Snyk" AND summary !~ "CVE-*")'
    )

    print(f"\nSearching for Jiras with the filter: {jql_query}")
    issues_in_release = jira.search_issues(jql_query)
    for issue in issues_in_release:
        print(f"Adding 'found_in_nightly' label to {issue.key}")
        labels = issue.fields.labels
        labels.append("found_in_nightly")
        issue.update(fields={"labels": labels})

    # Set found_in_rc label
    jira = JIRA('https://issues.redhat.com', token_auth=token)
    fixVersion = f"RHOAI_{current_version}.0"
    jql_query = (
        f'Project=RHOAIENG AND affectedVersion={fixVersion} AND '
        f'(type in (Bug)) AND '
        f'(component not in (Documentation, PXE)) AND '
        f'created >= "{rc_date}" AND created < "{ga_date}" AND '
        f'(labels NOT IN ("found_in_rc", "found_in_nightly", "RHOAI-releases", "RHOAI-internal", "pre-GA", "pre-RC") OR labels IS EMPTY) AND '
        f'(summary !~ "Snyk" AND summary !~ "CVE-*")'
    )

    print(f"\nSearching for Jiras with the filter: {jql_query}")
    issues_in_release = jira.search_issues(jql_query)
    for issue in issues_in_release:
        print(f"Adding 'found_in_rc' label to {issue.key}")
        labels = issue.fields.labels
        labels.append("found_in_rc")
        issue.update(fields={"labels": labels})

if __name__ == "__main__":
    main()
