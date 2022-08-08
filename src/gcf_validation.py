

import json

from constants import service_name, gcf, rule_id, gcf_rule, function_name, high_priority, priority, status_const, \
    message, public_entity, compliant, pass_status, public_bucket
from src.common_functions import get_iam_policy, get_status, get_yaml_entities_public

from src.common_functions import get_list


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
            command = 'gcloud functions get-iam-policy --region=us-central1 --format=json' + ' ' + function
            function_iam_policy = get_iam_policy(function, command)
            print(f'function iam policy is {function_iam_policy}')
            status = get_function_status(function_iam_policy, yaml_entities)
            status_list.append(
                {service_name: gcf, rule_id:gcf_rule, function_name: function, priority: high_priority,
                 status_const: status,message:compliant if status == pass_status else public_bucket})
    except Exception as e:
        print(f'Exception occurred in {method_name} method exception is{e}')
    print(f'status_list is {status_list}')
    return status_list


if __name__ == '__main__':
    project_id = 'badri-29apr2022-scrumteam'
    command_function = "gcloud functions list --format=" + 'value(name)'
    function_list = get_list(project_id, command_function)
    file_name = '../rule_yaml/badri-29apr2022-scrumteam' + '_func_' + 'rules.yaml'
    entities = get_yaml_entities_public(file_name)
    status_list_gcf = check_iam_policy_gcf(function_list, entities)
    print(status_list_gcf)
