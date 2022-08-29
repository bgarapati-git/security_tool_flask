# Security Assessment Tool
Pre Requisites:
Need to update the below yaml files as per the project needs
* api_urls.yml  -- To test API Security
* bq_PII_rule.yaml  -- To test PII data in BQ Tables
* report_gcs_bucket_config.yaml   -- To configure the bucket URL for storing the reports
* git_rules.yaml   --To validate git repos for API keys 


Run the shell script with project_id username and the necessary services as inputs

Service names that need to be passed to shell script 
for corresponding cloud services are as below

* [1] Cloud Storage
* [2] BigQuery
* [3] BigQuery_PII
* [4] Cloud SQL
* [5] Service Accounts
* [6] Cloud Run
* [7] Cloud Function
* [8] App Engine
* [9] API Security
* [10] Git Validation
* [all] Run all services

For example if you want to run the tool only for cloud Storage and Big Query , Need to provide 1,2 when prompted


