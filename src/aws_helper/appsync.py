import json
import os

import boto3
import requests
from dotenv import load_dotenv
from requests_aws_sign import AWSV4Sign
from aws_helper.secretManager import get_secret
load_dotenv()



def query(query, variables: dict):
    session = boto3.session.Session()
    credentials = session.get_credentials()
    
    region = os.environ.get("region")

    creds = json.loads(get_secret(secret_name=os.environ.get('secretName'), region_name=os.environ.get('region')))
    endpoint = creds['APPSYNC_ENDPOINT']
    x_api_key = creds['x-api-key']
    
    headers={"Content-Type": "application/json", 'x-api-key': x_api_key}
    payload = {"query": query, 'variables': variables}

    appsync_region = __parse_region_from_url(endpoint) or region
    auth=AWSV4Sign(credentials, appsync_region, 'appsync')
    try:
        response = requests.post(
            endpoint,
            auth=auth,
            json=payload,
            headers=headers
        ).json()
        if 'errors' in response:
            print('Error attempting to query AppSync')
            print(response['errors'])
        else:
            return response["data"]
    except Exception as exception:
        print('Error with Mutation')
        print(exception)

    return None

def __parse_region_from_url(url):
    """Parses the region from the appsync url so we call the correct region regardless of the session or the argument"""
    # Example URL: https://xxxxxxx.appsync-api.us-east-2.amazonaws.com/graphql
    split = url.split('.')
    if 2 < len(split):
        return split[2]
    return None
