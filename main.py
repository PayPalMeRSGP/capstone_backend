from flask import Flask #pip install flask
from flask import jsonify
from urllib2 import Request, urlopen, URLError #pip install urllib2
import xml.etree.ElementTree as ET #pip install ElementTree
import zulu  #pip install zulu
import folder_asset
app = Flask(__name__)
app.json_encoder = folder_asset.FolderAssetJSONEncoder

# rest url for folders, the first level is meant to be folders only
S3_BUCKET_FIRST_LEVEL = 'http://psyche-andromeda.s3.amazonaws.com/?delimiter=/'
# Tag in xml from S3_BUCKET_FIRST_LEVEL to look for folder names
FOLDER_LEVEL_XML_TAG_TARGET = '{http://s3.amazonaws.com/doc/2006-03-01/}CommonPrefixes'
# rest url to be used to get images urls from a folder
S3_FOLDER_PREFIX_FILTERING_URL = 'http://psyche-andromeda.s3.amazonaws.com/?prefix='
# after retrieving image urls, append to this string to make full image urls to be served by a flask server
IMAGE_LEVEL_XML_TAG_TARGET = '{http://s3.amazonaws.com/doc/2006-03-01/}Contents'
#used to build the base urls
S3_BASE_URL = 'http://psyche-andromeda.s3.amazonaws.com/'


Folder_To_Its_Image_Urls_Dict = {}

@app.route('/')
def hello_world():
    main()
    return jsonify(Folder_To_Its_Image_Urls_Dict)


def main():
    folders_list = retrieve_folder_list() #get a list of every folder...
    for folder in folders_list: #for every folder...
        folder_images_list = retrieve_folder_images_urls(folder) #get a list of images names...
        Folder_To_Its_Image_Urls_Dict[folder] = folder_images_list
    


def retrieve_folder_list():
    folders_list = []
    first_level_request = Request(S3_BUCKET_FIRST_LEVEL)
    try:
        response = urlopen(first_level_request)
        first_level_response = response.read()
        root = ET.fromstring(first_level_response)
        for child in root:
            if child.tag == FOLDER_LEVEL_XML_TAG_TARGET:
                folders_list.append(child[0].text)
        return folders_list

    except URLError, error:
        print 'Got an error code:', error


def retrieve_folder_images_urls(folderStr):
    asset_list = []
    rest_url = S3_FOLDER_PREFIX_FILTERING_URL + folderStr
    request = Request(rest_url)
    try:
        response = urlopen(request)
        folder_response = response.read()
        root = ET.fromstring(folder_response)
        skip_folder_flag = False 
        for child in root:
            if child.tag == IMAGE_LEVEL_XML_TAG_TARGET:
                if skip_folder_flag:
                    unix_timestamp = long(zulu.parse(child[1].text).timestamp())
                    asset = folder_asset.FolderAsset(S3_BASE_URL + child[0].text, unix_timestamp)
                    asset_list.append(asset)
                    
                skip_folder_flag = True
        return asset_list

    except URLError, error:
        print 'Got an error code:', error


if __name__ == "__main__":
    main()
