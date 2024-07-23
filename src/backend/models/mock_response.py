def mock_response(message):
    if "book" in message.lower():
        return "I can help you book an appointment. What date and time would you prefer?"
    elif "available" in message.lower():
        return "Please provide the date and time you are inquiring about."
    else:
        return "Sorry, I didn't understand that. Can you please rephrase?"
