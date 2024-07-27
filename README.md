# Palm Code Appointment Booking Agent

This project is an appointment booking agent designed to help users schedule appointments through a conversational interface. It leverages Rasa for natural language understanding and processing, along with a backend API built with FastAPI.

## Table of Contents

1. [Disclaimer](#disclaimer)
2. [Project Description](#project-description)
3. [Project Architecture](#project-architecture)
4. [Features](#features)
5. [Installation Guide](#installation-guide)
6. [References](#references)

## Disclaimer

This project was developed as part of the recruitment process for the Machine Learning Engineer position at [Palm Code](https://palm-co.de/). It is intended for demonstration and educational purposes, showcasing the integration of a chatbot with backend services for appointment scheduling.

## Project Description

The Appointment Booking Agent is an AI-driven service that allows users to schedule appointments through a chatbot interface. The backend is built using FastAPI, and Rasa is used for the chatbot's conversational logic. This system is designed to understand user queries, manage appointment slots, and provide relevant responses.

## Project Architecture

The project is organized into two main parts:

- **Frontend**: A simple HTML page (`index.html`) for interacting with the chatbot.
- **Backend**: Contains the Rasa model and the API service.

The folder structure is as follows:

```bash
.
├── data
│   ├── appointments.csv
├── references
│   ├── api.yml
├── src
│   ├── backend
│   │   ├── config
│   │   │   ├── config.py
│   │   │   ├── schemas.py
│   │   ├── data
│   │   │   ├── read_data.py
│   │   ├── models
│   │   │   ├── rasa
│   │   │   │   ├── actions
│   │   │   │   │   ├── actions.py
│   │   │   │   ├── data
│   │   │   │   │   ├── nlu.yml
│   │   │   │   │   ├── rules.yml
│   │   │   │   │   ├── stories.yml
│   │   │   │   ├── models
│   │   ├── main.py
│   │   ├── start_services.sh
│   ├── frontend
│   │   ├── index.html
├── docker-compose.yaml
├── requirements.txt
└── README.md

```

## Features
Natural Language Understanding: Uses Rasa to understand user inputs.
Appointment Management: Schedules, confirms, and cancels appointments.
API Integration: Provides a RESTful API for interaction.

## Installation Guide

1. Clone the repository

```bash
git clone git@github.com:hardefarogonondo/Palm-Code-appointment-booking-agent.git
```

Once all the terminals are running, you can access the frontend at:

```bash
http://localhost:8000/
```

Backend at:

```bash
Rasa Server: Accessible at http://localhost:5005/
Action Server: Accessible at http://localhost:5055/
FastAPI Backend: Accessible at http://localhost:8000/
```

2. Testing the API
You can interact with the chatbot using the frontend or directly through API endpoints using tools like Postman.

3. Running Manually
Clone the repository and navigate to the frontend folder. Open index.html in a browser or using a live server plugin in your code editor (like Live Server in VS Code).

4. Open three terminals:

First Terminal: Navigate to /src/backend/models/rasa and run:

```bash
rasa run --enable-api
```

Second Terminal: In the same directory, run:

```bash
rasa run actions
```

Third Terminal: Navigate to /src/backend and run:

```bash
uvicorn main:app
```

If all three services are running without errors, you can start interacting with the chatbot via the frontend.

## References
[Rasa](https://rasa.com/)

[FastAPI](https://fastapi.tiangolo.com/)