import json
import subprocess
import sys

import requests

sys.path.append('../')
from constants import service_name, message, rule_id, priority, status_const, app_engine, ae_rule, url_response, \
    compliant, high_priority, \
    pass_status, fail_status, entity


def get_app_urls(project_id):
    method=get_app_urls.__name__
    urls=[]
    try:
        list_ = subprocess.getoutput('gcloud app services list --format=json --project=' + project_id)
        json_list = json.loads(list_)
        services = [i['id'] for i in json_list]
        print(f' app services {services}')
        for i in services:
            url = subprocess.getoutput('gcloud app browse --service=' + i + ' --no-launch-browser')
            url = url.replace("https", "http")
            urls.append(url)
    except Exception as e:
        print(f'Exception occured in {method} method exception is {e}')
    return urls


def check_app_engine(urls):
    method = check_app_engine.__name__
    status_list = []
    try:
        for i in urls:
            request = requests.get(i)
            resp = request.history
            if '<Response [302]>' in str(resp) or '<Response [301]>' in str(resp):
                status_list.append({service_name: app_engine, rule_id: ae_rule, entity: i, priority: high_priority,
                                status_const: pass_status, message: compliant})
            else:
                status_list.append({service_name: app_engine, rule_id: ae_rule, entity: i, priority: high_priority,
                                status_const: fail_status, message: url_response})
    except Exception as e:
        print(f'Exception occured in {method} method exception is {e}')
    print(status_list)
    return status_list

