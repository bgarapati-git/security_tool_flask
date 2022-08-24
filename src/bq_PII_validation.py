import sys

sys.path.append('../')

from google.cloud import bigquery
from constants import service_name, message, rule_id, priority, status_const, big_query, bq_dp_rule, \
    Failed_due_to_exposed, high_priority, \
    pass_status, fail_status, PII_not_exposed, entity
from src.common_functions import get_yaml_data


# Construct a BigQuery client object.
def check_for_PII_data(project_id, dataset_and_table, entity, regex):
    client = bigquery.Client()
    table_ = project_id + "." + dataset_and_table
    print(regex)
    sql_query = """
       SELECT """ + entity + """ , REGEXP_CONTAINS(CAST(""" + entity + """ AS STRING), r'""" + regex + """') AS is_valid
       FROM `""" + table_ + """`
       LIMIT 100;
    """
    print(sql_query)
    status = "Fail"
    method_name = check_for_PII_data.__name__
    try:
        query_job = client.query(sql_query)  # Make an API request.
        res = query_job.result()  # Wait for the job to complete.

        list_ = []
        for row in res:
            list_.append(row["is_valid"])
        print(list_)
        # if True in list_:
        #     status="Fail"
        # else:
        #     status="Pass"
        status = "Fail" if True in list_ else "Pass"
    except Exception as e:
        print(f'Exception occurred in {method_name} method exception is{e}')
        if '403 Access Denied' in str(e):
            status = "Pass"
    print(status)
    return (status)


def bq_PII_data_validation(project_id, dataset_and_table, entity_list, regex_list):
    method = bq_PII_data_validation.__name__
    status_list = []
    try:
        for i in range(len(entity_list)):
            Failed_entities = []
            dataset_table = dataset_and_table[i]
            for j in range(len(entity_list[i])):
                Status = check_for_PII_data(project_id, dataset_table, entity_list[i][j], regex_list[i][j])
                if Status == "Fail":
                    Failed_entities.append(entity_list[i][j])
            if len(Failed_entities) == 0:
                status_list.append(
                    {service_name: big_query, rule_id: bq_dp_rule, entity: dataset_table, priority: high_priority,
                     status_const: pass_status, message: PII_not_exposed})
            else:
                s = ''
                for i in Failed_entities:
                    # if i == Failed_entities[-1]:
                    #     s = s + i
                    # else:
                    #     s = s + i + ", "
                    s = s + i if i == Failed_entities[-1] else s + i + ", "
                status_list.append(
                    {service_name: big_query, rule_id: bq_dp_rule, entity: dataset_table, priority: high_priority,
                     status_const: fail_status, message: Failed_due_to_exposed + s})
    except Exception as e:
        print(f'Exception occurred in {method} method exception is{e}')
    print(status_list)
    return (status_list)


def get_yaml(file_name):
    method_name = get_yaml.__name__
    dataset_and_table = []
    entities = []
    regex = []
    try:
        data = get_yaml_data(file_name)
        dataset_and_table = [key['Dataset_and_Table'] for key in data['rules']]
        PII_data = [key['PII_data'] for key in data["rules"]]
        # print(PII_data)
        entities = []
        regex = []
        for i in range(len(PII_data)):
            entities.append([key['entity'] for key in PII_data[i]])
            regex.append([key['regex'] for key in PII_data[i]])
    except Exception as e:
        print(f'Exception occurred in {method_name} method exception is{e}')
    return (dataset_and_table, entities, regex)
