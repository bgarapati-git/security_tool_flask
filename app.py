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
    remove_html_files()
    report_list = get_files_list()
    if len(report_list) > 0:
        col_names = ["SERVICE", "PASS COUNT", "FAIL COUNT", "VIEW"]
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
    project_id = app.config['project_id']
    user_name = app.config['user_name']
    services_list = app.config['services'].split(',')
    print(f'project_id is {project_id}')
    status_dict = run_security_tool(project_id, app.root_path, user_name, services_list)
    return status_dict


@app.route("/getReport", methods=["GET", "POST"])
def get_report_file():
    file_name = request.args.get('file')
    print(f'filename is {file_name}')
    path = os.path.join(app.root_path, "reports", file_name)
    return send_file(path)


def remove_html_files():
    # To check and remove the report html files generated previously before running the tool
    path = os.path.join(app.root_path, "reports")
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)) and (file.find('.html') != -1 or file.find('.csv') != -1):
            os.remove(os.path.join(path, file))
    return


if __name__ == "__main__":
    #print(f'command line arguments are {sys.argv}')
    app.config['project_id'] = sys.argv[1]
    app.config['user_name'] = sys.argv[2]
    app.config['services'] = sys.argv[3]
    app.run(debug=True)
