from fastapi import FastAPI
from routers import users, orders


app = FastAPI()

# @app.post("/create-user")
# def create_user(user: User):
#     return {
#         "name" : user.name,
#         "age" : user.age
#     }

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])


@app.get("/")
def home():
    return {"message": "Backend running"}

@app.get("/hello")
def hello():
    return {"message" : "Hello Backend"}

@app.get("/search")
def search(name: str):
    return {"searching_for": name}

# health  check API
@app.get("/health")
def health_check():
    return {"status": "running"}





