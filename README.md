# Setup Instructions
It is a simple Python script that can recursively parse a website for text and images.

1. In order to run this application successfully, ensure you have a folder that can store images, and a folder that can store text. The python script can be modified to include a clause to create a folder path in case there is not one.
2. Ensure to install BeautifulSoup, requests,os,json and urllib via console.
3. Execute main.py
4. images, text, summary files are stored in the location of the python script folder.

# Steps to run app in cloud environment
1. AWS Lambda
2. import boto3

s3 = boto3.client("s3")
BUCKET_NAME = "your-s3-bucket"

def upload_to_s3(file_path, s3_key):
    with open(file_path, "rb") as f:
        s3.upload_fileobj(f, BUCKET_NAME, s3_key)

3. job can be triggered via cronjob.