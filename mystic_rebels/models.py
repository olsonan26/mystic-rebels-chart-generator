from typing import Literal
from pydantic import BaseModel, Field, ConfigDict

class BirthInput(BaseModel):
    model_config=ConfigDict(extra='forbid',allow_inf_nan=False)
    name:str=Field(default='My chart',max_length=120)
    local_date:str
    local_time:str|None='12:00:00'
    timezone:str
    fold:Literal[0,1]|None=None
    latitude:float=Field(ge=-90,le=90)
    longitude:float=Field(ge=-180,le=180)
    location_name:str=Field(default='Entered coordinates',max_length=200)
    coordinate_provenance:str=Field(default='user_entered',max_length=250)
    time_accuracy:Literal['recorded_second','nearest_minute','approximate','unknown']='nearest_minute'
    uncertainty_seconds:float|None=Field(default=30,ge=0,le=86400)
    objects:list[str]=Field(default_factory=lambda:['Sun','Moon','Mercury','Venus','Mars','Jupiter','Saturn','Uranus','Neptune','Pluto','Ascendant','Midheaven'],min_length=1,max_length=100)
    chart_type:Literal['natal','dual']='natal'
