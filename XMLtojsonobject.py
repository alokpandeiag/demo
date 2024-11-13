import json
import xmltodict
from src.lambda_functions.cr_ref_acst_rtu_process_lambda.main.util import LoggerFactory as _logger
from src.lambda_functions.cr_ref_acst_rtu_process_lambda.main.util.FileLoadUtility import load_err_file
configs = load_err_file()


"""  
Converts an XML message to a JSON object.
Parameters: xml_content(str): The xml message  to be converted.

Returns: Dict: The JSON object parsed from the XML message is successful.
                None if an error occurs during reading or prasing the file.
"""  
def json_object_from_xml(xml_content, request_id):
    _logger.update_request_id(request_id)
    _logger.update_class_name(__name__)
    try:
        print("this is the xml content", xml_content)
        json_text = json.dumps(xmltodict.parse(xml_content), default=lambda o: o.__dict__, indent=4)
        json_obj = json.loads(json_text)
        print("This is the json text ", json_obj)
        return json_obj  
      
    except Exception as e:  # CATCH TE TBL 'fail to parse' 
        _logger.update_error_code('cr_ref_acst_rtu_500-0004')
        _logger.log_error(configs['TECHNICAL EXCEPTIONS']['cr_ref_acst_rtu_500-0004'])     # Unable to parse XML message 
        _logger.log_error(f"The Exception is : {e}")
        return None
        

       
       