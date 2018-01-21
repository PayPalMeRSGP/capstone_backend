from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
from botocore.exceptions import ClientError

access_key = "AKIAJC2BVGVB7DKERUZQ"
secret_key = "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"

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)



def getTimelineJSON():
    dynamodb = boto3.resource("dynamodb", aws_access_key_id=access_key, aws_secret_access_key=secret_key,
                              region_name='us-east-1')
    table = dynamodb.Table('CapstoneTimelineDB')

    try:
        response = table.scan()
        print(type(response))
    except ClientError as e:
        print("error")
        print(e.response['Error']['Message'])
    else:
        events = response["Items"][0]["Events"]
        return json.dumps(events, indent=4, cls=DecimalEncoder)