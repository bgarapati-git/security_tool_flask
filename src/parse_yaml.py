import json
import yaml
from yaml.loader import SafeLoader


def get_yaml_entities(project_id):
    # Open the file and load the file
    method_name = get_yaml_entities.__name__
    entities=[]
    try:
        file_name = '../rule_yaml/' + project_id + '_gcs_'+'rules.yaml'
        print(f'filename is {file_name}')
        with open(file_name) as f:
            data = yaml.load(f, Loader=SafeLoader)
            print(f'yaml data is {data} ')
            entities = [key['entity'] for key in data["rules"]]
    except Exception as e:
        print(f'Exception occurred in {method_name} method exception is{e}')
    return entities


def get_bucket_status(bucket_iam_policy, yaml_entities):
    method_name = get_bucket_status.__name__
    if len(yaml_entities) == 0:
        return
    try:
        iam_dict = json.loads(bucket_iam_policy)
        list_ = [bucket_iam['members'] for bucket_iam in iam_dict['bindings']
                 if any(elem in bucket_iam['members'] for elem in yaml_entities)]
    except Exception as e:
        print(f'Exception occurred in {method_name} method exception is{e}')
    return "Fail" if len(list_) > 0 else "Pass"


