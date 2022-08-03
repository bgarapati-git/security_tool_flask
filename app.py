import json
import os

from flask import Flask, send_from_directory, request
from flask_cors import CORS, cross_origin

from src.run_security_tool import run_security_tool

app = Flask(__name__, static_folder='static')
CORS(app, support_credentials=True)


@cross_origin(supports_credentials=True)
@app.route("/getFileList", methods=["GET"])
def get_files_list():
    project_id = request.args.get('project_id')
    # project_id='badri-29apr2022-scrumteam'
    status = run_security_tool(project_id, app.root_path)
    if status == "Success":
        file_list = [file for file in os.listdir('reports')]
        data = {'reports': file_list}
        response = app.response_class(
            response=json.dumps(data),
            status=200,
            mimetype='application/json'
        )

    else:
        response = app.response_class(
            response="Error Occurred while creating reports ",
            status=404,
            mimetype='application/json'
        )
    #response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route("/getReport", methods=["GET"])
def get_report_file():
    file_name = request.args.get('file')
    print(f'filename is {file_name}')
    return send_from_directory('reports', path="reports", filename=file_name)


if __name__ == "__main__":
    app.run(debug=True)
