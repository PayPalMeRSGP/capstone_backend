#NEEDS PYTHON2 NOT 3
from flask import Flask #pip install flask
from flask import jsonify
from flask import request
import folder_asset
import s3_rest_handler
import platform

app = Flask(__name__)
app.json_encoder = folder_asset.FolderAssetJSONEncoder


@app.route('/')
def base_page_handler():
    output = s3_rest_handler.retrieve_assets()
    return jsonify(output)

@app.route('/filter')
def unix_timestamp_get_request_handler():
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

def main():
    if platform.system() == "Linux":
        app.run(host='0.0.0.0', port=5000, debug=True)
        # If the system is a windows /!\ Change  /!\ the   /!\ Port
    elif platform.system() == "Windows":
        app.run(host='0.0.0.0', port=50000, debug=True)

if __name__ == "__main__":
    main()
