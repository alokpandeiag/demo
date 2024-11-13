import requests
import jwt
from cryptography.hazmat.primitives import serialization
import json
import configparser


def lambda_handler(event, context):
    print("Client token: " + event['authorizationToken'])
    print("Method ARN: " + event['methodArn'])

    principal_id = 'user:test'

    try:
       decode_token=decode(event['authorizationToken'])
     #  print('this is start point')
      # print(decode_token)  
       
       try:
           roles=retrieve_property('126d7c24-710c-4873-b8a6-78806ea1bf3e')
       except Exception as e: 
           print(e)
       role_list_token=list(decode_token['roles'])
      ##print(role_list_token[0])
       role_list_property=list(roles.split(','))
       print(role_list_property)

       if role_list_token[0] in role_list_property:
        principal_id = 'test:Success'
        policy_document = {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Action': 'execute-api:Invoke',
                    'Effect': 'Allow',
                    'Resource': event['methodArn']
                }
            ]
        }
       else:
        principal_id = 'Role not Matched'
        policy_document = {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Action': 'execute-api:Invoke',
                    'Effect': 'Deny',
                    'Resource': event['methodArn']
                }
            ]
        }

    
    except Exception as e:
        print(e)
        principal_id = 'unathorization'
        policy_document = {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Action': 'execute-api:Invoke',
                    'Effect': 'Deny',
                    'Resource': event['methodArn']
                }
            ]
        }

    return {
        'principal_id': principal_id,
        'policy_document': policy_document
    }

def retrieve_property(app_id):
   # Create a ConfigParser object
    print('this is a break point')
    config = configparser.ConfigParser()
    config.read('./src/lambda_functions/fc_rst_op_web_crewlink_auth_lambda/constant.properties')
    api_value = config.get('app_id : ROLES', app_id)


    print(f"API value: {api_value}")

    return api_value

def decode(token):
    #response1 = requests.get("https://login.microsoftonline.com/f27ea5d5-33a2-4431-8bc0-08c7232cd036/discovery/keys")
    response1 = requests.get("https://login.windows.net/common/discovery/keys")
    keys = response1.json()['keys']
    print(f"keys:{keys}")    
    token_headers = jwt.get_unverified_header(token)
    
    token_alg = token_headers['alg']
    token_kid = token_headers['kid']
    print(f"token_kid:{token_kid}")
    public_key = None
    for key in keys:
        if key['kid'] == token_kid:
            public_key = key 
    
    try:    
        rsa_pem_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(public_key))
    except Exception as e: 
           print(e)
    print(f"rsa_pem_key:{rsa_pem_key}")       
    rsa_pem_key_bytes = rsa_pem_key.public_bytes(
        encoding=serialization.Encoding.PEM, 
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ) 

    decode = jwt.decode(
        token,
        key=rsa_pem_key_bytes,
        algorithms=["RS256"],
        audience="api://126d7c24-710c-4873-b8a6-78806ea1bf3e"
    )


    return decode

