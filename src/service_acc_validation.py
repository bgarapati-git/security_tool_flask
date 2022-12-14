import itertools
import json
import subprocess

import yaml
from yaml.loader import SafeLoader

from constants import service_name, iam_role, rule_id, status_const, fail_status, \
    role_svc, message, svc_acnt_rule_1, svc_acnt_rule_2, default_svc, svc_acnt_rule_3, svc_acnt_rule_4, pass_status, \
    compliant, user_managed, priority, high_priority, entity


def get_service_acc_list(project_id):
    method = get_service_acc_list.__name__
    new = []
    try:
        acc_data = (subprocess.getoutput('gcloud iam service-accounts list --project ' + project_id + ' --format=json'))
        #print(f'service account list is {acc_data}')
        jsn_ = json.loads(acc_data)
        new = [j['email'] for j in jsn_]
    except Exception as e:
        print(f'Exception occurred in {method} method exception is {e}')
    return new


def get_yaml_details(project_id, filename):
    method = get_yaml_details.__name__
    yaml_ = []
    try:
        # filename = '../rule_yaml/' + project_id + '_service_' + 'rules.yaml'
        with open(filename) as f:
            data = yaml.load(f, Loader=SafeLoader)
            yaml_ = [i['role'] for i in data['rule-1']]
            rule2 = [i['email'].split('*')[-1] for i in data['rule-2']]
            rule3 = [i['keyType'] for i in data['rule-3']]
            yaml_ = yaml_ + rule2 + rule3
    except Exception as e:
        print(f'Exception occurred in {method} method exception is {e}')
    return yaml_


def get_ser_acc_keytypes(ser_acc):
    method = get_ser_acc_keytypes.__name__
    key_data=[]
    try:
        data = (
            subprocess.getoutput('gcloud iam service-accounts keys list --iam-account=' + ser_acc + ' --format=json'))
        key = json.loads(data)
        key_data = [i['keyType'] for i in key]
    except Exception as e:
        print(f'Exception occurred in {method} method exception is {e}')
    return key_data


def check_rules_yaml_service_accounts(projectId, filename):
    method = check_rules_yaml_service_accounts.__name__
    status_list = []
    pass_list = []
    try:
        email_data = get_service_acc_list(projectId)
        print(f'acc_data is {email_data}')
        failed_service_accounts = []
        yaml_ = get_yaml_details(projectId, filename)

    # checking Rule1
        acc_data = (subprocess.getoutput('gcloud projects get-iam-policy ' + projectId + ' --format=json'))
        jsn_ = json.loads(acc_data)
        members_admin = [i['members'] for i in jsn_['bindings'] if i['role'] in yaml_[:2]]
        final = list(itertools.chain(*members_admin))
        rule_1 = [i.split(':')[-1] for i in final if i.find('serviceAccount') != -1]
        failed_service_accounts.extend(rule_1)
        status_list = [{service_name: iam_role, rule_id: svc_acnt_rule_1, entity: i,priority: high_priority,
                    status_const: fail_status,
                    message: role_svc} for i in rule_1]

    # checking Rule2
        for i in email_data:
            for j in yaml_[3:5]:
                if i.__contains__(j):
                    status_dict = {service_name: iam_role, rule_id: svc_acnt_rule_2, entity: i,priority: high_priority,
                               status_const: fail_status,
                               message: default_svc}
                    status_list.append(status_dict)
                    failed_service_accounts.append(i)

    # Checking Rule3
        for i in email_data:
            key_types = get_ser_acc_keytypes(i)
            if set(yaml_[5:]) & set(key_types):
                status_dict = {service_name: iam_role, rule_id: svc_acnt_rule_3, entity: i,priority: high_priority,
                           status_const: fail_status,
                           message: user_managed}
                status_list.append(status_dict)
                failed_service_accounts.append(i)

        pass_list = [{service_name: iam_role, rule_id: svc_acnt_rule_4, entity: i,priority: high_priority,
                  status_const: pass_status,
                  message: compliant} for i in email_data if i not in failed_service_accounts]
    except Exception as e:
        print(f'Exception occurred in {method} method exception is {e}')
    return status_list + pass_list

