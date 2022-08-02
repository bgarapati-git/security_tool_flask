from constants import service_name, rule_id, bucket_name, priority, status_const, message, public_bucket, \
    pass_status, high_priority, gcs, gcs_rule, compliant
from src.common_functions import get_list, get_iam_policy, get_status, get_yaml_entities_public


def check_iam_policy(bucket_list, yaml_entities):
    method_name = check_iam_policy.__name__
    status_list = []
    try:
        for bucket in bucket_list:
            command = 'gsutil iam get' + ' ' + bucket
            bucket_iam_policy = get_iam_policy(bucket, command)
            status = get_status(bucket_iam_policy, yaml_entities)
            status_list.append(
                {service_name: gcs, rule_id: gcs_rule, bucket_name: bucket, priority: high_priority,
                 status_const: status, message: compliant if status == pass_status else public_bucket})
    except Exception as e:
        print(f'Exception occurred in {method_name} method exception is{e}')
    print(f'status_list is {status_list}')
    return status_list


if __name__ == '__main__':
    project_id = 'badri-29apr2022-scrumteam'
    command_ = 'gsutil ls -p' + ' ' + project_id
    bucket_list_ = get_list(project_id, command_)
    filename = '../rule_yaml/' + project_id + '_gcs_' + 'rules.yaml'
    #filename = '/rule_yaml/' + project_id + '_gcs_' + 'rules.yaml'
    yaml_entities_ = get_yaml_entities_public(filename)
    status_list = check_iam_policy(bucket_list_, yaml_entities_)
