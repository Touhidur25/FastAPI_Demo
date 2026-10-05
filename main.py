from fastapi import FastAPI,Path,HTTPException,Query
import json 

app = FastAPI()


def load_data():
    with open("patients.json" , "r") as f:
        data = json.load(f)
    return data 



@app.get("/")
def hello():
    return {'message':'A patient Info Platform'}


@app.get("/about")
def about():
    return {'message':'A Patient APi platform that store records'}


@app.get("/view")
def view ():
    data = load_data()
    return data 

#Show patient_id using path and Error function
@app.get('/patient/{patient_id}')
def patiend_id(patient_id:str = Path(...,description='Enter your patient ID: ', example="P001")):
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail='Patient Data Not Found')

#Query Parameter = Basically ami kivabe sort korte chai oita bujay hote pare catagory wise like bmi/ weight othoba ascending/descending order

@app.get('/sort')
def sort_patients(sort_by:str = Query(...,description='Enter which way you want to sort like according to BMI,Weight,Height'), order:str = Query('asc',description='sort in ascending or descending order')):
    valid_fields = ['height','weight','bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=404, detail='Invalid field select from {valid_fields}')

    if order not in ['asc','desc']:
        raise HTTPException(status_code=404, detail='Invalid field select between ascending and descending')

    data = load_data()

    sort_order = True if order == 'desc' else False

    sorted_data = sorted(data.values(),key=lambda x: x.get(sort_by,0),reverse=sort_order)

    return sorted_data