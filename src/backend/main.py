from config.config import setup_cors_and_logging
from config.schemas import OuterMessage
from data.read_data import load_appointments_data
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from models.mock_response import mock_response
from pydantic import ValidationError
import logging
import os
import uvicorn

app = FastAPI()
setup_cors_and_logging(app)
appointments_df = load_appointments_data('../../data/appointments.csv')


@app.get("/", response_class=HTMLResponse)
async def get():
    index_path = os.path.join(os.path.dirname(
        __file__), '../../../frontend/index.html')
    with open(index_path) as file:
        return HTMLResponse(content=file.read())


@app.post("/chat", response_class=JSONResponse)
async def chat(request: Request):
    try:
        payload = await request.json()
        logging.info(f"Incoming request payload: {payload}")
        outer_message = OuterMessage(**payload)
        message = outer_message.message
        response = mock_response(message.content)
        logging.info(f"Response message: {response}")
        return {"message": {"content": response, "id": message.id}}
    except ValidationError as error:
        logging.error(f"Validation error: {error.json()}")
        raise HTTPException(status_code=422, detail="Invalid request payload")
    except Exception as error:
        logging.error(f"Unexpected error: {str(error)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.on_event("shutdown")
async def shutdown_event():
    logging.info("Shutting down server...")


if __name__ == "__main__":
    try:
        uvicorn.run("main:app",
                    host="0.0.0.0", port=8000, reload=True)
    except asyncio.CancelledError:
        pass
    except KeyboardInterrupt:
        logging.info("Server stopped by user")
