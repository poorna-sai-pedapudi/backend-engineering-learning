from pydantic import BaseModel, EmailStr, Field

class User(BaseModel):
    name: str = Field(min_length = 2, max_length = 50)
    email: EmailStr
    age: int = Field(gt=0)
    password: str = Field(min_length=6)

class Order(BaseModel):
    user_id: int
    product_name: str = Field(min_length = 2, max_length = 150)
    price: int = Field(gt = 0)

class LoginUser(BaseModel):
    email: EmailStr
    password: str
