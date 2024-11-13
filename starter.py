from src.lambda_functions.cr_ref_acst_rtu_process_lambda.main.service import aircraft_subtype_int as asi
from src.lambda_functions.cr_ref_acst_rtu_process_lambda.main.util import LoggerFactory as _logger
from src.lambda_functions.cr_ref_acst_rtu_process_lambda.main.util.FileLoadUtility import load_err_file
import os

# Get Current Working Directory
current_dir = os.getcwd() 

# Load error config file
configs = load_err_file()


def main(xml_message, request_id):
    _logger.update_request_id(request_id)
    result = 'Success'
    try:
        xml_file = xml_message
        dict1 = asi.parse_xml_message(xml_file, request_id)
        if dict1 is None:
            result = 'Failure'
            return result
            # Handle the case where dict1 is None

        # Print the dictionary for debugging purposes
        print("Successfully Generated Dictionary: ", dict1)
        
        # Print action type and identifiers
        print("ActionType : ",dict1['aircraftSubtype']['@actionType'])

        # Determine action type
        actiontype = dict1['aircraftSubtype']['@actionType']
        
        # Perform actions based on action type
        if actiontype == "CREATE":
            aircraft_object = asi.initialize_aircraft_subtype_object_int(dict1, request_id)
            if aircraft_object is None:
                result = 'Failure'
                _logger.log_error("Failed to initialize aircraft object for CREATE action.")
            else:
                result = asi.action_type_create(aircraft_object, request_id)
                _logger.log_info(f"action CREATE : {result}")

        elif actiontype == "UPDATE": 
            if 'originalSubtypeIdentifier' in dict1['aircraftSubtype']['aircraftSubtypeIdentifier']:
                aircraft_object = asi.initialize_aircraft_subtype_object_int(dict1, request_id)
                original_aircraft_subtype_object = asi.initialize_original_aircraft_subtype_object_int(dict1, request_id)
                if aircraft_object is None or original_aircraft_subtype_object is None:
                    result = 'Failure'
                    _logger.log_error("Failed to initialize aircraft objects for UPDATE action.")
                else:
                    result = asi.action_type_update(aircraft_object, original_aircraft_subtype_object, request_id)
                    _logger.log_info(f"action UPDATE with New Keys: {result}")
            else:
                _logger.update_error_code('cr_ref_acst_rtu_300-0036')
                _logger.log_error(configs['VALIDATION EXCEPTIONS']['cr_ref_acst_rtu_300-0036'])
                result = 'Failure'

        elif actiontype == "DELETE":
            delete_aircraft_object = asi.delete_aircraft_subtype_object_int(dict1, request_id)
            if delete_aircraft_object is None:
                result = 'Failure'
                _logger.log_error("Failed to initialize delete aircraft object.")
            else:
                result = asi.action_type_delete(delete_aircraft_object, request_id)
                _logger.log_info(f"action DELETE : {result}")
            
        else:
            print(f"Unknown action type: {actiontype}. No action performed.")
            result = 'Failure'
            
        return result

    except Exception as e:
        _logger.update_error_code('cr_ref_acst_rtu_500-0030')
        _logger.log_error(configs['TECHNICAL_EXCEPTIONS']['cr_ref_acst_rtu_500-0030'])
        _logger.log_error(f"The Exception is {e}")

        result = 'Failure'
        return result