import json

class FolderAsset():
    def __init__(self, upload_time, asset_url):
        self.upload_time = upload_time
        self.asset_url = asset_url
   
       
class FolderAssetJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, FolderAsset): 
            return {
            'upload_time' : obj.upload_time,
            'asset_url' : obj.asset_url
            }
        return json.JSONEncoder.default(self, obj)
