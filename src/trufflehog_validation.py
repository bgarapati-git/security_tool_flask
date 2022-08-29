import os
import sys
sys.path.append('../')
import json
import subprocess

from src.common_functions import get_yaml_data
from constants import repository,branch,commit_name,commit_hash,git_validate,path,reason,service_name

def get_url(file_name):
    method=get_url.__name__
    url=[]
    try:
        data=get_yaml_data(file_name)
        url=[i['git_url'] for i in data['rules']]
    except Exception as e:
        print(f'Exception occured in {method} method exception is {e}')
    return url

def get_secrets(urls, app_root_path, file):
    method=get_secrets.__name__
    dict_list=[]
    try:       
        for git_url in urls:
            output=subprocess.getoutput('trufflehog --regex --json --entropy=False ' + git_url + ' > '+app_root_path+'/reports/output.json')
            file_name=app_root_path+'/reports/output.json'
            git_url1=git_url[:8] + git_url[git_url.find('@')+1:] if git_url.find('@')!=-1 else git_url
            for line1 in open(file_name, 'r'):
                line=json.loads(line1)
                dict_list.append({service_name : git_validate, repository : git_url1, branch : line['branch'], commit_name : line['commit'], commit_hash :line['commitHash'][:7], path : line['path'], reason : line['reason']})
            print(f'dict_list is {dict_list}')
            out_path=os.path.join(app_root_path,'reports','output.json')
            os.remove(out_path)
    except Exception as e:
        print(f'Exception occured in {method} method exception is {e}')
    return dict_list
