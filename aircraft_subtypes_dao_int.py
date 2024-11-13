from datetime import datetime
from zoneinfo import ZoneInfo
import traceback
from src.lambda_functions.cr_ref_acst_rtu_process_lambda.main.entity.aircraft_subtype_FleetMapping import FlightCrewAircraftFleetMapping
from src.lambda_functions.cr_ref_acst_rtu_process_lambda.main.dao.db_manager import Database
from src.lambda_functions.cr_ref_acst_rtu_process_lambda.main.util import LoggerFactory as _logger
from src.lambda_functions.cr_ref_acst_rtu_process_lambda.main.util.FileLoadUtility import load_err_file


configs = load_err_file()
BUSINESS_EXCEPTIONS = configs['BUSINESS EXCEPTIONS']
CREATED_AIRCRAFT_SUBTYPE = "Successfully created AircraftSubtype in Database "
new_ba_and_fleet = "FLIGHT_CREW_LICENSE_FLEET,FLIGHT_CREW_BASE_FLEET and BA_QUALIFIED_FLEET columns to be updated manually"


def create_aircraft_subtype(aircraft_subtype_object_int, request_id):
    _logger.update_class_name(__name__)
    _logger.update_request_id(request_id)
    
    print(aircraft_subtype_object_int, "This is aircraft object")
        
    session = Database.get_session(request_id)
    try:
        _logger.log_info(f"Attempting to create AircraftSubtype Object in Int DB: {aircraft_subtype_object_int}")
        
        if is_record_present(session, aircraft_subtype_object_int, request_id):
            existing_records = get_existing_record(session, aircraft_subtype_object_int, request_id)
            check_effective_to_datetime(session, aircraft_subtype_object_int, existing_records, request_id)
        else:
            _logger.update_error_code('cr_ref_acst_rtu_400-0093')
            _logger.log_error(BUSINESS_EXCEPTIONS['cr_ref_acst_rtu_400-0093'])     # new_ba_and_fleet
            session.add(aircraft_subtype_object_int)
            _logger.log_debug(CREATED_AIRCRAFT_SUBTYPE)
        session.flush()
        session.commit()

    except Exception as e:
        session.rollback()  # Rollback the transaction in case of an error
        _logger.update_error_code('cr_ref_acst_rtu_400-0089')
        _logger.log_error(BUSINESS_EXCEPTIONS['cr_ref_acst_rtu_400-0089'])     # An Error Occurred in create_aircraft_subtype
        _logger.log_error(f"The Exception is : {e}")
        traceback.print_exc()
        return None
    finally:
        session.close()
    return aircraft_subtype_object_int


def delete_aircraft_subtype(delete_aircraft_subtype_object_int, request_id):
    _logger.update_class_name(__name__)
    _logger.update_request_id(request_id)

    session = Database.get_session(request_id)
    try:
        _logger.log_info(f"Attempting to delete AircraftSubtype Object in Int DB: {delete_aircraft_subtype_object_int}")

        existing_records = get_existing_record(session, delete_aircraft_subtype_object_int, request_id)
        if existing_records:
            for record in existing_records:
                _logger.log_info("Update the EFFECTIVE_TO_DATETIME of Existing Record with New Record")
                new_valid_to = ensure_datetime(delete_aircraft_subtype_object_int.EFFECTIVE_TO_DATETIME)
                if isinstance(record.EFFECTIVE_TO_DATETIME, datetime):  # Correctly checking for datetime
                    record.EFFECTIVE_TO_DATETIME = new_valid_to
                    session.merge(record)
                else:
                    _logger.log_debug("The record.EFFECTIVE_TO_DATETIME is not of type datetime.")
        else:
            _logger.update_error_code('cr_ref_acst_rtu_400-0090')
            _logger.log_error(BUSINESS_EXCEPTIONS['cr_ref_acst_rtu_400-0090'])   # No matching record found for ActionType : Delete
        
        session.flush()
        session.commit()

    except Exception as e:
        session.rollback()  # Rollback the transaction in case of an error
        _logger.update_error_code('cr_ref_acst_rtu_400-0091')
        _logger.log_error(BUSINESS_EXCEPTIONS['cr_ref_acst_rtu_400-0091'])     # An Error Occurred in delete_aircraft_subtype
        _logger.log_error(f"The Exception is : {e}")
        traceback.print_exc()
        return None
    finally:
        session.close()
    return delete_aircraft_subtype_object_int


