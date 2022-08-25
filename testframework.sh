#!/bin/bash
echo Enter project ID:
read projectID
#echo $projectID
echo Enter Username:
read Username
#echo $Username
echo "Choose the Services to Test:
      [1] Cloud Storage
      [2] BigQuery
      [3] BigQuery_PII
      [4] Cloud SQL
      [5] Service Accounts
      [6] Cloud Run
      [7] Cloud Function
      [8] App Engine
      [9] API Security
      [10] Git Validation

      format: 2,4,6"
read Services
#echo $Services

cd security_tool_flask
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py $projectID $Username $Services
