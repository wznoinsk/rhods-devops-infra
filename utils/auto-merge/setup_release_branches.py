import os
import re
import json
from datetime import datetime, timedelta
import smartsheet
import argparse

import yaml


class setup_release_branches:
    def __init__(self):
        pass

    def get_sprint_start_dates(self):
        column_map = {}
        smart = smartsheet.Smartsheet()
        # response = smart.Sheets.list_sheets()
        sheed_id = os.getenv('BUILD_SHEET_ID')
        sheet = smart.Sheets.get_sheet(sheed_id)
        for column in sheet.columns:
            column_map[column.title] = column.id
        # print(column_map)

        # process existing data
        sprintStartDates = {row.cells[1].value: datetime.strptime(row.cells[3].value, '%Y-%m-%dT%H:%M:%S').date() for row in sheet.rows if row.cells[1].value and ('sprint starts' in str(row.cells[1].value).lower() or 'sprintstarts' in str(row.cells[1].value).lower() or 'sprint-starts' in str(row.cells[1].value).lower()) }
        print('sprintStartDates', sprintStartDates)
        return sprintStartDates
    def get_release_to_be_setup(self):
        dates_to_search = [datetime.today().date()]
        release_to_be_setup = ''
        sprintStartDates = self.get_sprint_start_dates()
        for event, dt in sprintStartDates.items():
            if dt in dates_to_search:
                capture = re.search('2.([0-9]{1,2})[a-zA-Z\s]{1,20}', event)
                release_to_be_setup = f'rhoai-2.{capture.group(1)}'
                break
        print('release_to_be_setup', release_to_be_setup)
        print('dates_to_search', dates_to_search)
        return release_to_be_setup

    def update_release_map(self, release_to_be_setup):
        release_map = yaml.load(open('src/config/releases.yaml'))
        if release_to_be_setup:
            print(f'adding {release_to_be_setup} to the config')
            if release_to_be_setup not in release_map['releases']:
                release_map['releases'].append(release_to_be_setup)
            print('release_map', release_map)
        yaml.dump(release_map, open('src/config/releases.yaml', 'w'))



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--release', default='DEFAULT', required=False, help='Release to be setup', dest='release')
    args = parser.parse_args()
    srb = setup_release_branches()
    release_to_be_setup = args.release if args.release and args.release != 'DEFAULT' else srb.get_release_to_be_setup()
    with open('RELEASE_TO_BE_SETUP' ,'w') as RELEASE_TO_BE_SETUP:
        RELEASE_TO_BE_SETUP.write(release_to_be_setup)
    srb.update_release_map(release_to_be_setup)