def update_aircraft_subtype(aircraft_subtype_object_int, original_aircraft_subtype_object_int, request_id):
    _logger.update_class_name(__name__)
    _logger.update_request_id(request_id) 

    session = Database.get_session(request_id)
    try:
        _logger.log_info(f"Attempting to update Original AircraftSubtype: {original_aircraft_subtype_object_int}")
        
        existing_records = get_existing_record(session, original_aircraft_subtype_object_int, request_id)
        
        if len(existing_records) >= 1 :  # If records are found
            handle_existing_records(session, aircraft_subtype_object_int, existing_records, request_id)           
        else:
            handle_no_existing_records(session, aircraft_subtype_object_int, request_id)

        session.flush()
        session.commit()

    except Exception as e:
        session.rollback()
        _logger.update_error_code('cr_ref_acst_rtu_400-0092')
        _logger.log_error(BUSINESS_EXCEPTIONS['cr_ref_acst_rtu_400-0092'])     # An Error Occurred in update_aircraft_subtype
        _logger.log_error(f"The Exception is : {e}")
        traceback.print_exc()
        return None
    finally:
        session.close()
    return aircraft_subtype_object_int


def get_existing_record(session, aircraft_subtype_object_int, request_id):
    """Retrieve existing record based on original identifiers."""
    _logger.update_request_id(request_id)
    try:
        _logger.log_debug("Comparing Primary Keys for Matching Records ")
        existing_records = session.query(FlightCrewAircraftFleetMapping).filter(
            FlightCrewAircraftFleetMapping.AIRCRAFT_OWNER == aircraft_subtype_object_int.AIRCRAFT_OWNER,
            FlightCrewAircraftFleetMapping.AIRCRAFT_SUBTYPE == aircraft_subtype_object_int.AIRCRAFT_SUBTYPE
        ).all()  # Returns a list of matching records
    except Exception  as e:
        _logger.update_error_code('cr_ref_acst_rtu_500-0003')
        _logger.log_error(configs['TECHNICAL EXCEPTIONS']['cr_ref_acst_rtu_500-0003'])
        _logger.log_debug(f"The Exception is : {e}")
        return None
    return existing_records


def is_record_present(session, aircraft_subtype_object_int, request_id):
    _logger.update_request_id(request_id)
    try:
        _logger.log_debug("Comparing Primary Keys for Matching Records Present Or Not ")
        record_exists = session.query(FlightCrewAircraftFleetMapping).filter(
            FlightCrewAircraftFleetMapping.AIRCRAFT_OWNER == aircraft_subtype_object_int.AIRCRAFT_OWNER,
            FlightCrewAircraftFleetMapping.AIRCRAFT_SUBTYPE == aircraft_subtype_object_int.AIRCRAFT_SUBTYPE
        ).first() is not None  # Returns a boolean indicating existence, is not None is used to make it return true or false
        _logger.log_debug(f"Result returned from is_record_present query: {record_exists}")
    except Exception as e:
        _logger.log_debug(f"No Matching Record Found: {e}")
        return False

    return record_exists

