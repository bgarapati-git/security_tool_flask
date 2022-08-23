import os
import sys
sys.path.append('../')
import json
import subprocess

from src.common_functions import get_yaml_data
from constants import repository,branch,commit_name,commit_hash,git_validate,path,reason,service_name

def get_url(file_name):
    method=get_url.__name__
    try:
        data=get_yaml_data(file_name)
        url=[i['git_url'] for i in data['rules']]
    except Exception as e:
        print(f'Exception occured in {method} method exception is {e}')
    return url

def get_secrets(urls, app_root_path, file):
    method=get_secrets.__name__
    try:
        dict_list=[]
        for git_url in urls:
            output=subprocess.getoutput('trufflehog --regex --json --entropy=False ' + git_url + ' > '+app_root_path+'/reports/output.json')
            #print(output)
            file_name=app_root_path+'/reports/output.json'
            for line1 in open(file_name, 'r'):
                #print(f'line is {json.loads(line1)}')
                line=json.loads(line1)
                dict_list.append({service_name : git_validate, repository : git_url, branch : line['branch'], commit_name : line['commit'], commit_hash :line['commitHash'][7:], path : line['path'], reason : line['reason']})
            # with open(app_root_path + "/reports/" + file, "w") as outfile:
            #     json.dump(dict_list, outfile)
            print(f'dict_list is {dict_list}')
            os.remove(app_root_path + '/reports/output.json')
    except Exception as e:
        print(f'Exception occured in {method} method exception is {e}')
    return dict_list

if __name__ == '__main__':
    file_name='../rule_yaml/git_rules.yaml'
    url=get_url(file_name)
    app_root_path="D:/security_tool_flask"
    file='result.json'
    print((url))
    get_secrets(url,app_root_path, file)