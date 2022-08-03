import requests
import subprocess
from constants import service_name,message,rule_id,priority,status_const,app_engine,ae_rule,url,url_response,compliant,high_priority, \
    pass_status,fail_status

def get_app_urls(project_id):
    list_= subprocess.getoutput('gcloud app services list --project='+project_id)
    services=(list_.split("\n")[::3])
    urls=[]
    for i in services:
        i=i[9:]
        url=subprocess.getoutput('gcloud app browse --service='+i + ' --no-launch-browser')
        url=url.replace("https","http")
        #url='http'+url[5:]
        urls.append(url)
    return urls

def check_app_engine(urls):
    status_list=[]
    for i in urls:
        request=requests.get(i)
        #print(request)
        resp=request.history
        #print(resp)
        if  '<Response [302]>' in str(resp) or '<Response [301]>' in str(resp) :
            status_list.append({service_name: app_engine, rule_id: ae_rule, url: i, priority: high_priority,
                                status_const:pass_status, message:compliant})
        else:
            status_list.append({service_name: app_engine, rule_id: ae_rule, url: i, priority: high_priority,
                                status_const:fail_status, message:url_response})
    print(status_list)
    return status_list

if __name__ == '__main__':
    urls=get_app_urls('badri-29apr2022-scrumteam')
    check_app_engine(urls)