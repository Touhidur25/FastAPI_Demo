from fastapi import FastAPI
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
    return {'message':'A APi platform that store records'}


@app.get("/view")
def view ():
    data = load_data()
    return data 