def handle_no_existing_records(session, aircraft_subtype_object_int, request_id):
    """Handle case when no existing records are found."""
    _logger.update_request_id(request_id) 
    _logger.log_info("No match found for ActionType='Update'.")
    matching_records = get_existing_record(session, aircraft_subtype_object_int, request_id)
    if matching_records:
        check_effective_to_datetime(session, aircraft_subtype_object_int, matching_records, request_id)
    else:
        _logger.update_error_code('cr_ref_acst_rtu_400-0093')
        _logger.log_error(BUSINESS_EXCEPTIONS['cr_ref_acst_rtu_400-0093'])
        session.add(aircraft_subtype_object_int)
        _logger.log_debug(CREATED_AIRCRAFT_SUBTYPE)
    session.flush()
    session.commit()


def handle_existing_records(session, aircraft_subtype_object_int, existing_records, request_id):
    """Handle case when existing records are found."""
    _logger.update_request_id(request_id) 
    matching_records = get_existing_record(session, aircraft_subtype_object_int, request_id)
    if matching_records:
        check_effective_to_datetime(session, aircraft_subtype_object_int, matching_records, request_id)
    else:
        check_effective_to_datetime(session, aircraft_subtype_object_int, existing_records, request_id)


def check_effective_to_datetime(session, aircraft_subtype_object_int, matching_records, request_id):
    _logger.update_request_id(request_id) 
    for record in matching_records:
        effective_to_datetime = ensure_datetime(record.EFFECTIVE_TO_DATETIME)
        print("This is the datetime :",effective_to_datetime )
        if effective_to_datetime < datetime.now():
            _logger.update_error_code('cr_ref_acst_rtu_400-0093')
            _logger.log_error(BUSINESS_EXCEPTIONS['cr_ref_acst_rtu_400-0093']) 
            session.add(aircraft_subtype_object_int)
            _logger.log_debug(CREATED_AIRCRAFT_SUBTYPE)
        else:
            # Override the existing row, excluding some specific conditions
            update_existing_record(session, record, aircraft_subtype_object_int, request_id)
            session.merge(record)
            _logger.log_info("Successfully updated AircraftSubtype in Database ")
    session.flush()
    session.commit()


def update_existing_record(session, existing_record, new_record, request_id):
    """Update the existing record with new values."""
    _logger.update_request_id(request_id)
    _logger.log_debug("Updating existing record.")
    existing_record.AIRCRAFT_OWNER = new_record.AIRCRAFT_OWNER
    existing_record.AIRCRAFT_SUBTYPE = new_record.AIRCRAFT_SUBTYPE
    existing_record.AIRCRAFT_TYPE_IATA = new_record.AIRCRAFT_TYPE_IATA
    existing_record.AIRCRAFT_TYPE_ICAO = new_record.AIRCRAFT_TYPE_ICAO
    existing_record.AIRCRAFT_SUBTYPE_ICAO = new_record.AIRCRAFT_SUBTYPE_ICAO
    existing_record.FLEET_CODE_FICO_CONSOLIDATED = new_record.FLEET_CODE_FICO_CONSOLIDATED

    new_valid_from = ensure_datetime(new_record.EFFECTIVE_FROM_DATETIME)
    new_valid_to = ensure_datetime(new_record.EFFECTIVE_TO_DATETIME)
    existing_record.EFFECTIVE_FROM_DATETIME = new_valid_from
    existing_record.EFFECTIVE_TO_DATETIME = new_valid_to
    session.merge(existing_record)


def ensure_datetime(date_time_str):
    if isinstance(date_time_str, str):
        try:
            # Convert string to naive datetime (UTC)
            return datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%SZ')
        except ValueError as ve:
            _logger.log_debug(f"ValueError: {ve} - Problem Parsing date string: {date_time_str}")
            return None  # Return None to indicate failure

    elif isinstance(date_time_str, datetime):
        # Convert aware datetime to naive by assuming UTC
        if date_time_str.tzinfo is not None:
            return date_time_str.astimezone(ZoneInfo("UTC")).replace(tzinfo=None)
        return date_time_str  # already naive

    else:
        _logger.log_debug(f"TypeError: Expected a string or datetime object, got {type(date_time_str)}")
        return None
