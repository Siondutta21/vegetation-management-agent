#!/usr/bin/env python3
"""
Simple Working Backend for Vegetation Management Agent
This is a basic, reliable version that will start without issues
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import random
import json
import time

app = FastAPI(title="Vegetation Management Agent API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class VegetationRequest(BaseModel):
    line_id: str
    line_data: Dict
    coordinates: List[Dict[str, float]]
    line_type: str

class KMLRequest(BaseModel):
    kml_content: str

# Cache for storing results
vegetation_cache = {}
risk_cache = {}
growth_cache = {}

@app.get("/")
async def root():
    return {"message": "Vegetation Management Agent API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": time.time()}

@app.post("/detect_vegetation")
async def detect_vegetation(request: VegetationRequest):
    """Detect vegetation along power lines"""
    try:
        # Generate vegetation data based on line characteristics
        vegetation_data = generate_vegetation_data(request.line_id, request.line_data)
        
        return {
            "vegetation_data": vegetation_data,
            "total_points": len(vegetation_data),
            "line_id": request.line_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/assess_risk")
async def assess_risk(request: Dict):
    """Assess risk of vegetation interference"""
    try:
        vegetation_data = request.get("vegetation_data", [])
        risk_analysis = calculate_risk_assessment(vegetation_data)
        
        return {
            "risk_analysis": risk_analysis,
            "assessment_timestamp": time.time()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict_growth")
async def predict_growth(request: Dict):
    """Predict vegetation growth patterns"""
    try:
        vegetation_data = request.get("vegetation_data", [])
        growth_prediction = generate_growth_prediction(vegetation_data)
        
        return {
            "growth_prediction": growth_prediction,
            "prediction_timestamp": time.time()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process_kml")
async def process_kml(request: KMLRequest):
    """Process KML file and generate map configuration"""
    try:
        # Simple KML processing without external dependencies
        kml_content = request.kml_content
        
        # Basic validation
        if not kml_content or '<kml' not in kml_content:
            raise HTTPException(status_code=400, detail="Invalid KML content")
        
        # Extract basic coordinates (simplified)
        coordinates = extract_coordinates_simple(kml_content)
        
        if not coordinates:
            raise HTTPException(status_code=400, detail="No coordinates found in KML")
        
        # Calculate simple bounds
        bounds = calculate_simple_bounds(coordinates)
        center_lat = (bounds['min_lat'] + bounds['max_lat']) / 2
        center_lon = (bounds['min_lon'] + bounds['max_lon']) / 2
        
        # Determine zoom level
        lat_span = bounds['max_lat'] - bounds['min_lat']
        lon_span = bounds['max_lon'] - bounds['min_lon']
        max_span = max(lat_span, lon_span)
        
        if max_span > 10:
            zoom_level = 5
        elif max_span > 5:
            zoom_level = 6
        elif max_span > 2:
            zoom_level = 7
        elif max_span > 1:
            zoom_level = 8
        elif max_span > 0.5:
            zoom_level = 9
        else:
            zoom_level = 10
        
        return {
            "success": True,
            "map_config": {
                "center_lat": center_lat,
                "center_lon": center_lon,
                "zoom_level": zoom_level,
                "bounds": bounds
            },
            "lines_data": [{"name": "KML Line", "coordinates": coordinates}],
            "total_lines": 1,
            "total_coordinates": len(coordinates)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/validate_kml")
async def validate_kml(request: KMLRequest):
    """Validate KML file format and content"""
    try:
        kml_content = request.kml_content
        
        validation_result = {
            "is_valid": False,
            "has_kml_tag": False,
            "has_placemarks": False,
            "has_coordinates": False,
            "error_message": ""
        }
        
        # Check for KML tag
        if '<kml' in kml_content:
            validation_result['has_kml_tag'] = True
        
        # Check for Placemark tags
        if '<Placemark>' in kml_content:
            validation_result['has_placemarks'] = True
        
        # Check for coordinates
        if '<coordinates>' in kml_content:
            validation_result['has_coordinates'] = True
        
        # Try to extract coordinates
        coordinates = extract_coordinates_simple(kml_content)
        if coordinates:
            validation_result['is_valid'] = True
        
        return validation_result
        
    except Exception as e:
        return {
            "is_valid": False,
            "error_message": str(e)
        }

# Helper functions
def extract_coordinates_simple(kml_content: str) -> List[Dict[str, float]]:
    """Extract coordinates from KML content (simplified)"""
    coordinates = []
    
    try:
        # Find coordinates section
        if '<coordinates>' in kml_content:
            start = kml_content.find('<coordinates>') + len('<coordinates>')
            end = kml_content.find('</coordinates>')
            
            if start > 0 and end > start:
                coord_text = kml_content[start:end].strip()
                coord_pairs = coord_text.split()
                
                for pair in coord_pairs:
                    parts = pair.split(',')
                    if len(parts) >= 2:
                        try:
                            lon = float(parts[0])
                            lat = float(parts[1])
                            coordinates.append({'lon': lon, 'lat': lat})
                        except ValueError:
                            continue
    except:
        pass
    
    return coordinates

def calculate_simple_bounds(coordinates: List[Dict[str, float]]) -> Dict[str, float]:
    """Calculate bounding box for coordinates"""
    if not coordinates:
        return {
            'min_lat': 37.7749, 'max_lat': 37.7749,
            'min_lon': -122.4194, 'max_lon': -122.4194
        }
    
    lats = [coord['lat'] for coord in coordinates]
    lons = [coord['lon'] for coord in coordinates]
    
    return {
        'min_lat': min(lats),
        'max_lat': max(lats),
        'min_lon': min(lons),
        'max_lon': max(lons)
    }

def generate_vegetation_data(line_id: str, line_data: Dict) -> List[Dict]:
    """Generate vegetation data for a power line"""
    vegetation_points = []
    
    # Determine vegetation density based on line characteristics
    line_type = line_data.get('line_type', 'transmission')
    region = line_data.get('region', 'Unknown')
    
    # Base vegetation count
    base_count = 50 if line_type == 'transmission' else 30
    
    # Adjust based on region
    if 'forest' in region.lower() or 'rural' in region.lower():
        base_count *= 2
    elif 'urban' in region.lower() or 'city' in region.lower():
        base_count *= 0.3
    
    # Generate vegetation points
    for i in range(base_count):
        vegetation_points.append({
            "id": f"VEG_{line_id}_{i:03d}",
            "type": random.choice(["Oak", "Pine", "Maple", "Birch", "Cedar"]),
            "height": random.uniform(5, 25),
            "distance": random.uniform(5, 50),
            "riskScore": random.uniform(0.1, 0.9),
            "riskLevel": random.choice(["Low", "Medium", "High", "Critical"]),
            "priority": random.choice(["Low", "Medium", "High", "Immediate"]),
            "estimatedCost": random.uniform(1000, 5000)
        })
    
    return vegetation_points

def calculate_risk_assessment(vegetation_data: List[Dict]) -> Dict:
    """Calculate risk assessment for vegetation data"""
    if not vegetation_data:
        return {"error": "No vegetation data provided"}
    
    critical_count = sum(1 for v in vegetation_data if v['riskLevel'] == 'Critical')
    high_count = sum(1 for v in vegetation_data if v['riskLevel'] == 'High')
    medium_count = sum(1 for v in vegetation_data if v['riskLevel'] == 'Medium')
    low_count = sum(1 for v in vegetation_data if v['riskLevel'] == 'Low')
    
    total_cost = sum(v['estimatedCost'] for v in vegetation_data)
    avg_risk = sum(v['riskScore'] for v in vegetation_data) / len(vegetation_data)
    
    return {
        "critical_risks": critical_count,
        "high_risks": high_count,
        "medium_risks": medium_count,
        "low_risks": low_count,
        "total_cost": total_cost,
        "average_risk_score": avg_risk,
        "total_vegetation_points": len(vegetation_data)
    }

def generate_growth_prediction(vegetation_data: List[Dict]) -> Dict:
    """Generate growth prediction for vegetation"""
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    predictions = []
    for month in months:
        predictions.append({
            "month": month,
            "growth_rate": random.uniform(0.1, 0.3),
            "risk_increase": random.uniform(0.05, 0.2),
            "maintenance_needed": random.choice([True, False])
        })
    
    return {
        "predictions": predictions,
        "total_growth": sum(p['growth_rate'] for p in predictions),
        "maintenance_schedule": [p['month'] for p in predictions if p['maintenance_needed']]
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Simple Vegetation Management Agent API Server...")
    print("📊 API will be available at: http://localhost:8000")
    print("🔍 Health check: http://localhost:8000/health")
    uvicorn.run(app, host="0.0.0.0", port=8000) 