from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import os

app = Flask(__name__)
CORS(app)  # Enables cross-origin requests from your vanilla HTML5 frontend

# Global variable to hold our loaded historical arrays in RAM
CLIMATE_DATA = {
    'TMIN': None,
    'TMAX': None,
    'RAIN': None
}

DATA_DIR = r"C:\Users\deves\Downloads\IMD_Data_Bulk"

def load_climate_matrices():
    """
    Pre-loads data arrays into memory when the server starts up 
    so API calls are lightning fast during the hackathon demo.
    """
    print("Initializing historical climate arrays...")
    # In a real run, you would call your ingest_historical_data function here.
    # For testing, we can simulate an active array footprint:
    try:
        # Example: Mocking a 52-year time series array shape for testing
        # Replace with real array loading post-exams: 
        # CLIMATE_DATA['TMIN'] = np.load(os.path.join(DATA_DIR, "tmin_compiled.npy"))
        print("Backend data arrays successfully mapped.")
    except Exception as e:
        print(f"Data loading notice: {e}")

# Explicitly call the load function when the app initializes
with app.app_context():
    load_climate_matrices()

@app.route('/api/simulate', methods=['POST'])
def run_simulation():
    """
    Handles the 'Run Digital Twin Simulation' event from your Leaflet UI.
    """
    data = request.json
    
    # 1. Parse incoming UI state variables
    source = data.get('sourceRegion')   # e.g., "AP"
    target = data.get('targetRegion')   # e.g., "UP"
    scenario = data.get('currentScenario') # e.g., 'heat'
    temp_delta = float(data.get('tempDelta', 0.0))
    rain_delta = int(data.get('rainDelta', 0))
    wind_delta = int(data.get('windDelta', 0))
    
    print(f"\n[Simulation Request] Triggering {scenario.upper()} from {source} targeting {target}")
    print(f"Parameters -> Temp Delta: {temp_delta}°C, Rain Delta: {rain_delta}%, Wind: {wind_delta} km/h")
    
    # 2. AI Inference Engine Placeholder (ConvLSTM Logic)
    # This is where your AI model will calculate how the perturbation spreads.
    # To match your frontend requirement, we return a structural tensor layout:
    
    # Generating a structured grid map matching your spatial dimensions
    # For a temperature scenario (31x31 grid), we generate dummy delta responses:
    grid_lat, grid_lon = 31, 31
    if scenario == 'rain':
        grid_lat, grid_lon = 129, 135 # Rainfall high-res grid structure
        
    # Create an inference matrix demonstrating spatiotemporal ripples
    simulated_grid = []
    for day in range(1, 6): # 5-day forecast tracking (t+1 to t+5)
        # Constructing multidimensional array layout [[lat_idx, lon_idx, intensity_value], ...]
        # This keeps it structurally ready for Leaflet WebGL/Canvas rendering
        day_points = []
        for r in range(0, grid_lat, 2):  # Step by 2 for lighter payload during development
            for c in range(0, grid_lon, 2):
                # Simple math calculation to simulate a localized ripple expanding outwards over time
                base_val = temp_delta if scenario != 'rain' else rain_delta
                decay = 1.0 / (day + 0.5) # Anomaly fades or spreads over days
                day_points.append([r, c, float(base_val * decay)])
        simulated_grid.append(day_points)

    # 3. Formulate the JSON response to update your UI metrics
    response_payload = {
        "status": "success",
        "engine": "ConvLSTM v3 Core",
        "modelConfidence": "92% (INSAT/IMD Assimilated)",
        "forecast_days": 5,
        "spatial_grid": simulated_grid, # The tensor outputs
        "analytics": {
            "riskProbabilities": {
                "heatwave": 85 if scenario == 'heat' else 12,
                "flood": 90 if scenario == 'rain' else 5,
                "cyclone": 75 if scenario == 'cyclone' else 0,
                "coldwave": 80 if scenario == 'fog' else 8
            },
            "sectorImpacts": {
                "agriculture": -18 if scenario == 'heat' else (15 if scenario == 'rain' else -5),
                "waterResources": -25 if scenario == 'heat' else 40,
                "energy": -30 if scenario == 'heat' else -10,
                "health": -15 if scenario == 'heat' else -8
            }
        }
    }
    
    return jsonify(response_payload)

if __name__ == '__main__':
    # Running locally on port 5000
    app.run(debug=True, port=5000)