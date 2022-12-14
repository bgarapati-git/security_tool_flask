from constants import service_name, rule_id, priority, status_const, message, public_bucket, \
    pass_status, high_priority, gcs, gcs_rule, compliant, entity
from src.common_functions import get_iam_policy, get_status


def check_iam_policy(bucket_list, yaml_entities):
    method_name = check_iam_policy.__name__
    status_list = []
    try:
        for bucket in bucket_list:
            command = 'gsutil iam get' + ' ' + bucket
            bucket_iam_policy = get_iam_policy(bucket, command)
            status = get_status(bucket_iam_policy, yaml_entities)
            status_list.append(
                {service_name: gcs, rule_id: gcs_rule, entity: bucket, priority: high_priority,
                 status_const: status, message: compliant if status == pass_status else public_bucket})
    except Exception as e:
        print(f'Exception occurred in {method_name} method exception is{e}')
    print(f'status_list is {status_list}')
    return status_list


