import yaml
from src.lambda_functions.cr_ref_acst_rtu_process_lambda.main.util import LoggerFactory as _logger
import configparser
import os
""" 
    load yaml to fetch the application configurations & logger
    Paramters: None
    Raises: IOError: If there is an error like file not found etc.
            Exception: For all other errors.
"""

current_dir = os.getcwd()
configs = configparser.ConfigParser()

def load_err_file():
    global TECHNICAL_EXCEPTIONS
    try:
        with open(current_dir + "/src/lambda_functions/common/errorcodes.properties", "r") as error_file:
            configs.read_file(error_file)
            TECHNICAL_EXCEPTIONS = configs['TECHNICAL EXCEPTIONS']
            return configs
    except IOError as e :
        _logger.update_error_code('cr_ref_acst_rtu_500-0030')
        _logger.log_error(TECHNICAL_EXCEPTIONS['cr_ref_acst_rtu_500-0030'])
        _logger.log_error(f"The Exception is : {e}")

    except Exception as e:
        _logger.update_error_code('cr_ref_acst_rtu_500-0026')
        _logger.log_error(TECHNICAL_EXCEPTIONS['cr_ref_acst_rtu_500-0026']) 
        _logger.log_error(f"The Exception is : {e}")
    
    return None

def load_log_config_file():
    try:
        with open(current_dir + "/src/lambda_functions/cr_ref_acst_rtu_process_lambda/main/resources/logging.yaml", "rt") as logging_file:
            return yaml.safe_load(logging_file)
    except IOError as e:
        _logger.update_error_code('cr_ref_acst_rtu_500-0030')
        _logger.log_error(TECHNICAL_EXCEPTIONS['cr_ref_acst_rtu_500-0030'])
        _logger.log_error(f"The Exception is : {e}")
    except Exception as e:
        _logger.update_error_code('cr_ref_acst_rtu_500-0026')
        _logger.log_error(TECHNICAL_EXCEPTIONS['cr_ref_acst_rtu_500-0026']) 
        _logger.log_error(f"The Exception is : {e}")

    return None

