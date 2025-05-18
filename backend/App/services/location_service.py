import requests
import math
from flask import current_app
from bson import ObjectId
from App import mongo
from App.utils.mongo_utils import serialize_ids

def geocode_address(address):
    """Convert address to latitude and longitude coordinates"""
    try:
        # Check if we have cached this address
        cached_location = mongo.db.locations.find_one({"address": address})
        if cached_location:
            return cached_location["latitude"], cached_location["longitude"]
        
        # Using a generic geocoding API service
        api_key = current_app.config.get('GEOCODING_API_KEY', '')
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
        
        response = requests.get(url)
        data = response.json()
        
        if data['status'] == 'OK':
            location = data['results'][0]['geometry']['location']
            lat, lng = location['lat'], location['lng']
            
            # Cache this location
            mongo.db.locations.insert_one({
                "address": address,
                "latitude": lat,
                "longitude": lng,
                "created_at": datetime.utcnow()
            })
            
            return lat, lng
        else:
            raise Exception(f"Geocoding failed: {data['status']}")
    
    except Exception as e:
        print(f"Geocoding error: {str(e)}")
        raise

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points in kilometers using Haversine formula"""
    # Convert latitude and longitude from degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Haversine formula
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    # Radius of Earth in kilometers
    radius = 6371
    
    # Calculate distance
    distance = radius * c
    
    return distance

def get_events_by_proximity(latitude, longitude, radius_km=10):
    """Find events within a certain radius of a location using MongoDB's geospatial queries"""
    # Convert radius to meters
    radius_meters = radius_km * 1000
    
    # Use MongoDB's $geoNear to find nearby events
    events = list(mongo.db.events.find({
        "location": {
            "$nearSphere": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": [float(longitude), float(latitude)]
                },
                "$maxDistance": radius_meters
            }
        },
        "status": "approved"
    }))
    
    # Process results
    result = []
    for event in events:
        # Calculate exact distance
        if "location" in event and event["location"] and "coordinates" in event["location"]:
            coords = event["location"]["coordinates"]
            distance = calculate_distance(latitude, longitude, coords[1], coords[0])
            event["distance"] = round(distance, 2)
        result.append(event)
    
    # Sort by distance
    result.sort(key=lambda x: x.get("distance", float("inf")))
    
    return serialize_ids(result)
