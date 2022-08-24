import json
import subprocess


import yaml
from yaml import SafeLoader

from constants import iam_message, specialGroup, groupByEmail, userByEmail, big_query, service_name, rule_id, \
    data_set_name, status_const, pass_status, fail_status, message, compliant, bq_rule_1, bq_rule_2, bq_rule_3, \
    bq_rule_4, bq_rule_0


def get_bq_dataset_list(project_id):
    method = get_bq_dataset_list.__name__
    dataset_list=[]
    try:
        list_ = subprocess.getoutput('bq ls --format=prettyjson --project_id' + ' ' + project_id)
        i=list_.find("[")
        #print(list_[i:])
        json_data = json.loads(list_[i:])
        print(json_data)
        dataset_list = [j['datasetId'] for j in [i['datasetReference'] for i in json_data]]
        print(f'dataset_list is {dataset_list}')
    except Exception as e:
        print(f'Exception occurred in {method} method exception is {e}')
    return dataset_list


def get_yaml(project_id, filename):
    method = get_yaml.__name__
    yaml_dict = {}
    try:
        # filename='../rule_yaml/' + project_id + '_bq_' +'rules.yaml'
        print(f'file name is {filename}')
        with open(filename) as f:
            data = yaml.load(f, Loader=SafeLoader)
            print(f'\nyaml data is {data}')
            yaml_ = [yaml_dict.update(v3) for v1 in data['rules'] for v2 in v1['bindings'] for v3 in v2['members']]
            print(f'result is {yaml_dict}')

    except Exception as e:
        print(f'Exception occured in {method} method exception is {e}')
    return yaml_dict


def get_list_roles_users(project_id, dataset):
    method = get_list_roles_users.__name__
    role_data = []
    try:
        role_data = subprocess.getoutput('bq show --format=prettyjson' + ' ' + project_id + ':' + dataset)
        role_data_=role_data[role_data.find("{"):]
    except Exception as e:
        print(f'Exception occurred in {method} method exception is {e}')
    return role_data_


def check_rules_yaml(project_id, dataset_list, filename):
    method = check_rules_yaml.__name__
    status_list = []

    try:
        yaml_data = get_yaml(project_id, filename)
        gmail = yaml_data['userByEmail'].split('*')[1]
        google_groups = yaml_data['groupByEmail'].split('*')[1]
        print(f'yaml_data is {yaml_data}')
        for dataset in dataset_list:
            failed_list = []
            roles = get_list_roles_users(project_id, dataset)
            print(f'roles is {roles}')
            json_ = json.loads(roles)
            dict_list = json_['access']
            status_pass = {service_name: big_query, rule_id: bq_rule_0, data_set_name: dataset,
                           status_const: pass_status,
                           message: compliant}
            for i in dict_list:
                if 'specialGroup' in i.keys() and i['specialGroup'] == yaml_data['specialGroup']:
                    status = {service_name: big_query, rule_id: bq_rule_1, data_set_name: dataset,
                              status_const: fail_status, message: specialGroup}
                    failed_list.append(status)

                if 'iamMember' in i.keys() and i['iamMember'] == yaml_data['iamMember']:
                    status = {service_name: big_query, rule_id: bq_rule_2, data_set_name: dataset,
                              status_const: fail_status, message: iam_message}
                    failed_list.append(status)

                if 'groupByEmail' in i.keys() and google_groups in i['groupByEmail']:
                    status = {service_name: big_query, rule_id: bq_rule_3, data_set_name: dataset,
                              status_const: fail_status, message: groupByEmail}
                    failed_list.append(status)

                if 'userByEmail' in i.keys() and gmail in i['userByEmail']:
                    status = {service_name: big_query, rule_id: bq_rule_4, data_set_name: dataset,
                              status_const: fail_status, message: userByEmail}
                    failed_list.append(status)

            status_list.extend(failed_list) if len(failed_list) > 0 else status_list.append(status_pass)
            # print(f'status is {status}')
            # status_list.append(status)
    except Exception as e:
        print(f'Exception occurred in {method} method exception is {e}')
    return status_list

