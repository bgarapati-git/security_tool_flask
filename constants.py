# Report Headers
service_name = 'Service'
rule_id = 'Rule Id'
bucket_name = 'Bucket Name'
gcr_service_name = "Cloud Run Service"
priority = 'Priority'
status_const = 'Status'
message = 'Message'
pass_status = "Pass"
fail_status = "Fail"
high_priority = "High"
low_priority = "Low"
medium_priority = "Medium"
data_set_name = 'Dataset Name'
sql_instance = 'Sql Instance'
cloud_sql_public = "Instance has Public IP"
iam_role = "IAM"
project_svc = 'Project'
svc_acnt = "Service Account"
role_svc = "Service Account has standard roles like Editor/Owner/Viewer"
default_svc = "Default Service Account is used"
function_name = "Function Name"
url = "URL"
Dataset_and_Table = 'Dataset and Table name'
repository = 'Repository'
branch = 'Branch Name'
commit_name = "Commit Name"
commit_hash = "Commit Hash"
path = "Path"
reason = "Reason"
entity = "Entity Name"

# Services
gcs = "Cloud Storage"
gcr = "Cloud Run"
big_query = 'BigQuery'
cloud_sql = "Cloud SQL"
gcf = "Cloud Function"
app_engine = "App Engine"
api_security = "API Security"
service_accounts = "Service Accounts"
bq_pii = 'BQ PII Validation'
git_validate = "Git Validation"
# Rule Ids

gcs_rule = "SML-GCS-1"
gcr_rule = "SML-GCR-1"
bq_rule_1 = 'SML_BQ_01'
bq_rule_2 = 'SML_BQ_02'
bq_rule_3 = 'SML_BQ_03'
bq_rule_4 = 'SML_BQ_04'
bq_rule_0 = 'SML_BQ_00'
bq_dp_rule = 'SML-DE-4'
cloud_sql_rule = 'SML_SQL_01'
svc_acnt_rule_1 = 'SML_SVC_01'
svc_acnt_rule_2 = 'SML_SVC_02'
svc_acnt_rule_3 = 'SML_SVC_03'
svc_acnt_rule_4 = 'SML_SVC_04'
gcf_rule = "SML-GCF-1"
ae_rule = "SML_AE_1"
api_rule = "SML-SEC-1"

# Messages

public_entity = "Publicly Accessible"
compliant = "Security Compliant"
public_bucket = "Public Bucket"
public_function = "Function is Public"
public_run = "Cloud Run is public"

iam_message = 'iamMember is public'
specialGroup = 'specialGroup is public'
groupByEmail = 'groupByEmail contains google groups'
userByEmail = 'userByEmail contains gmail'
url_response = "URL doesn't redirect to https"
user_managed = "User Managed Key is found"
api_unsecured = "API allows Empty/Invalid Tokens"
Failed_due_to_exposed = "Failed due to exposed entities: "
PII_not_exposed = "PII data is not exposed"

# Services for Input
cloud_storage = "1"
big_query_service = "2"
big_query_pii = "3"
sql = "4"
sa = "5"
cloud_run = "6"
cloud_functions = "7"
app_engine_service = "8"
api_security_check = "9"
git_validation = "10"
all_services = "all"