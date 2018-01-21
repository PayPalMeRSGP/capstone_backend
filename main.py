#NEEDS PYTHON2 NOT 3
from flask import Flask #pip install flask
from flask import jsonify
from flask import request
import folder_asset
import s3_rest_handler
import platform
import dyanmodb_handler

app = Flask(__name__)
app.json_encoder = folder_asset.FolderAssetJSONEncoder

@app.route('/')
def base_page_handler():
    return "api:" \
           "\n" \
           "GET [base_url]/everything\n" \
           "returns every asset in s3" \
           "\n\n" \
           "GET [base_url]/filter?=[unix_timestamp]\n" \
           "returns every asset uploaded after [unix_timestamp] argument" \
           "\n\n" \
           "GET [base_url]/timeline \n" \
           "returns the mission timeline"

@app.route('/everything')
def everything_page_handler():
    output = s3_rest_handler.retrieve_assets()
    return jsonify(output)

@app.route('/filter')
def filter_page_handler():
    s3_data = s3_rest_handler.retrieve_assets()
    s3_filtered_data = {}
    last_update_timestamp = request.args.get('last_update', default=0, type=long)
    for folder in s3_data:
        asset_list = s3_data[folder]
        for idx, asset in enumerate(asset_list):
            if asset.upload_time > last_update_timestamp:
                s3_filtered_data[folder] = asset_list[idx:]
                break
    return jsonify(s3_filtered_data)

@app.route('/timeline')
def timeline():
    return dyanmodb_handler.getTimelineJSON()

def main():
    if platform.system() == "Linux":
        app.run(host='0.0.0.0', port=5000, debug=True)
        # If the system is a windows /!\ Change  /!\ the   /!\ Port
    elif platform.system() == "Windows":
        app.run(host='0.0.0.0', port=50000, debug=True)

if __name__ == "__main__":
    main()
