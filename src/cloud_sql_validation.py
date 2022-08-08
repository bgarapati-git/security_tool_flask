

import json
import subprocess

import yaml
from yaml import SafeLoader

from constants import pass_status, fail_status, service_name, cloud_sql, rule_id, cloud_sql_rule, sql_instance, \
    status_const, message, compliant, cloud_sql_public


def get_cloud_sql_list(project_id):
    method_name = get_cloud_sql_list.__name__
    try:
        list_ = subprocess.getoutput('gcloud sql instances list --format="(NAME)" --project' + ' ' + project_id)
        sql_list = list_.split("\n")[1:]
        print(f'sql_list {sql_list}')
    except Exception as e:
        print(f'Exception occurred in {method_name} method exception is{e}')
    return sql_list


def get_ip_config(sql_name):
    method_name = get_ip_config.__name__
    try:
        ip = subprocess.getoutput("gcloud sql instances describe" + " " + sql_name + " " + "--format=json")
        ip_json = json.loads(ip)
        if "authorizedNetworks" in ip_json['settings']['ipConfiguration'].keys():
            authorized_networks = ip_json['settings']['ipConfiguration']['authorizedNetworks']
            ip_config = [i['value'] for i in authorized_networks]
            print(f'public_ip is  {ip_config}')
        else:
            ip_config = ip_json['settings']['ipConfiguration']['privateNetwork']
            print(ip_config)
    except Exception as e:
        print(f'Exception occurred in {method_name} method exception is{e}')
    return ip_config


def get_yaml_data_sql(project_id,file_name):
    method_name = get_yaml_data_sql.__name__
    try:
        #file_name = '../rule_yaml/' + project_id + '_cloud_sql_' + 'rules.yaml'
        print(f'filename is {file_name}')
        with open(file_name) as f:
            data = yaml.load(f, Loader=SafeLoader)
            print(f'yaml data is {data} ')
            ip = next(key['public_ip'] for key in data["rules"])
            print(f'ip value to compare is {ip} type is {type(ip)}')
    except Exception as e:
        print(f'Exception occurred in {method_name} method exception is{e}')
    return ip


def check_public_ip(sql_list, project_id,file_name):
    method_name = check_public_ip.__name__
    status_list = []
    try:
        yaml_ = get_yaml_data_sql(project_id, file_name)
        for i in sql_list:
            public_ip = get_ip_config(i)
            status = fail_status if (yaml_ in public_ip) else pass_status
            status_dict = {service_name: cloud_sql, rule_id: cloud_sql_rule, sql_instance: i, status_const: status,
                           message: compliant if status == pass_status else cloud_sql_public}
            status_list.append(status_dict)
    except Exception as e:
        print(f'Exception occurred in {method_name} method exception is{e}')
    return status_list
