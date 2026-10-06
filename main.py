from fastapi import FastAPI,Path,HTTPException,Query
from fastapi.responses import JSONResponse
import json 
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal

app = FastAPI()


class Patient(BaseModel):
    id: Annotated[str, Field(...,description='Enter patient id', examples=["P001"])]
    name: Annotated[str, Field(...,description='Enter patient name')]
    city: Annotated[str, Field(...,description='Enter where patient live')]
    age: Annotated[int, Field(..., gt=0, lt=120, description='Age of the patient')]
    gender:  Annotated[Literal['male', 'female', 'others'], Field(..., description='Gender of the patient')]
    weight: Annotated[float, Field(..., description="Enter patient's weight in kg" )]
    height: Annotated[float, Field(..., description="Enter patient's height in meter")]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height)**2)
        return bmi

    @computed_field
    @property
    def verdict(self) -> str:
        if 0< self.bmi < 18.5:
            return 'Underweight'
        elif 18.6<self.bmi <24.9:
            return 'Healthy'
        elif 25<self.bmi<29.9:
            return 'OverWeight'
        else:
            return 'Obese'

def load_data():
    with open("patients.json" , "r") as f:
        data = json.load(f)
    return data 

def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data,f)

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
def view_patient(patient_id:str = Path(...,description='Enter your patient ID: ', example="P001")):
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


@app.post('/create')
def create_patient(patient:Patient):
    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient ALready Exist...')

    data[patient.id] = patient.model_dump(exclude=['id'])

    save_data(data)

    return JSONResponse(status_code=201, content={'message': 'Patients User Created Successfully'})