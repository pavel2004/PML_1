from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI()

model = joblib.load('/models/model.pkl')

class Passenger(BaseModel):
    Pclass: int
    Sex: str
    SibSp: int
    Parch: int

def preprocess(data: Passenger):
    df = pd.DataFrame([data.model_dump()])
    df = pd.get_dummies(df)
    
    expected_cols = ['Pclass', 'SibSp', 'Parch', 'Sex_female', 'Sex_male']
    for col in expected_cols:
        if col not in df.columns:
            df[col] = 0
    df = df[expected_cols]
    
    return df

@app.post("/predict")
def predict(passenger: Passenger):
    input_data = preprocess(passenger)
    prediction = model.predict(input_data)
    
    return {"Survived": int(prediction[0])}
