#Report Headers
service_name = 'Service'
rule_id = 'Rule Id'
bucket_name = 'Bucket Name'
gcr_service_name="Cloud Run Service"
priority = 'Priority'
status_const = 'Status'
message = 'Message'
pass_status="Pass"
fail_status="Fail"
high_priority="High"
low_priority="Low"
medium_priority="Medium"
data_set_name='Dataset Name'
sql_instance='Sql Instance'
cloud_sql_public="Instance has Public IP"
iam_role="IAM"
project_svc='Project'
svc_acnt="Service Account"
role_svc="Service Account has roles/editor or roles/owner privilege"
default_svc="Default Service Account is used"
function_name="Function Name"
url="URL"
Dataset='Dataset'
Table="Table"

#Services
gcs="Cloud Storage"
gcr="Cloud Run"
big_query='BigQuery'
cloud_sql="Cloud SQL"
gcf="Cloud Function"
app_engine= "App Engine"
api_security= "API Security"

#Rule Ids

gcs_rule="SML-GCS-1"
gcr_rule="SML-GCR-1"
bq_rule_1='SML_BQ_01'
bq_rule_2='SML_BQ_02'
bq_rule_3='SML_BQ_03'
bq_rule_4='SML_BQ_04'
bq_rule_0='SML_BQ_00'
bq_dp_rule='SML-DE-4'
cloud_sql_rule='SML_SQL_01'
svc_acnt_rule_1='SML_SVC_01'
svc_acnt_rule_2='SML_SVC_02'
svc_acnt_rule_3='SML_SVC_03'
svc_acnt_rule_4='SML_SVC_04'
gcf_rule="SML-GCF-1"
ae_rule="SML_AE_1"
api_rule="SML-SEC-1"


#Messages

public_entity="Publicly Accessible"
compliant="Security Compliant"
public_bucket="Public Bucket"

iam_message = 'iamMember is public'
specialGroup = 'specialGroup is public'
groupByEmail = 'groupByEmail contains google groups'
userByEmail = 'userByEmail contains gmail'
url_response= "Url is not redirected"
user_managed="User Managed Key is found"
Failed_due_to_exposed="Failed due to exposed entities: "
PII_not_exposed="PII data is not exposed"