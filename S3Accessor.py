import boto3

__s3 = boto3.client('s3')
__BUCKET_NAME = "FOOBAR"


def save_file_to_s3(path, file_name):
    __s3.upload_file(path + file_name, __BUCKET_NAME, file_name)


def download_file_from_s3(path, file_name):
    __s3.download_file(__BUCKET_NAME, file_name, path + file_name)
