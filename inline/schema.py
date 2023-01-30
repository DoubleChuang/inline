from pydantic import BaseModel, NonNegativeInt
from datetime import datetime
from enum import Enum, auto
from typing import List

# 人數 (日期 時間) 姓名 性別 電話 套餐 備注

class Gender(Enum):
    MALE = 1
    FEMALE = 2

class Meal(Enum):
    MEAL1180 = 1
    MEAL1580 = 2
    Lobster = 3
    
class OrderInfo(BaseModel):
    adult_num: NonNegativeInt
    meal_datetime: datetime
    name: str
    gender: Gender
    phone: str
    meal: List[Meal]
    remark: str