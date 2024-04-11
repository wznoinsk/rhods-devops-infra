import os

import requests
from datetime import datetime
import traceback

BASE_URL = 'https://quay.io/api/v1'
START_DATE = datetime.strptime('04-05-24 00:00:00 -0000', '%m-%d-%y %H:%M:%S %z')
END_DATE = datetime.strptime('04-09-24 23:59:59 -0500', '%m-%d-%y %H:%M:%S %z')

class quay_controller:
    def __init__(self, org):
        self.org = org


    def get_all_repos(self):
        repositories = []
        url = f'{BASE_URL}/repository?last_modified=true&namespace={self.org}&popularity=true&public=true&quota=true'
        response = requests.get(url)
        if response.json():
            resp_object = response.json()
            repositories += [repo['name'] for repo in resp_object['repositories']]
            while 'next_page' in resp_object:
                next_url = f"{url}&next_page={resp_object['next_page']}"
                response = requests.get(next_url)
                resp_object = response.json()
                repositories += [repo['name'] for repo in resp_object['repositories']]

        return repositories


    def get_all_tags_between_given_dates(self, repo):
        tags = []
        url = f'{BASE_URL}/repository/{self.org}/{repo}/tag/?limit=100&onlyActiveTags=true'
        try:
            for page in range(1, 100):
                page_url = f"{url}&page={page}"
                response = requests.get(page_url)
                resp_object = response.json()
                tags += [{'name':tag['name'], 'digest': tag['manifest_digest'], 'created_on': tag['last_modified']} for tag in resp_object['tags'] if START_DATE <= datetime.strptime(tag['last_modified'], '%a, %d %b %Y %H:%M:%S %z') <= END_DATE]
                if not resp_object['tags']:
                    break
                last_date = datetime.strptime(resp_object['tags'][-1]['last_modified'], '%a, %d %b %Y %H:%M:%S %z')
                if last_date <= START_DATE:
                    break
            print(f'{self.org}/{repo}', len(tags))
        except Exception as e:
            print(e)
            print(f' exception while procesing {self.org}/{repo}')
            print(traceback.format_exc())

        return tags

    def get_tag_details(self, repo, tag):
        url = f'{BASE_URL}/repository/{self.org}/{repo}/tag/?specificTag={tag["name"]}'
        response = requests.get(url)
        tag = response.json()['tags'][0]
        return tag



    def delete_tag(self, repo, tag):
        url = f'{BASE_URL}/repository/{self.org}/{repo}/tag/{tag["name"]}'
        try:
            tag_details = self.get_tag_details(repo, tag)
            if START_DATE <= datetime.strptime(tag_details['last_modified'], '%a, %d %b %Y %H:%M:%S %z') <= END_DATE:
                with open('Quay-Cleanup-Logs.txt', 'a') as log:
                    print(f'Deleting quay.io/{self.org}/{repo}@{tag["digest"]}')
                    log.write(f'Deleting quay.io/{self.org}/{repo}@{tag["digest"]}\n')
                    response = requests.delete(url, headers={'Authorization': f'Bearer {os.environ[self.org + "_token"]}'})
                    print(response.status_code)
                    print(f'Deleted quay.io/{self.org}/{repo}@{tag["digest"]}')
                    log.write(f'Deleted quay.io/{self.org}/{repo}@{tag["digest"]}\n')
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            raise e
