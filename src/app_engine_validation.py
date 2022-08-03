import requests
import subprocess

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

def check_app_engine(url):
    status_list=[]
    for i in url:
        request=requests.get(i)
        #print(request)
        resp=request.history
        #print(resp)
        if  '<Response [302]>' in str(resp) or '<Response [301]>' in str(resp) :
            status_list.append({"Service": "APP ENGINE", "Rule_ID": "SML-DE-4", "URL": i, "Priority": "Important",
                     "Status": "Pass", "Message": "Security Compliant, URL redirected "})
        else:
            status_list.append({"Service": "APP ENGINE", "Rule_ID": "SML-DE-4", "URL": i, "Priority": "Important",
                     "Status": "Fail", "Message": "URL is not redirected"})
    print(status_list)
    return status_list

if __name__ == '__main__':
    urls=get_app_urls('badri-29apr2022-scrumteam')
    check_app_engine(urls)