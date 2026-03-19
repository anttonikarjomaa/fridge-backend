from fastapi import FastAPI
from app.api import inventory, shopping

app = FastAPI(title="Fridge Inventory API")

# Include routers
app.include_router(inventory.router)
app.include_router(shopping.router)

@app.get("/")
def root():
    return {"message": "Fridge backend is running!"}