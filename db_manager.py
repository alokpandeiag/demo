
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from threading import Lock
import psycopg
import boto3
import json
import os

from src.lambda_functions.cr_ref_acst_rtu_process_lambda.main.util import LoggerFactory as _logger
from src.lambda_functions.cr_ref_acst_rtu_process_lambda.main.util.FileLoadUtility import load_err_file

_logger.update_class_name(__name__)

configs = load_err_file()

class Database:
    _connection = None
    _engine = None
    _engine_lock = Lock()

    @staticmethod
    def get_db_credentials(secret_name, request_id):
        """Retrieve database credentials from AWS Secrets Manager."""
        _logger.update_request_id(request_id)
        secrets_manager_client = boto3.client('secretsmanager', region_name=os.environ.get('REGION'))
        try:
            response = secrets_manager_client.get_secret_value(SecretId=secret_name)
            secret_string = response['SecretString']
            db_credentials = json.loads(secret_string)
            return db_credentials
        except Exception as e:
            _logger.update_error_code('cr_ref_acst_rtu_500-0024')
            _logger.log_error(configs['TECHNICAL EXCEPTIONS']['cr_ref_acst_rtu_500-0024'])  # Failed to retrieve RDS secret
            _logger.log_error(f"The Exception is : {e}")
            raise

    @staticmethod
    def get_engine(request_id):
        """Create and return a singleton SQLAlchemy engine."""
        _logger.update_request_id(request_id)
        with Database._engine_lock:
            if Database._engine is None:
                db_credentials = Database.get_db_credentials(os.environ.get('RDS_SECRET_NAME'), request_id)
                try:
                    Database._engine = create_engine(
                        f"postgresql+psycopg://{db_credentials['username']}:{db_credentials['password']}@"
                        f"{db_credentials['host']}:{db_credentials['port']}/{db_credentials['dbname']}",
                        pool_size=5, max_overflow=10
                    )
                    _logger.log_info("Retrieved credentials from secret manager and SQLAlchemy engine created successfully")
                except Exception as e:
                    _logger.update_error_code('cr_ref_acst_rtu_500-0002')
                    _logger.log_error(configs['TECHNICAL EXCEPTIONS']['cr_ref_acst_rtu_500-0002'])
                    _logger.log_error(f"The Exception is : {e}")
                    raise
            return Database._engine

    @staticmethod
    def get_session(request_id):
        """Create and return a new SQLAlchemy session instance."""
        engine = Database.get_engine(request_id)
        session = sessionmaker(bind=engine)
        return session()

    @staticmethod
    def close_connection():
        """Close the database connection if it exists."""
        if Database._connection:
            Database._connection.close()
            _logger.log_info("Connection closed.")
