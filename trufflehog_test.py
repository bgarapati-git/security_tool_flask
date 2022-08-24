import os
import subprocess
import json
#os.system("truffleHog --json https://github.com/riju11sharma/NewRepo.git >>output1.json")
#output = subprocess.getoutput('truffleHog --regex --json --max_depth 2 --rules custom_regex.json --entropy=False https://github.com/riju11sharma/NewRepo.git > output.json')

output = subprocess.getoutput('truffleHog --regex --json --rules custom_regex.json --entropy=False https://github.com/riju11sharma/NewRepo.git > output.json')
#json_=json.loads(output)

dict_list=[]
for line1 in open('output.json', 'r'):
    print(f'line is {json.loads(line1)}')
    line=json.loads(line1)
    dict_list.append({'branch' :line['branch'],'commit' :line['commit'],'commitHash' :line['commitHash'],'path' :line['path'],'reason' :line['reason']})

print(f'dict_list is {dict_list}')


if __name__=="__main__":
    print (f'type is {type(output)}')