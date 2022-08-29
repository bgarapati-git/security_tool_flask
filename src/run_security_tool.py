import calendar
import datetime
import os
import subprocess
import time

from constants import gcs, big_query, cloud_sql, gcr, gcf, app_engine, api_security, service_accounts, bq_pii, \
    git_validate, cloud_storage, big_query_service, big_query_pii, sql, sa, cloud_run, cloud_functions, \
    app_engine_service, api_security_check,git_validation, all_services
from src.api_security_validation import get_urls, check_api
from src.app_engine_validation import get_app_urls, check_app_engine
from src.bq_PII_validation import get_yaml, bq_PII_data_validation
from src.bq_validation import get_bq_dataset_list, check_rules_yaml
from src.cloud_sql_validation import check_public_ip, get_cloud_sql_list
from src.common_functions import convert_to_html_git, get_yaml_entities_public_gcr
from src.common_functions import get_list, get_yaml_entities_public, convert_to_html, get_yaml_data
from src.gcf_validation import check_iam_policy_gcf, get_function_name_list
from src.gcr_validation import check_iam_policy_gcr, get_gcr_list
from src.gcs_validation import check_iam_policy
from src.service_acc_validation import check_rules_yaml_service_accounts
from src.trufflehog_validation import get_url, get_secrets


def run_security_tool(project_id, app_root_path, user_name,services_list):
    method_name = run_security_tool.__name__
    count_dict = []
    try:
        if cloud_storage in services_list or all_services in services_list:
            count_gcs = validate_gcs_buckets(project_id, app_root_path)
            count_dict.append(count_gcs)
        if big_query_service in services_list or all_services in services_list:
            count_bq = validate_bq(project_id, app_root_path)
            count_dict.append(count_bq)
        if big_query_pii in services_list or all_services in services_list:
            count_bq_pii = validate_bq_PII(project_id, app_root_path)
            count_dict.append(count_bq_pii)
        if sql in services_list or all_services in services_list:
            count_sql = validate_cloud_sql(project_id, app_root_path)
            count_dict.append(count_sql)
        if sa in services_list or all_services in services_list:
            count_sa = validate_service_accounts(project_id, app_root_path)
            count_dict.append(count_sa)
        if cloud_run in services_list or all_services in services_list:
            count_gcr = validate_cloud_run(project_id, app_root_path)
            count_dict.append(count_gcr)
        if cloud_functions in services_list or all_services in services_list:
            count_gcf = validate_cloud_function(project_id, app_root_path)
            count_dict.append(count_gcf)
        if app_engine_service in services_list or all_services in services_list:
            count_app = validate_app_engine(project_id, app_root_path)
            count_dict.append(count_app)
        if api_security_check in services_list or all_services in services_list:
            count_api = validate_api_security(project_id, app_root_path)
            count_dict.append(count_api)
        if git_validation in services_list or all_services in services_list:
            count_git = validate_git(project_id, app_root_path)
            count_dict.append(count_git)

        # Check whether csv is uploaded and delete the csv
        csv_path = os.path.join(app_root_path, 'reports', 'security_status_template.csv')
        path = os.path.join(app_root_path, "reports")
        if len(count_dict) > 0:
            bucket_url = upload_to_gcs(project_id, app_root_path, user_name)
            if os.path.exists(csv_path) and bucket_url is not None:
                os.remove(csv_path)
        status = "Success"
        status_dict = {"status": status, "report_list": count_dict, "gcs_url": bucket_url}
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
    # file_name = '../rule_yaml/' + 'bq_PII_rule.yaml'
    file_name = app_root_path + '/rule_yaml/' + 'bq_PII_rule.yaml'
    dataset_and_table, entity_list, regex_list = get_yaml(file_name)
    status_list_bq_PII = bq_PII_data_validation(project_id, dataset_and_table, entity_list, regex_list)
    file = 'bq_PII_status_report.html'
    count_dict = convert_to_html(status_list_bq_PII, file, app_root_path, service_name)
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
    entities = get_yaml_entities_public_gcr(file_name)
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
    urls,methods= (get_urls(file_name))
    status_list_api = check_api(urls,methods)
    file = 'api_security_report.html'
    count_dict = convert_to_html(status_list_api, file, app_root_path, service_name)
    return count_dict


def validate_git(project_id, app_root_path):
    service_name = git_validate
    file_name = app_root_path + '/rule_yaml/' + 'git_' + 'rules.yaml'
    url = get_url(file_name)
    file = 'git_validation_report.html'
    dict_list = get_secrets(url, app_root_path, file)
    count_dict = convert_to_html_git(dict_list, file, app_root_path, service_name)
    return count_dict


def upload_to_gcs(project_id, app_root_path, user_name):
    file_name = app_root_path + '/rule_yaml/' + 'report_gcs_bucket_config.yaml'
    yaml_data = get_yaml_data(file_name)
    gcs_bucket = yaml_data['gcs'][0]['gcs_report_url']
    print(f'gcs_bucket is {gcs_bucket}')
    upload_folder = os.path.join(app_root_path, 'reports')
    timestamp = calendar.timegm(time.gmtime())
    time_iso = datetime.datetime.fromtimestamp(timestamp).isoformat()
    suffix = project_id + '/' + user_name + '_' + str(time_iso) + '/' + 'reports'
    command = "gsutil -m cp -r " + upload_folder + ' ' + gcs_bucket + suffix
    out_put = subprocess.getoutput(command)
    print(f'out_put is {out_put}')
    return gcs_bucket + suffix
