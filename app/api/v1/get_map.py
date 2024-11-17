from flask import Flask, send_file, request, jsonify, make_response
from typing import Tuple, Union
from http import HTTPStatus
from functools import wraps
from io import BytesIO
import logging

"""
Import is intentionally incorrect, since the API used for Scraping the maps is
created in the MapAPI.Dockerfile. This same Dockerfile flattens the folder
structure between: 
- api/v1/get_map.py
- hooks/map_hook.py
- core/settings.py
to them being all in the same folder
"""
from map_hook import GetMapHook

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the GetMapHook instance
map_hook = GetMapHook()

def validate_coordinates(func):
    """
    Decorator to validate coordinate parameters in requests.
    
    Checks if required parameters are present and within valid ranges:
    - Latitude: -90 to 90
    - Longitude: -180 to 180
    - Zoom: 0 to 20
    - Width/Height: 50 to 4000 pixels
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            # Get parameters with defaults
            lat = float(request.args.get('lat', None))
            lng = float(request.args.get('lng', None))
            zoom = int(request.args.get('zoom', 12))
            width = int(request.args.get('width', 800))
            height = int(request.args.get('height', 600))

            # Validate parameters
            if lat is None or lng is None:
                return jsonify({
                    'error': 'Missing required parameters: lat and lng are required'
                }), HTTPStatus.BAD_REQUEST

            if not (-90 <= lat <= 90):
                return jsonify({
                    'error': 'Invalid latitude: must be between -90 and 90'
                }), HTTPStatus.BAD_REQUEST

            if not (-180 <= lng <= 180):
                return jsonify({
                    'error': 'Invalid longitude: must be between -180 and 180'
                }), HTTPStatus.BAD_REQUEST

            if not (0 <= zoom <= 20):
                return jsonify({
                    'error': 'Invalid zoom level: must be between 0 and 20'
                }), HTTPStatus.BAD_REQUEST

            if not (50 <= width <= 4000) or not (50 <= height <= 4000):
                return jsonify({
                    'error': 'Invalid dimensions: width and height must be between 50 and 4000 pixels'
                }), HTTPStatus.BAD_REQUEST

            return func(*args, lat=lat, lng=lng, zoom=zoom, width=width, height=height, **kwargs)

        except ValueError as e:
            return jsonify({
                'error': f'Invalid parameter format: {str(e)}'
            }), HTTPStatus.BAD_REQUEST

    return wrapper

@app.route('/map/screenshot', methods=['GET'])
@validate_coordinates
def get_map_screenshot(lat: float, lng: float, zoom: int, width: int, height: int) -> Union[Tuple[bytes, HTTPStatus], Tuple[dict, HTTPStatus]]:
    """
    Endpoint to get a map screenshot for given coordinates.
    
    Query Parameters:
        lat (float): Latitude of the location
        lng (float): Longitude of the location
        zoom (int, optional): Zoom level (0-20). Defaults to 12
        width (int, optional): Image width in pixels. Defaults to 800
        height (int, optional): Image height in pixels. Defaults to 600
    
    Returns:
        Image file or JSON error response
    """
    try:
        # Get the screenshot using GetMapHook
        image, location_name = map_hook.retry_screenshot(lat, lng, zoom, width, height)

        # Convert PIL Image to bytes
        img_byte_array = BytesIO()
        image.save(img_byte_array, format='PNG')
        img_byte_array.seek(0)

        # Create response with custom headers
        response = make_response(send_file(
            img_byte_array,
            mimetype='image/png',
            as_attachment=False
        ))

        # Add custom headers with metadata
        response.headers['X-Location-Name'] = location_name
        response.headers['X-Coordinates'] = f"{lat},{lng}"
        response.headers['X-Image-Size'] = f"{width}x{height}"
        
        return response

    except Exception as e:
        logger.error(f"Error generating screenshot: {str(e)}")
        return jsonify({
            'error': 'Failed to generate map screenshot',
            'details': str(e)
        }), HTTPStatus.INTERNAL_SERVER_ERROR

@app.route('/map/location', methods=['GET'])
@validate_coordinates
def get_location_info(lat: float, lng: float, zoom: int, width: int, height: int) -> Tuple[dict, HTTPStatus]:
    """
    Endpoint to get location information without screenshot.
    
    Query Parameters:
        lat (float): Latitude of the location
        lng (float): Longitude of the location
        
    Returns:
        JSON response with location information
    """
    try:
        location_name = map_hook.get_location_name(lat, lng)
        return jsonify({
            'location': location_name,
            'coordinates': {
                'lat': lat,
                'lng': lng
            }
        }), HTTPStatus.OK

    except Exception as e:
        logger.error(f"Error getting location info: {str(e)}")
        return jsonify({
            'error': 'Failed to retrieve location information',
            'details': str(e)
        }), HTTPStatus.INTERNAL_SERVER_ERROR

@app.errorhandler(404)
def not_found(e) -> Tuple[dict, HTTPStatus]:
    """Handle 404 errors"""
    return jsonify({'error': 'Resource not found'}), HTTPStatus.NOT_FOUND

@app.errorhandler(500)
def server_error(e) -> Tuple[dict, HTTPStatus]:
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), HTTPStatus.INTERNAL_SERVER_ERROR

@app.route('/health', methods=['GET'])
def health_check() -> Tuple[dict, HTTPStatus]:
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), HTTPStatus.OK

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)