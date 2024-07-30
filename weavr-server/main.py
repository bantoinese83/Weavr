import logging

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.create_tables import create_database
from app.routers import router

app = FastAPI()

app.include_router(router)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.on_event("startup")
async def on_startup():
    try:
        await create_database()
        logger.info("Database created successfully.")
    except Exception as e:
        logger.error(f"Error creating database: {e}")
        raise


@app.on_event("shutdown")
async def on_shutdown():
    logger.info("Application shutdown.")


@app.get("/health", response_class=JSONResponse)
async def health_check():
    return {"status": "ok"}


# Include router
app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
