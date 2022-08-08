

import requests
import json
from constants import service_name,message,rule_id,priority,status_const,api_security,api_rule,url,compliant,high_priority, \
    pass_status,fail_status

import yaml 
def get_urls(filename):
    method=get_urls.__name__
    try:
        with open(filename) as file: 
             documents = yaml.full_load(file) 
             urls = [] 
             for app in documents["endpoints"]: 
                urls += documents["endpoints"][app]["url"] 
    except Exception as e:
        print(f'Exception occured in {method} method exception is {e}')
    print(urls)
    return(urls)

def check_api(urls): 
    status_list=[]
    empty_token_header ={
                        'Authorization': "",
                        'Content-Type': 'application/json'
                        }
    wrong_token_header ={
                        'Authorization': 'Bearer 111111111111111111111',
                        'Content-Type': 'application/json'
                        }
    for i in urls:
        status=[]
        response1 = requests.request("POST",i)
        status.append(response1.status_code)
        response2 = requests.request("POST",i,headers=empty_token_header)
        status.append(response2.status_code)
        response3 = requests.request("POST",i,headers=wrong_token_header)
        status.append(response3.status_code)
        print(status)
        #print(response.status_code)
        value=200
        if value in status:
           status_list.append({service_name: api_security, rule_id: api_rule, url: i, priority: high_priority,
                                status_const:fail_status, message:compliant})
        else:
           status_list.append({service_name: api_security, rule_id: api_rule, url: i, priority: high_priority,
                                status_const:pass_status, message:compliant})
    print(status_list)
    return(status_list)

'''if __name__ == '__main__':   
    urls=(get_urls())
    check_api(urls)'''