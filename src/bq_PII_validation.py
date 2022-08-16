

from google.cloud import bigquery
from constants import service_name,message,rule_id,priority,status_const,big_query,bq_dp_rule,Failed_due_to_exposed,high_priority, \
    pass_status,fail_status, PII_not_exposed, Dataset, Table
from src.common_functions import get_yaml_data

# Construct a BigQuery client object.
def check_for_PII_data(project_id,dataset,table,entity,regex):
    client = bigquery.Client()
    table_=project_id+"."+dataset+"."+table

    sql_query = """
       SELECT """+entity+""", REGEXP_CONTAINS("""+entity+""", r'"""+regex+"""') AS is_valid
       FROM `"""+table_+"""`;
    """
    print(sql_query)
    query_job = client.query(sql_query) # Make an API request.
    res=query_job.result() # Wait for the job to complete.

    list_=[]
    for row in res:
       list_.append(row["is_valid"])
       #title=row["is_valid"]
       #print(f'{title}')
    print(list_)
    if True in list_:
        status="Fail"
    else:
        status="Pass"
    print(status)
    return(status)

def bq_PII_data_validation(project_id,dataset,table,entity_list,regex_list):
    Failed_entities=[]
    status_list=[]
    for i in range(len(entity_list)):
        Status=check_for_PII_data(project_id,dataset,table,entity_list[i],regex_list[i])
        if Status=="Fail":
            Failed_entities.append(entity_list[i])
    if len(Failed_entities)==0:
        status_list.append({service_name: big_query, rule_id: bq_dp_rule, Dataset: dataset, Table: table, priority: high_priority,
                                status_const:pass_status, message:PII_not_exposed})
    else:
        s=''
        for i in Failed_entities:
            if i==Failed_entities[-1]:
               s=s+i
            else:
               s=s+i+", " 

        status_list.append({service_name: big_query, rule_id: bq_dp_rule, dataset: dataset, table: table, priority: high_priority,
                                status_const:fail_status, message:Failed_due_to_exposed+s})
    print(status_list)
    return(status_list)

def get_yaml(file_name):
    method_name = get_yaml.__name__
    try:
        data = get_yaml_data(file_name)
        dataset=[key['Dataset_name'] for key in data['rules']]
        table=[key['Table_name'] for key in data['rules']]
        PII_data = [key['PII_data'] for key in data["rules"]]
        #print(PII_data)
        entities=[key['entity'] for key in PII_data[0]]
        regex=[key['regex'] for key in PII_data[0]]
    except Exception as e:
        print(f'Exception occurred in {method_name} method exception is{e}')
    #print(entities)
    #print(regex)
    return(dataset[0],table[0],entities,regex)

if __name__ == '__main__':
  file_name = '../rule_yaml/badri-29apr2022-scrumteam' + '_bq_PII_' + 'rule.yaml'
  dataset,table,entity_list,regex_list=get_yaml(file_name)
  bq_PII_data_validation("badri-29apr2022-scrumteam", dataset, table,entity_list,regex_list)

        





