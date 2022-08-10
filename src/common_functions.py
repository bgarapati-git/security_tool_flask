import json
import subprocess

import pandas as pd
import yaml
from yaml import SafeLoader


def read_project_json():
    method_name = read_project_json.__name__
    file_name = '../project_ids.json'
    project_ids = []
    try:
        with open(file_name) as f:
            data = json.load(f)
        project_ids = [project['project_id'] for project in data['projects']]
        print(f'json data is {data} project_ids is {project_ids}')
    except Exception as e:
        print(f'Exception occurred in {method_name} method exception is{e}')
    return project_ids


def convert_to_html(status_list, file, app_root_path, service_name):
    method_name = convert_to_html.__name__
    print(f'In method {method_name} status_list is {status_list}')
    count_dict = {}
    try:
        df = pd.DataFrame.from_records(status_list)
        df_fail = df[df.Status == "Fail"]
        fail_count = len(df_fail)
        df_pass = df[df.Status == "Pass"]
        pass_count = len(df_pass)
        count_dict = {"filename": file, "service": service_name, "fail_count": fail_count, "pass_count": pass_count}
        df = df.sort_values(by='Status')

        html_string = '''
        <html>
          <head><title>Report</title></head>
          <link rel="stylesheet" type="text/css" href="../static/css/styles.css"/>
          <script type="text/javascript" src="../static/css/script.js"></script>          
          {table}
          <script>
            createtable();
          </script>
        </html>.
        '''

        # OUTPUT AN HTML FILE
        with open(app_root_path + "/reports/" + file, 'w') as f:
            print(f'app_root_path is {app_root_path}')
            f.write(html_string.format(table=df.to_html(index=False, classes='mystyle')))
            f.close()
    except Exception as e:
        print(f'Exception occurred in {method_name} method exception is{e}')
    return count_dict


def execute_command(command):
    output = subprocess.getoutput(command)
    return output


def read_yaml(file_name):
    with open(file_name) as f:
        data = yaml.load(f, Loader=SafeLoader)
        print(f'yaml file is {file_name} and yaml data is {data} ')
    return data


def get_iam_policy(service_name, command):
    method_name = get_iam_policy.__name__
    try:
        iam_policy = subprocess.getoutput(command)
    except Exception as e:
        print(f'Exception occurred in {method_name} method exception is{e}')
    return iam_policy


def get_yaml_data(file_name):
    # Open the file and load the file
    method_name = get_yaml_data.__name__
    try:
        print(f'filename is {file_name}')
        with open(file_name) as f:
            data = yaml.load(f, Loader=SafeLoader)
            print(f'yaml data is {data} ')
    except Exception as e:
        print(f'Exception occurred in {method_name} method exception is{e}')
    return data


def get_yaml_entities_public(file_name):
    # Open the file and load the file
    method_name = get_yaml_entities_public.__name__
    try:
        data = get_yaml_data(file_name)
        entities = [key['entity'] for key in data["rules"]]
    except Exception as e:
        print(f'Exception occurred in {method_name} method exception is{e}')
    return entities


def get_list(project_id, command):
    # List buckets in a project 'gsutil ls -p PROJECT_ID'
    method_name = get_list.__name__
    service_list = []
    try:
        services = subprocess.getoutput(command)
        service_list = services.split('\n')
    except Exception as e:
        print(f'Exception occurred in {method_name} method exception is{e}')
    return service_list


def get_status(iam_policy, entities):
    method_name = get_status.__name__
    print(f'iam_policy is {iam_policy} and entities is {entities}')
    list_ = []
    if len(entities) == 0:
        return
    try:
        iam_dict = json.loads(iam_policy)
        list_ = [iam['members'] for iam in iam_dict['bindings']
                 if any(elem in iam['members'] for elem in entities)]
    except Exception as e:
        print(f'Exception occurred in {method_name} method exception is{e}')
    return "Fail" if len(list_) > 0 else "Pass"
