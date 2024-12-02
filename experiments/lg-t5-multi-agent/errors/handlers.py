import json

from configs.logging_config import setup_logger
from errors.exceptions import InvalidRequestError

logger = setup_logger()

def handle_invalid_request_error(error):
    logger.error(f'Error: {error}')

    if isinstance(error, InvalidRequestError):
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(error)})
        }

    return {
        'statusCode': 500,
        'body': json.dumps({'error': 'Internal server error', 'details': str(error)})
    }
