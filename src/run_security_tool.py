from src.bq_validation import get_bq_dataset_list, check_rules_yaml
from src.cloud_sql_validation import check_public_ip, get_cloud_sql_list
from src.gcs_validation import check_iam_policy
from src.service_acc_validation import check_rules_yaml_service_accounts
from src.common_functions import get_list, get_yaml_entities_public, read_project_json, convert_to_html
from src.gcr_validation import check_iam_policy_gcr
from src.gcf_validation import check_iam_policy_gcf
from src.app_engine_validation import get_app_urls, check_app_engine

# def run_security_tool():
#     method_name = run_security_tool.__name__
#     status = ''
#     try:
#         project_ids = read_project_json()
#         for project_id in project_ids:
#             validate_gcs_buckets(project_id)
#             validate_bq(project_id)
#             validate_cloud_sql(project_id)
#             validate_service_accounts(project_id)
#             validate_cloud_run(project_id)
#             validate_cloud_function(project_id)
#             status = "Success"
#     except Exception as e:
#         print(f'Exception occurred in {method_name} method exception is{e}')
#         status = "Fail"
#     return status


def run_security_tool(project_id, app_root_path):
    method_name = run_security_tool.__name__
    try:
        validate_gcs_buckets(project_id, app_root_path)
        validate_bq(project_id, app_root_path)
        validate_cloud_sql(project_id, app_root_path)
        validate_service_accounts(project_id, app_root_path)
        validate_cloud_run(project_id, app_root_path)
        validate_cloud_function(project_id, app_root_path)
        validate_app_engine(project_id,app_root_path)
        status = "Success"
    except Exception as e:
        print(f'Exception occurred in {method_name} method exception is{e}')
        status = "Fail"
    return status


def validate_gcs_buckets(project_id, app_root_path):
    # file_name = '../rule_yaml/' + project_id + '_gcs_' + 'rules.yaml'
    file_name = app_root_path + '/rule_yaml/' + project_id + '_gcs_' + 'rules.yaml'
    command = 'gsutil ls -p' + ' ' + project_id
    bucket_list = get_list(project_id, command)
    yaml_entities = get_yaml_entities_public(file_name)
    status_list_gcs = check_iam_policy(bucket_list, yaml_entities)
    file = 'gcs_status_report.html'
    convert_to_html(status_list_gcs, file, app_root_path)


def validate_bq(project_id, app_root_path):
    filename = app_root_path + '/rule_yaml/' + project_id + '_bq_' + 'rules.yaml'
    dataset_list = get_bq_dataset_list(project_id)
    status_list_bq = check_rules_yaml(project_id, dataset_list, filename)
    file = 'bq_status_report.html'
    convert_to_html(status_list_bq, file, app_root_path)


def validate_cloud_sql(project_id, app_root_path):
    file_name = app_root_path + '/rule_yaml/' + project_id + '_cloud_sql_' + 'rules.yaml'
    sql_list = get_cloud_sql_list(project_id)
    status_list_sql = check_public_ip(sql_list, project_id, file_name)
    file = 'sql_status_report.html'
    convert_to_html(status_list_sql, file, app_root_path)


def validate_service_accounts(project_id, app_root_path):
    filename = app_root_path + '/rule_yaml/' + project_id + '_service_' + 'rules.yaml'
    status_list_sa = check_rules_yaml_service_accounts(project_id, filename)
    file = 'service_account_status_report.html'
    convert_to_html(status_list_sa, file, app_root_path)


def validate_cloud_run(project_id, app_root_path):
    file_name = app_root_path + '/rule_yaml/' + project_id + '_gcr_' + 'rules.yaml'
    command_service = "gcloud run services list --format=" + "'value(name)'"
    service_list = get_list(project_id, command_service)
    entities = get_yaml_entities_public(file_name)
    status_list_gcr = check_iam_policy_gcr(service_list, entities)
    file = 'gcr_status_report.html'
    convert_to_html(status_list_gcr, file, app_root_path)


def validate_cloud_function(project_id, app_root_path):
    file_name = app_root_path + '/rule_yaml/' + project_id + '_func_' + 'rules.yaml'
    command_function = "gcloud functions list --format=" + "'value(name)'"
    function_list = get_list(project_id, command_function)
    entities = get_yaml_entities_public(file_name)
    status_list_gcf = check_iam_policy_gcf(function_list, entities)
    file = 'gcf_status_report.html'
    convert_to_html(status_list_gcf, file, app_root_path)

def validate_app_engine(project_id,app_root_path):
    urls=get_app_urls(project_id)
    status_list_app=check_app_engine(urls)
    file = 'app_engine_report.html'
    convert_to_html(status_list_app,file,app_root_path)


if __name__ == '__main__':
    run_security_tool()
