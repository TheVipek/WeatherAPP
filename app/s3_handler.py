import os,boto3

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.environ.get('aws_access_key_id'),
    aws_secret_access_key=os.environ.get('aws_secret_access_key'),
    region_name =os.environ.get('region')
)

#default s3 bucket from environment
def aws_get_all(bucket=os.environ.get('s3_bucket')):
    if bucket!=None:
        items = s3.list_objects(Bucket=bucket)
        return items

#default s3 bucket from environment 
def aws_upload_file(bucket=os.environ.get('s3_bucket'),object_name=None,content=None):
    if bucket and object_name!=None and content!=None:
        s3.put_object(
            Bucket=bucket,
            Key=object_name,
            Body=content
        )
def aws_get_file(bucket,object_name):
    return s3.get_object(Bucket=bucket,
                        Key=object_name
                        )
