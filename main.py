from math import e
from fastapi import FastAPI, HTTPException
from routers import users, orders
from database import cursor
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



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

# health check API
@app.get("/health")
def health_check():
    logger.info("Health Check requested")
    return {"status": "running"}

# health db API
@app.get("/health/db")
def database_health_check():
    logger.info("Database health check requested")

    try:
        cursor.execute("select 1 as db_status")
        result = cursor.fetchone()

        return {
            "status": "connected",
            "database": "PostgreSQL",
            "db_status": result["db_status"]
        }
    
    except Exception as e:
        logger.error(f"Database health check failed: {e}")

        raise HTTPException(
            status_code=500,
            detail={
                "status": "disconnected",
                "error": str(e)
            }
        )





