"""
Ce script permet d'inférer le model de machine learning et de le mettre à disposition
dans un Webservice.
"""

import os
import pickle
from dataclasses import dataclass
from enum import Enum
import pandas as pd

from fastapi import FastAPI, Depends
from titanic.api.auth import verify_token

JAEGER_ENDPOINT = os.getenv("JAEGER_ENDPOINT", "http://localhost:4318/v1/traces")

app = FastAPI()

with open("./src/titanic/api/resources/model.pkl", "rb") as f:
    model = pickle.load(f)


class Pclass(Enum):
    UPPER = 1
    MIDDLE = 2
    LOW = 3


class Sex(Enum):
    MALE = "male"
    FEMALE = "female"


@dataclass
class Passenger:
    pclass: Pclass
    sex: Sex
    sibSp: int
    parch: int

    def to_dict(self) -> dict:
        return {"Pclass": self.pclass.value, "Sex": self.sex.value, "SibSp": self.sibSp, "Parch": self.parch}


@app.get("/health")
def health() -> dict:
    return {"status": "OK"}


@app.post("/infer")
def infer(passenger: Passenger, token: str = Depends(verify_token("api:read"))) -> list:
    df_passenger = pd.DataFrame([passenger.to_dict()])
    df_passenger["Sex"] = pd.Categorical(df_passenger["Sex"], categories=[Sex.FEMALE.value, Sex.MALE.value])
    df_to_predict = pd.get_dummies(df_passenger)
    res = model.predict(df_to_predict)
    return res.tolist()
