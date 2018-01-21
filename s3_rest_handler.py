from urllib2 import Request, urlopen, URLError #pip install urllib2
import xml.etree.ElementTree as ET #pip install ElementTree
import zulu  #pip install zulu
import folder_asset


#XML parsing tag targets:
# Tag in xml from S3_BUCKET_FIRST_LEVEL to look for folder names
COMMONPREFIXES_XML_TAG_TARGET = '{http://s3.amazonaws.com/doc/2006-03-01/}CommonPrefixes'
# after retrieving image urls, append to this string to make full image urls to be served by a flask server
CONTENTS_XML_TAG_TARGET = '{http://s3.amazonaws.com/doc/2006-03-01/}Contents'

#REST URLs to get gallery assets:
# rest url for folders, the first level is reserved for folders
S3_ASSET_BUCKET_FIRST_LEVEL = 'http://psyche-andromeda.s3.amazonaws.com/?delimiter=/'
# rest url to be used to get images urls from a folder
S3_ASSET_FOLDER_PREFIX_FILTERING_URL = 'http://psyche-andromeda.s3.amazonaws.com/?prefix='
#used to build the base urls
S3_ASSET_BASE_URL = 'http://psyche-andromeda.s3.amazonaws.com/'

#REST URLs to get gallery text:
S3_TEXT_BUCKET_FIRST_LEVEL = 'http://psyche-andromeda-text.s3.amazonaws.com/?delimiter=/'

S3_TEXT_FOLDER_PREFIX_FILTERING_URL = 'http://psyche-andromeda-text.s3.amazonaws.com/?prefix='

S3_TEXT_BASE_URL = 'http://psyche-andromeda-text.s3.amazonaws.com/'




def retrieve_assets():
    folder__to__assets__dict = {}
    folders_list = retrieve_folder_list(S3_ASSET_BUCKET_FIRST_LEVEL)  # get a list of every folder...
    for folder in folders_list:  # for every folder...
        folder_images_list = retrieve_folder_images_urls(folder)  # get a list of images names...
        folder__to__assets__dict[folder] = folder_images_list
    return folder__to__assets__dict

def retrieve_folder_list(url):
    folders_list = []
    first_level_request = Request(url)
    try:
        response = urlopen(first_level_request)
        first_level_response = response.read()
        root = ET.fromstring(first_level_response)
        for child in root:
            if child.tag == COMMONPREFIXES_XML_TAG_TARGET:
                folders_list.append(child[0].text[:-1])
        return folders_list

    except URLError, error:
        print 'Got an error code:', error


def retrieve_folder_images_urls(folder_str):
    asset_list = []
    text_list_links = []
    images_rest_url = S3_ASSET_FOLDER_PREFIX_FILTERING_URL + folder_str
    images_request = Request(images_rest_url)
    text_rest_url = S3_TEXT_FOLDER_PREFIX_FILTERING_URL + folder_str
    text_request = Request(text_rest_url)

    try:
        text_response = urlopen(text_request)
        text_folder_response = text_response.read()
        text_root = ET.fromstring(text_folder_response)
        skip_folder_flag = False
        for child in text_root:
            if child.tag == CONTENTS_XML_TAG_TARGET:
                if skip_folder_flag:
                    text_list_links.append(child[0].text)
                skip_folder_flag = True

        images_response = urlopen(images_request)
        images_folder_response = images_response.read()
        images_root = ET.fromstring(images_folder_response)
        skip_folder_flag = False #skip the first entry
        idx = -1 #due to skipping first loop am not using enumerate, this idx is used for looping through the text_list_links list
        for child in images_root:
            if child.tag == CONTENTS_XML_TAG_TARGET:
                if skip_folder_flag: #do not execute on first loop, second loop is when folder contents start
                    unix_timestamp = long(zulu.parse(child[1].text).timestamp())
                    txt = urlopen(S3_TEXT_BASE_URL + text_list_links[idx]).read()
                    asset = folder_asset.FolderAsset(S3_ASSET_BASE_URL + child[0].text, unix_timestamp, txt)
                    asset_list.append(asset)
                skip_folder_flag = True
                idx += 1
        return sorted(asset_list, key=lambda asset: asset.upload_time)

    except URLError, error:
        print 'Got an error code:', error