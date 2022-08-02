import json
import subprocess

import yaml
from yaml import SafeLoader

from constants import iam_message, specialGroup, groupByEmail, userByEmail, big_query, service_name, rule_id, \
    data_set_name, status_const, pass_status, fail_status, message, compliant, bq_rule_1, bq_rule_2, bq_rule_3, \
    bq_rule_4


def get_bq_dataset_list(project_id):
    method = get_bq_dataset_list.__name__
    try:
        list_ = subprocess.getoutput('bq ls --format=prettyjson --project_id' + ' ' + project_id)
        json_data = json.loads(list_)
        dataset_list = [j['datasetId'] for j in [i['datasetReference'] for i in json_data]]
        print(f'dataset_list is {dataset_list}')
    except Exception as e:
        print(f'Exception occurred in {method} method exception is {e}')
    return dataset_list


def get_yaml(project_id, filename):
    method = get_yaml.__name__
    try:
        # filename='../rule_yaml/' + project_id + '_bq_' +'rules.yaml'
        print(f'file name is {filename}')
        with open(filename) as f:
            data = yaml.load(f, Loader=SafeLoader)
            print(f'\nyaml data is {data}')
            yaml_dict = {}
            yaml_ = [yaml_dict.update(v3) for v1 in data['rules'] for v2 in v1['bindings'] for v3 in v2['members']]
            print(f'result is {yaml_dict}')

    except Exception as e:
        print(f'Exception occured in {method} method exception is {e}')
    return yaml_dict


def get_list_roles_users(project_id, dataset):
    method = get_list_roles_users.__name__
    try:
        role_data = subprocess.getoutput('bq show --format=prettyjson' + ' ' + project_id + ':' + dataset)
    except Exception as e:
        print(f'Exception occurred in {method} method exception is {e}')
    return role_data


def check_rules_yaml(project_id, dataset_list, filename):
    method = check_rules_yaml.__name__
    try:
        yaml_data = get_yaml(project_id, filename)
        print(f'yaml_data is {yaml_data}')

        # status messages
        # iam_message = 'iamMember is public'
        # specialGroup = 'specialGroup is public'
        # groupByEmail = 'groupByEmail contains google groups'
        # userByEmail = 'userByEmail contains gmail'

        status_list = []
        for dataset in dataset_list:
            roles = get_list_roles_users(project_id, dataset)
            print(f'roles is {roles}')
            json_ = json.loads(roles)
            dict_list = json_['access']
            status = {service_name: big_query, rule_id: bq_rule_1, data_set_name: dataset, status_const: pass_status,
                      message: compliant}
            for i in dict_list:
                if 'iamMember' in i.keys() and i['iamMember'] == yaml_data['iamMember']:
                    status = {service_name: big_query, rule_id: bq_rule_2, data_set_name: dataset,
                              status_const: fail_status, message: iam_message}
                    break
                elif 'specialGroup' in i.keys() and i['specialGroup'] == yaml_data['specialGroup']:
                    status = {service_name: big_query, rule_id: bq_rule_2, data_set_name: dataset,
                              status_const: fail_status, message: specialGroup}
                    break
                elif 'groupByEmail' in i.keys() and i['groupByEmail'] == yaml_data['groupByEmail']:
                    status = {service_name: big_query, rule_id: bq_rule_3, data_set_name: dataset,
                              status_const: fail_status, message: groupByEmail}
                    break
                elif 'userByEmail' in i.keys() and i['userByEmail'] == yaml_data['userByEmail']:
                    status = {service_name: big_query, rule_id: bq_rule_4, data_set_name: dataset,
                              status_const: fail_status, message: userByEmail}
                    break

            print(f'status is {status}')
            status_list.append(status)
    except Exception as e:
        print(f'Exception occurred in {method} method exception is {e}')
    return status_list


if __name__ == '__main__':
    get_bq_dataset_list('badri-29apr2022-scrumteam')
