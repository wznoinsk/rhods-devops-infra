import re
import json
import pyyaml
from datetime import datetime, timedelta
import smartsheet
import argparse

import yaml


class stop_auto_merge:
    def __init__(self):
        pass

    def get_code_freeze_dates(self):
        column_map = {}
        smart = smartsheet.Smartsheet()
        # response = smart.Sheets.list_sheets()
        sheed_id = 3025228340193156
        sheet = smart.Sheets.get_sheet(sheed_id)
        for column in sheet.columns:
            column_map[column.title] = column.id
        # print(column_map)

        # process existing data
        codeFreezeDates = {row.cells[1].value: datetime.strptime(row.cells[3].value, '%Y-%m-%dT%H:%M:%S').date() for row in sheet.rows if 'code freeze' in row.cells[1].value.lower() or 'codefreeze' in row.cells[1].value.lower() or 'code-freeze' in row.cells[1].value.lower() }
        print('codeFreezeDates', codeFreezeDates)
        return codeFreezeDates
    def get_release_to_be_removed(self):
        dates_to_search = []
        release_to_be_removed = ''
        # if datetime.today().date().weekday() != 4:
        if datetime.today().date().weekday() != 3:
            dates_to_search.append(datetime.today().date())
        # if datetime.today().date().weekday() == 0:
        if datetime.today().date().weekday() == 4:
            dates_to_search.append(datetime.today().date() - timedelta(days=3))
        codeFreezeDates = self.get_code_freeze_dates()
        for event, dt in codeFreezeDates.items():
            if dt in dates_to_search:
                capture = re.search('2.([0-9]{1,2})[a-zA-Z\s]{1,20}', event)
                release_to_be_removed = f'rhoai-2.{capture.group(1)}'
                break
        print('release_to_be_removed', release_to_be_removed)
        print('dates_to_search', dates_to_search)
        return release_to_be_removed

    def update_release_map(self, release_to_be_removed):
        release_map = yaml.load(open('src/config/releases.yaml'))
        if release_to_be_removed:
            print(f'removing {release_to_be_removed} from the config')
            release_map['releases'].remove(release_to_be_removed)
            print('release_map', release_map)
        yaml.dump(release_map, open('src/config/releases.yaml', 'w'))



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--release', default='', required=False, help='Release to be removed from the auto-merge config', dest='release')
    args = parser.parse_args()
    sam = stop_auto_merge()
    release_to_be_removed = args.release if args.release else sam.get_release_to_be_removed()
    sam.update_release_map(release_to_be_removed)
