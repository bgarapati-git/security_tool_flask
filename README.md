# Security Assessment Tool
Pre Requisites:
Need to update the below yaml files as per the project needs
* api_urls.yml  -- To test API Security
* bq_PII_rule.yaml  -- To test PII data in BQ Tables
* report_gcs_bucket_config.yaml   -- To configure the bucket URL for storing the reports
* git_rules.yaml   --To validate git repos for API keys 


Run the shell script with project_id and the necessary services as inputs

Service names that need to be passed to shell script 
for corresponding cloud services are as below

* Cloud Storage - "GCS"
* Big Query - "BQ"
* Big Query PII - "BQ-PII"
* AppEngine - "APP"
* API- "API"
* Cloud SQL - "SQL"
* Cloud Functions - "GCF"
* Cloud Run - "GCR"
* IAM/Service Accounts -"IAM"
* Git repo Validation - "GIT"

For example if you want to run the tool for only cloud Storage and Big Query use as below

```commandline
    test.sh project_id "GCS" "BQ"
```


