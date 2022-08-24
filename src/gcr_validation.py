import json
import subprocess

from constants import service_name, gcr, rule_id, gcr_rule, priority, high_priority, status_const, \
    message, compliant, pass_status, public_run, entity
from src.common_functions import get_iam_policy, get_status


def get_gcr_list():
    method_name = get_gcr_list.__name__
    gcr_names = []
    try:
        command = "gcloud run services list --format=json"
        gcr_list = subprocess.getoutput(command)
        json_list = json.loads(gcr_list)
        gcr_names = [i['metadata']['name'] for i in json_list]
    except Exception as e:
        print(f'Exception occurred in {method_name} method exception is{e}')
    print(f'gcr name list is {gcr_names}')
    return gcr_names


def check_iam_policy_gcr(service_list, yaml_entities):
    method_name = check_iam_policy_gcr.__name__
    status_list = []
    location=''
    for i in yaml_entities:
        if type(i) is dict:
            location= i['location']
            break
    try:
        for service in service_list:
            command = 'gcloud run services get-iam-policy --region='+location+' '+'--format=json' + ' ' + service
            service_iam_policy = get_iam_policy(service, command)
            status = get_status(service_iam_policy, yaml_entities)
            status_list.append(
                {service_name: gcr, rule_id: gcr_rule, entity: service, priority: high_priority,
                 status_const: status, message: compliant if status == pass_status else public_run})
    except Exception as e:
        print(f'Exception occurred in {method_name} method exception is{e}')
    print(f'status_list is {status_list}')
    return status_list
