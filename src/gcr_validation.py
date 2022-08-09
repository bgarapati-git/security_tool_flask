

from constants import service_name, gcr, rule_id, gcr_rule, gcr_service_name, priority, high_priority, status_const, \
    message, public_entity, compliant, pass_status, public_bucket, public_run
from src.common_functions import get_iam_policy, get_status, get_list, get_yaml_entities_public


def check_iam_policy_gcr(service_list, yaml_entities):
    method_name = check_iam_policy_gcr.__name__
    status_list = []
    try:
        for service in service_list:
            command = 'gcloud run services get-iam-policy --region=us-central1 --format=json' + ' ' + service
            service_iam_policy = get_iam_policy(service, command)
            status = get_status(service_iam_policy, yaml_entities)
            status_list.append(
                {service_name: gcr, rule_id: gcr_rule,gcr_service_name : service, priority: high_priority,
                 status_const: status,message:compliant if status == pass_status else public_run})
    except Exception as e:
        print(f'Exception occurred in {method_name} method exception is{e}')
    print(f'status_list is {status_list}')
    return status_list


if __name__ == '__main__':
    project_id = 'badri-29apr2022-scrumteam'
    command_service = "gcloud run services list --format=" + 'value(name)'
    service_list = get_list(project_id, command_service)
    file_name = '../rule_yaml/badri-29apr2022-scrumteam' + '_gcr_' + 'rules.yaml'
    entities = get_yaml_entities_public(file_name)
    status_list_gcr = check_iam_policy_gcr(service_list, entities)
