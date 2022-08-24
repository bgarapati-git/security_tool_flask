import json
import subprocess

from constants import service_name, gcf, rule_id, gcf_rule, function_name, high_priority, priority, status_const, \
    message, compliant, pass_status, public_function
from src.common_functions import get_iam_policy, get_yaml_entities_public
from src.common_functions import get_list


def get_function_name_list():
    method = get_function_name_list.__name__
    function_names = []
    try:
        command = "gcloud functions list --format=json"
        function_list = subprocess.getoutput(command)
        json_list = json.loads(function_list)
        function_names = [i['name'].split('/')[-1] for i in json_list]
    except Exception as e:
        print(f'Exception occurred in {method_name} method exception is{e}')
    print(f'cloud function name list is {function_names}')
    return function_names


def get_function_status(function_iam_policy, yaml_entities):
    method_name = get_function_status.__name__
    list_ = []
    if len(yaml_entities) == 0:
        return
    try:
        iam_dict = json.loads(function_iam_policy)
        if "bindings" in iam_dict:
            list_ = [function_iam['members'] for function_iam in iam_dict['bindings']
                     if any(elem in function_iam['members'] for elem in yaml_entities)]
    except Exception as e:
        print(f'Exception occurred in {method_name} method exception is{e}')
    return "Fail" if len(list_) > 0 else "Pass"


def check_iam_policy_gcf(func_list, yaml_entities):
    method_name = check_iam_policy_gcf.__name__
    status_list = []
    print(f'function ist is {func_list}')
    try:
        for function in func_list:
            command = 'gcloud functions get-iam-policy --format=json' + ' ' + function
            function_iam_policy = get_iam_policy(function, command)
            print(f'function iam policy is {function_iam_policy}')
            status = get_function_status(function_iam_policy, yaml_entities)
            status_list.append(
                {service_name: gcf, rule_id: gcf_rule, function_name: function, priority: high_priority,
                 status_const: status, message: compliant if status == pass_status else public_function})
    except Exception as e:
        print(f'Exception occurred in {method_name} method exception is{e}')
    print(f'status_list is {status_list}')
    return status_list

