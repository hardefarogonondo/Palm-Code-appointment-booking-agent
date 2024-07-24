from config.config import setup_cors_and_logging
from config.schemas import OuterMessage
from data.read_data import load_appointments_data
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from models.mock_response import mock_response
from pydantic import ValidationError
import logging
import os
import requests
import uvicorn

app = FastAPI()
setup_cors_and_logging(app)
appointments_df = load_appointments_data('../../data/appointments.csv')
RASA_SERVER_URL = 'http://localhost:5005/webhooks/rest/webhook'


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
        ##############################
        # response = mock_response(message.content)

        # Send user message to Rasa server
        response = requests.post(RASA_SERVER_URL, json={
                                 "sender": message.id, "message": message.content})
        response_data = response.json()
        if response_data:
            rasa_response = response_data[0].get(
                "text", "No response received")
        else:
            rasa_response = "Sorry, I didn't understand that. Can you please rephrase?"
        logging.info(f"Response message: {rasa_response}")
        return {"message": {"content": rasa_response, "id": message.id}}

        # logging.info(f"Response message: {message}")
        # return {"message": {"content": response, "id": message.id}}
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
