import requests
import json
from constants import service_name, message, rule_id, priority, status_const, api_security, api_rule, url, compliant, \
    high_priority, \
    pass_status, fail_status, api_unsecured

import yaml 
def get_urls(filename):
    method=get_urls.__name__
    urls = []
    methods = []
    try:
        with open(filename) as file: 
             documents = yaml.full_load(file) 
             for app in documents["endpoints"]: 
                urls += documents["endpoints"][app]["url"] 
                methods +=documents["endpoints"][app]["method"]
    except Exception as e:
        print(f'Exception occured in {method} method exception is {e}')
    print(urls)
    return(urls,methods)

def check_api(urls,methods): 
    method=check_api.__name__
    status_list=[]
    try:
        empty_token_header ={
                        'Authorization': "",
                        'Content-Type': 'application/json'
                        }
        wrong_token_header ={
                        'Authorization': 'Bearer 111111111111111111111',
                        'Content-Type': 'application/json'
                        }
        for i in range(len(urls)):
            status=[]
            response1 = requests.request(methods[i],urls[i])
            status.append(response1.status_code)
            response2 = requests.request(methods[i],urls[i],headers=empty_token_header)
            status.append(response2.status_code)
            response3 = requests.request(methods[i],urls[i],headers=wrong_token_header)
            status.append(response3.status_code)
            print(status)
            #print(response.status_code)
            value=200
            if value in status:
                status_list.append({service_name: api_security, rule_id: api_rule, url: urls[i], priority: high_priority,
                                status_const:fail_status, message:api_unsecured})
            else:
                status_list.append({service_name: api_security, rule_id: api_rule, url: urls[i], priority: high_priority,
                                status_const:pass_status, message:compliant})
    except Exception as e:
        print(f'Exception occured in {method} method exception is {e}')
    print(status_list)
    return(status_list)
