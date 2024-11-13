import logging
import logging.config
import os
import yaml

# # Fetch the logging config file by calling load_config_file method

current_dir = os.getcwd()
def get_logger_object():
    print(current_dir)
    with open(current_dir + "/src/lambda_functions/cr_ref_acst_rtu_process_lambda/main/resources/logging.yaml", 'r') as log_config_file:
        logging_properties = yaml.safe_load(log_config_file)        
        
    logging.config.dictConfig(logging_properties)
    return logging.getLogger()
    

# Define a dictionary to hold variables
patterns = {
    'request_id': 'AWS_Request_ID',
    'class_name': 'class_name',
    'unique_id': 'unique_id',
    'error_type': 'TE',
    'error_code': '5000-5001',
    'message': 'default message'
}
logger = get_logger_object()


# Function to update a pattern
def update_request_id(new_value):
    patterns['request_id'] = new_value


def update_log_level(new_value):
    patterns['log_level'] = new_value


def update_class_name(new_value):
    patterns['class_name'] = new_value


def update_unique_id(new_value):
    patterns['unique_id'] = new_value


def update_error_type(new_value):
    patterns['error_type'] = new_value


def update_error_code(new_value):
    patterns['error_code'] = new_value


def update_message(new_value):
    patterns['message'] = new_value


def log_info(message): 
    update_message(message)  
    logger.info(f"{patterns['request_id']} {'INFO'} {patterns['class_name']} {patterns['unique_id']} - {patterns['message']}")


def log_debug(message): 
    update_message(message)   
    logger.debug(f"{patterns['request_id']} {'DEBUG'} {patterns['class_name']} {patterns['unique_id']} - {patterns['message']}")


def log_error(message): 
    update_message(message)     
    logger.error(f"{patterns['request_id']} {'ERROR'} {patterns['class_name']} {patterns['unique_id']} {patterns['error_type']} {patterns['error_code']} - {patterns['message']}")
