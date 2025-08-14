#!/usr/bin/env python3
"""
Simple Backend for Vegetation Management Agent - Optimized for Render
This version has minimal dependencies and will deploy reliably
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import random
import json
import time

app = FastAPI(title="Vegetation Management Agent API", version="1.0.0")

# Add CORS middleware for web access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
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
    return {
        "message": "Vegetation Management Agent API", 
        "status": "running",
        "version": "1.0.0",
        "deployed_on": "Render"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "timestamp": time.time(),
        "service": "vegetation-management-agent"
    }

@app.post("/detect_vegetation")
async def detect_vegetation(request: VegetationRequest):
    """Detect vegetation along power lines"""
    try:
        # Generate vegetation data based on line characteristics
        vegetation_data = generate_vegetation_data(request.line_id, request.line_data)
        
        return {
            "vegetation_data": vegetation_data,
            "total_points": len(vegetation_data),
            "line_id": request.line_id,
            "analysis_timestamp": time.time()
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
        kml_content = request.kml_content
        
        # Basic validation
        if not kml_content or '<kml' not in kml_content:
            raise ValueError("Invalid KML content")
        
        # Parse KML and extract coordinates
        coordinates = parse_kml_coordinates(kml_content)
        
        # Generate sample vegetation data
        vegetation_data = generate_sample_vegetation_data(coordinates)
        
        # Calculate risk assessment
        risk_analysis = calculate_risk_assessment(vegetation_data)
        
        # Generate growth prediction
        growth_prediction = generate_growth_prediction(vegetation_data)
        
        return {
            "coordinates": coordinates,
            "vegetation_data": vegetation_data,
            "risk_analysis": risk_analysis,
            "growth_prediction": growth_prediction,
            "total_lines": len(coordinates) // 10,  # Estimate
            "vegetation_points": len(vegetation_data),
            "overall_risk": risk_analysis.get("overall_risk", "Low"),
            "growth_rate": growth_prediction.get("growth_rate", "5%"),
            "processing_timestamp": time.time()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def parse_kml_coordinates(kml_content: str) -> List[Dict[str, float]]:
    """Parse KML content and extract coordinates"""
    coordinates = []
    
    # Simple coordinate extraction (you can enhance this)
    lines = kml_content.split('\n')
    for line in lines:
        if '<coordinates>' in line:
            # Extract coordinates from KML
            coord_text = line.replace('<coordinates>', '').replace('</coordinates>', '').strip()
            coord_parts = coord_text.split()
            
            for i in range(0, len(coord_parts), 3):
                if i + 2 < len(coord_parts):
                    try:
                        lon = float(coord_parts[i])
                        lat = float(coord_parts[i + 1])
                        coordinates.append({"lng": lon, "lat": lat})
                    except ValueError:
                        continue
    
    # If no coordinates found, generate sample ones
    if not coordinates:
        coordinates = [
            {"lng": -122.4194, "lat": 37.7749},  # San Francisco
            {"lng": -122.4194, "lat": 37.7849},
            {"lng": -122.4094, "lat": 37.7849},
            {"lng": -122.4094, "lat": 37.7749}
        ]
    
    return coordinates

def generate_sample_vegetation_data(coordinates: List[Dict[str, float]]) -> List[Dict]:
    """Generate sample vegetation data for demonstration"""
    vegetation_data = []
    
    for i, coord in enumerate(coordinates):
        if i % 3 == 0:  # Add vegetation every 3rd point
            vegetation_data.append({
                "id": f"veg_{i}",
                "type": random.choice(["Tree", "Bush", "Grass", "Shrub"]),
                "height": round(random.uniform(1.0, 15.0), 2),
                "distance": round(random.uniform(5.0, 50.0), 2),
                "risk_level": random.choice(["Low", "Medium", "High"]),
                "growth_rate": round(random.uniform(0.5, 3.0), 2),
                "health": random.choice(["Good", "Fair", "Poor"]),
                "priority": random.choice(["Low", "Medium", "High"]),
                "coordinates": coord
            })
    
    return vegetation_data

def generate_vegetation_data(line_id: str, line_data: Dict) -> List[Dict]:
    """Generate vegetation data for a specific line"""
    return generate_sample_vegetation_data([])

def calculate_risk_assessment(vegetation_data: List[Dict]) -> Dict:
    """Calculate risk assessment based on vegetation data"""
    if not vegetation_data:
        return {"overall_risk": "Low", "risk_score": 0}
    
    total_risk = 0
    risk_counts = {"Low": 0, "Medium": 0, "High": 0}
    
    for veg in vegetation_data:
        risk = veg.get("risk_level", "Low")
        risk_counts[risk] += 1
        
        if risk == "High":
            total_risk += 3
        elif risk == "Medium":
            total_risk += 2
        else:
            total_risk += 1
    
    avg_risk = total_risk / len(vegetation_data)
    
    if avg_risk >= 2.5:
        overall_risk = "High"
    elif avg_risk >= 1.5:
        overall_risk = "Medium"
    else:
        overall_risk = "Low"
    
    return {
        "overall_risk": overall_risk,
        "risk_score": round(avg_risk * 33.33, 2),  # Scale to 0-100
        "high_risk": risk_counts["High"],
        "medium_risk": risk_counts["Medium"],
        "low_risk": risk_counts["Low"],
        "total_points": len(vegetation_data)
    }

def generate_growth_prediction(vegetation_data: List[Dict]) -> Dict:
    """Generate growth prediction for vegetation"""
    if not vegetation_data:
        return {"growth_rate": "0%", "time_to_critical": "N/A"}
    
    total_growth = sum(veg.get("growth_rate", 0) for veg in vegetation_data)
    avg_growth = total_growth / len(vegetation_data)
    
    return {
        "growth_rate": f"{round(avg_growth * 100, 1)}%",
        "time_to_critical": f"{round(12 / avg_growth, 1)} months" if avg_growth > 0 else "N/A",
        "month_1": round(avg_growth * 1, 2),
        "month_3": round(avg_growth * 3, 2),
        "month_6": round(avg_growth * 6, 2),
        "year_1": round(avg_growth * 12, 2)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 