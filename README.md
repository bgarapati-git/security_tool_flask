# Security Assessment Tool
Pre Requisites:

Clone the repo as below for the first time 
```commandline
git clone https://github.com/bindu-haritha/security_tool_flask.git
```

If the repo already cloned, get the latest code as below :

cd to the directory where repo has been cloned and git pull 
```commandline
cd security_tool_flask
git pull origin
```

```Project specific rules configuration
Below yaml files needs to be updated based on the project requirements:
* api_urls.yml  -- To test API Security
* bq_PII_rule.yaml  -- To test PII data in BQ Tables
* git_rules.yaml   --To validate git repos for API keys 
* gcr_rules.yaml  --To give location of the cloud run
* report_gcs_bucket_config.yaml   -- To configure the bucket URL for storing the reports
'''

Run the shell script as below 
```
    . testframework.sh
```
It prompts for project_id (cloud project id), username(any name for now) and the necessary services that need to be run.

Service names that need to be passed to shell script prompt are listed below:

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

For example, if we need to run the tool only for cloud Storage and Big Query , Need to provide 1,2 when prompted.

If all services need to be validated provide **all** when prompted


