from wsgiref import validate
from constants import gcs, big_query, cloud_sql, gcr, gcf, app_engine, api_security, service_accounts, bq_pii, git_validate
from src.api_security_validation import get_urls, check_api
from src.app_engine_validation import get_app_urls, check_app_engine
from src.bq_validation import get_bq_dataset_list, check_rules_yaml
from src.cloud_sql_validation import check_public_ip, get_cloud_sql_list
from src.common_functions import convert_to_html_git, get_list, get_yaml_entities_public, convert_to_html
from src.gcf_validation import check_iam_policy_gcf, get_function_name_list
from src.gcr_validation import check_iam_policy_gcr, get_gcr_list
from src.gcs_validation import check_iam_policy
from src.service_acc_validation import check_rules_yaml_service_accounts
from src.bq_PII_validation import get_yaml, bq_PII_data_validation
from src.trufflehog_validation import get_url, get_secrets
def run_security_tool(project_id, app_root_path):
    method_name = run_security_tool.__name__
    count_dict = []
    try:
        '''count_dict1 = validate_gcs_buckets(project_id, app_root_path)
        count_dict.append(count_dict1)
        count_dict2 = validate_bq(project_id, app_root_path)
        count_dict.append(count_dict2)'''
        count_dict3=validate_bq_PII(project_id, app_root_path)
        count_dict.append(count_dict3)
        '''count_dict4=validate_cloud_sql(project_id, app_root_path)
        count_dict.append(count_dict4)
        count_dict5=validate_service_accounts(project_id, app_root_path)
        count_dict.append(count_dict5)
        count_dict6=validate_cloud_run(project_id, app_root_path)
        count_dict.append(count_dict6)
        count_dict7=validate_cloud_function(project_id, app_root_path)
        count_dict.append(count_dict7)
        count_dict8=validate_app_engine(project_id,app_root_path)
        count_dict.append(count_dict8)
        count_dict9=validate_api_security(project_id, app_root_path)
        count_dict.append(count_dict9)
        count_dict10=validate_git(project_id,app_root_path)
        count_dict.append(count_dict10)'''

        status = "Success"
        status_dict = {"status": status, "report_list": count_dict}
    except Exception as e:
        print(f'Exception occurred in {method_name} method exception is{e}')
        status = "Fail"
        status_dict = {"status": status, "report_list": count_dict}
    return status_dict


def validate_gcs_buckets(project_id, app_root_path):
    service_name = gcs
    file_name = app_root_path + '/rule_yaml/' + 'gcs_' + 'rules.yaml'
    command = 'gsutil ls -p' + ' ' + project_id
    bucket_list = get_list(project_id, command)
    yaml_entities = get_yaml_entities_public(file_name)
    status_list_gcs = check_iam_policy(bucket_list, yaml_entities)
    file = 'gcs_status_report.html'
    count_dict = convert_to_html(status_list_gcs, file, app_root_path, service_name)
    return count_dict


def validate_bq(project_id, app_root_path):
    service_name = big_query
    filename = app_root_path + '/rule_yaml/' + 'bq_' + 'rules.yaml'
    dataset_list = get_bq_dataset_list(project_id)
    status_list_bq = check_rules_yaml(project_id, dataset_list, filename)
    file = 'bq_status_report.html'
    count_dict = convert_to_html(status_list_bq, file, app_root_path, service_name)
    return count_dict

def validate_bq_PII(project_id, app_root_path):
    service_name = bq_pii
    #file_name = '../rule_yaml/' + 'bq_PII_rule.yaml'
    file_name = app_root_path + '/rule_yaml/' + 'bq_PII_rule.yaml'
    dataset_and_table, entity_list, regex_list=get_yaml(file_name)
    status_list_bq_PII = bq_PII_data_validation(project_id, dataset_and_table,entity_list,regex_list)
    file = 'bq_PII_status_report.html'
    count_dict=convert_to_html(status_list_bq_PII, file, app_root_path,service_name)
    return count_dict

def validate_cloud_sql(project_id, app_root_path):
    service_name = cloud_sql
    file_name = app_root_path + '/rule_yaml/' + 'cloud_sql_' + 'rules.yaml'
    sql_list = get_cloud_sql_list(project_id)
    status_list_sql = check_public_ip(sql_list, project_id, file_name)
    file = 'sql_status_report.html'
    count_dict = convert_to_html(status_list_sql, file, app_root_path, service_name)
    return count_dict


def validate_service_accounts(project_id, app_root_path):
    service_name = service_accounts
    filename = app_root_path + '/rule_yaml/' + 'service_' + 'rules.yaml'
    status_list_sa = check_rules_yaml_service_accounts(project_id, filename)
    file = 'service_account_status_report.html'
    count_dict = convert_to_html(status_list_sa, file, app_root_path, service_name)
    return count_dict


def validate_cloud_run(project_id, app_root_path):
    service_name = gcr
    file_name = app_root_path + '/rule_yaml/' + 'gcr_' + 'rules.yaml'
    service_list = get_gcr_list()
    entities = get_yaml_entities_public(file_name)
    status_list_gcr = check_iam_policy_gcr(service_list, entities)
    file = 'gcr_status_report.html'
    count_dict = convert_to_html(status_list_gcr, file, app_root_path, service_name)
    return count_dict


def validate_cloud_function(project_id, app_root_path):
    service_name = gcf
    file_name = app_root_path + '/rule_yaml/' + 'func_' + 'rules.yaml'
    function_list = get_function_name_list()
    entities = get_yaml_entities_public(file_name)
    status_list_gcf = check_iam_policy_gcf(function_list, entities)
    file = 'gcf_status_report.html'
    count_dict = convert_to_html(status_list_gcf, file, app_root_path, service_name)
    return count_dict


def validate_app_engine(project_id, app_root_path):
    service_name = app_engine
    urls = get_app_urls(project_id)
    status_list_app = check_app_engine(urls)
    file = 'app_engine_report.html'
    count_dict = convert_to_html(status_list_app, file, app_root_path, service_name)
    return count_dict


def validate_api_security(project_id, app_root_path):
    service_name = api_security
    file_name = app_root_path + '/rule_yaml/' + 'api_' + 'urls.yml'
    urls = (get_urls(file_name))
    status_list_api = check_api(urls)
    file = 'api_security_report.html'
    count_dict = convert_to_html(status_list_api, file, app_root_path, service_name)
    return count_dict

def validate_git(project_id,app_root_path):
    service_name = git_validate
    file_name = app_root_path +'/rule_yaml/' + 'git_' + 'rules.yaml'
    url = get_url(file_name)
    file ='git_validation_report.html'
    dict_list = get_secrets(url, app_root_path, file)
    count_dict = convert_to_html_git(dict_list, file, app_root_path, service_name)
    return count_dict


if __name__ == '__main__':
    run_security_tool()
