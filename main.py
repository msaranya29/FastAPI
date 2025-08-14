from fastapi import FastAPI,Path, HTTPException,Query
import json

app = FastAPI()

def load_data():
    with open("patients.json", "r") as f:
        data = json.load(f)
    return data

@app.get("/")
def hello_world():
    return {"message": "Patient Management System API"}

@app.get("/about")
def about():
    return {"message": "A fully functional API for managing patient records, appointments, and medical history."}

@app.get("/view")
def view():
    data = load_data()
    return data

@app.get("/patient/{patient_id}")
def view_patient(patient_id: str=Path(..., description="The ID of the patient to view",example="P001")):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description="Field to sort by height weight or bmi"),order: str = Query("asc", description="Sort in ascending or descending order")):
    valid_fields = ['height', 'weight', 'bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort field. Choose from{valid_fields}")
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="Invalid order. Choose 'asc' or 'desc'")
    
    data= load_data()
    sort_order =True if order == 'desc' else False
    sorted_data = sorted(data.values(), key=lambda x: x[sort_by], reverse= sort_order)
    
    return sorted_data
    
