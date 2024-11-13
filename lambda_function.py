import sys
import os
import json
import boto3
from src.lambda_functions.cr_ref_acst_rtu_process_lambda.main.starter import main as start_main # Import the main function from starter.py
from src.lambda_functions.cr_ref_acst_rtu_process_lambda.main.util import LoggerFactory as _logger
 
# Initialize the SQS client
sqs_client = boto3.client('sqs')
 
def lambda_handler(event, context):
    request_id = context.aws_request_id   
    _logger.update_request_id(request_id)
    
    try:
        # Log the event to verify Lambda invocation
        _logger.log_info("Lambda function is invoked.")
        _logger.log_info(f"Received event: {event}")
 
        output_queue_url = os.environ.get('SQS_OUTPUT_QUEUE')
        dlq_queue_url = os.environ.get('SQS_DLQ_QUEUE')
 
        # Check if there are records in the event
        if "Records" in event and len(event["Records"]) > 0:
            for record in event["Records"]:
                message_body = record['body']
                print(f"Message ID: {record['messageId']}")
                print(f"Message Body: {message_body}")
 
                try:
                    # Call your main function with the JSON object
                    process_message = start_main(message_body, request_id)
                    # passed request id to main function
                    
                    if process_message == 'Success':
                        
                        # Send the SQS message to the output queue
                        response = sqs_client.send_message(
                            QueueUrl=output_queue_url,
                            MessageBody=message_body  # Passing the message from input to output
                        )
                        # Log the response from sending the message
                        _logger.log_info(f"Message sent to output queue. SQS Response: {response}")
                        _logger.log_info(f"Message Body : {message_body}")
                    
                    else:
                        response = sqs_client.send_message(
                            QueueUrl=dlq_queue_url,
                            MessageBody=message_body  # Passing the message from input to dlq
                        )
                        _logger.log_info("Error Occured While Processing the input message & Updating the Database. Message sent to DLQ SQS ")
                        

                except Exception as e:
                    print(f"The Exception from the lambda function is: {str(e)}")
                    return {
                        'statusCode': 400,
                        'body': f"The Exception from the lambda function is: {str(e)}"
                    }
 
        return {
            'statusCode': 200,
            'body': 'Starter main function executed and messages sent to output queue successfully'
        }
 
    except Exception as e:
        # Log error details
        print(f"An error occurred: {str(e)}")
        return {
            'statusCode': 500,
            'body': f"An error occurred: {str(e)}"
        }
