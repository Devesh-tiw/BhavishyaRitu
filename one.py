import numpy as np
import matplotlib.pyplot as plt

def ingest_imd_grd(file_path):
    """
    Reads an IMD Gridded Binary (.GRD) file for Minimum Temperature.
    """
    # Fixed the f-string syntax here!
    print(f"Initiating Data Ingestion for: {file_path}...")
    
    try:
        # 1. Load the raw binary data as 32-bit floats
        raw_data = np.fromfile(file_path, dtype=np.float32)
        print(f"Success: Loaded {raw_data.shape[0]} data points.")
        
        # 2. Handling Missing Values
        # IMD uses 99.9 to represent missing/ocean data.
        # We replace these with NaN (Not a Number) so the AI ignores them.
        raw_data[raw_data == 99.9] = np.nan 
        
        # 3. Reshaping the Data
        # IMD Minimum Temp (1x1 degree) is arranged in a 31x31 grid.
        # Assuming a non-leap year (365 days): 365 * 31 * 31 = 350765 data points
        # reshaped_data = raw_data.reshape((365, 31, 31)) 
        
        return raw_data

    except Exception as e:
        print(f"Ingestion Failed: {e}")
        return None

# --- To test this post-exams ---
filepath = r'C:\Users\deves\OneDrive\Desktop\RituBhavishya\BhavishyaRitu\Mintemp_MinT_2025.GRD'
min_temp_array = ingest_imd_grd(filepath)