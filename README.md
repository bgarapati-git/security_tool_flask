# Security Assessment Tool
 
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

For example if you want to run the tool for only cloud Storage and Big Query

```commandline
    test.sh project_id "GCS" "BQ"
```


