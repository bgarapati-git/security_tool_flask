import os
import sys

from flask import Flask, request, send_file, render_template
from flask_cors import CORS

from src.run_security_tool import run_security_tool

app = Flask(__name__, static_url_path='/reports/static',
            static_folder='reports/static')

CORS(app, support_credentials=True, expose_headers=["Content-Disposition"])


@app.route("/")
def render_html():
    report_list = get_files_list()
    if len(report_list) > 0:
        col_names = ["SERVICE", "PASS COUNT", "FAIL COUNT", "GCS REPORT LOCATION", "VIEW"]
        keys = ["service", "pass_count", "fail_count"]
        context = {
            "table_title": "Security Assessment Tool",
            "report_list": report_list['report_list'],
            "col_names": col_names,
            "keys": keys,
            "gcs_url": report_list["gcs_url"]
        }
        return render_template("summary.html", title="Security Assessment Tool", **context)
    else:
        return f'Exception occurred while generating the reports'


def get_files_list():
    data = []
    project_id = app.config['project_id']
    user_name = app.config['user_name']
    print(f'project_id is {project_id}')
    status_dict = run_security_tool(project_id, app.root_path,user_name)
    # if status_dict['status'] == "Success":
    #     data = status_dict['report_list']
    # return data
    return status_dict


@app.route("/getReport", methods=["GET", "POST"])
def get_report_file():
    file_name = request.args.get('file')
    print(f'filename is {file_name}')
    path = os.path.join(app.root_path, "reports", file_name)
    return send_file(path)


if __name__ == "__main__":
    # print(f'command line arguments are {sys.argv}')
    if len(sys.argv) == 1:
        print('Please provide the project id and user name.Refer to Readme.md for help ')
    elif len(sys.argv) == 2:
        print('Please provide the user name.Refer to Readme.md for help ')
    else:
        # project = sys.argv[1]
        # user_name = sys.argv[2]
        app.config['project_id'] = sys.argv[1]
        app.config['user_name'] = sys.argv[2]
        app.run(debug=True)
