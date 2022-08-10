import json
import os

from flask import Flask, request, send_file, render_template
from flask_cors import CORS, cross_origin

from src.run_security_tool import run_security_tool

app = Flask(__name__, static_folder='static')
CORS(app, support_credentials=True, expose_headers=["Content-Disposition"])


@app.route("/")
def render_html():
    report_list=get_files_list()
    print(f'type is {type(report_list)}')
    #report_list=json_obj['report']
    col_names=["REPORTS","PASS COUNT","FAIL COUNT","VIEW"]
    keys=["filename","pass_count","fail_count"]
    context = {
        "table_title": "Security Assessment Tool",
        "report_list": report_list,
        "col_names":col_names,
        "keys":keys
    }
    return render_template("summary.html", title="Security Assessment Tool",**context)

# @cross_origin(supports_credentials=True)
# @app.route("/getFileList", methods=["GET"])
# def get_files_list():
#     project_id = request.args.get('project_id')
#     # project_id='badri-29apr2022-scrumteam'
#     status_dict = run_security_tool(project_id, app.root_path)
#     if status_dict['status'] == "Success":
#         data = {'reports': status_dict['report_list']}
#         response = app.response_class(
#             response=json.dumps(data),
#             status=200,
#             mimetype='application/json'
#         )
#
#     else:
#         response = app.response_class(
#             response="Error Occurred while creating reports ",
#             status=404,
#             mimetype='application/json'
#         )
#     return response


def get_files_list():
    #project_id = request.args.get('project_id')
    project_id='badri-29apr2022-scrumteam'
    status_dict = run_security_tool(project_id, app.root_path)
    if status_dict['status'] == "Success":
        #data = {'reports': status_dict['report_list']}
        data=status_dict['report_list']
    else:
        data=[]
    return data

@app.route("/getReport", methods=["GET"])
def get_report_file():
    file_name = request.args.get('file')
    print(f'filename is {file_name}')
    path = os.path.join(app.root_path, "reports", file_name)
    return send_file(path)




if __name__ == "__main__":
    app.run(debug=True)
