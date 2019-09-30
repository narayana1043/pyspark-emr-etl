import json
import boto3
from botocore.exceptions import ClientError


def S3_read(bucket, key):
    try:
        s3obj = boto3.client('s3',
                             aws_access_key_id='abcdedf',
                             aws_secret_access_key='abcdef'
                             ).get_object(Bucket=bucket, Key=key)
        contents = json.loads(s3obj['Body'].read().decode('utf-8'))
        return contents
    except ClientError as ex:
        if ex.response['Error']['Code'] == 'NoSuchKey':
            return None
        else:
            raise None
    except KeyError as ex:
        return None


def S3_write(bucket, key, object):
    boto3.client('s3', aws_access_key_id='abcdef',
                 aws_secret_access_key='abcdef'
                 ).put_object(Bucket=bucket, Key=key, Body=object)


def read_from_json(x):
    return json.loads(x)


def pick_from_json(x, key):
    return x[key]
