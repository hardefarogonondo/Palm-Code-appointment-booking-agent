from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import pandas as pd
import dateparser
from typing import Any, Text, Dict, List
import os
import logging


class ActionBookAppointment(Action):

    def name(self) -> Text:
        return "action_book_appointment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            # Get the extracted date and time slots
            date = tracker.get_slot('date')
            time = tracker.get_slot('time')

            logging.info(f"Extracted date: {date}, time: {time}")

            if not date:
                dispatcher.utter_message(
                    text="Could you please specify a date for your appointment?")
                return []

            if not time:
                dispatcher.utter_message(
                    text="Could you please specify a time for your appointment?")
                return []

            # Combine date and time into a single string and parse it
            date_time_str = f"{date} {time}" if time else date
            date_time = dateparser.parse(date_time_str)

            logging.info(f"Parsed date_time: {date_time}")

            if not date_time:
                dispatcher.utter_message(
                    text="Could you please specify the date and time more clearly?")
                return []

            # Path to the data folder and appointments file
            current_dir = os.path.dirname(os.path.realpath(__file__))
            data_folder = os.path.join(current_dir, '../../../../../../data')
            appointments_file = os.path.join(data_folder, 'appointments.csv')

            # Debugging line to check the path
            logging.info(f"DEBUG: appointments_file: {appointments_file}")

            # Ensure the data folder exists
            if not os.path.exists(data_folder):
                dispatcher.utter_message(
                    text="The data folder does not exist.")
                return []

            # Load existing appointments
            try:
                appointments = pd.read_csv(appointments_file)
                appointments['Date'] = pd.to_datetime(appointments['Date'])
                appointments['Start'] = pd.to_datetime(
                    appointments['Start']).dt.time
                appointments['End'] = pd.to_datetime(
                    appointments['End']).dt.time
                logging.info(f"Appointments data:\n{appointments.head()}")
            except FileNotFoundError:
                dispatcher.utter_message(
                    text="The appointments file does not exist.")
                return []
            except Exception as e:
                dispatcher.utter_message(
                    text=f"Could not load the appointments data: {str(e)}")
                return []

            # Check for double booking
            for _, row in appointments.iterrows():
                if row['Date'].date() == date_time.date() and row['Start'] <= date_time.time() <= row['End']:
                    dispatcher.utter_message(
                        text="This slot is already booked. Please choose another time.")
                    return []

            # Add the new appointment (assuming end time needs to be calculated or provided)
            new_appointment = pd.DataFrame(
                [{'Name': 'New User', 'Date': date_time.date(), 'Start': date_time.time(), 'End': None}])
            appointments = pd.concat(
                [appointments, new_appointment], ignore_index=True)

            # Generate a unique file name for the new appointment file
            existing_files = [f for f in os.listdir(data_folder) if f.startswith(
                "appointment_") and f.endswith(".csv")]
            next_index = len(existing_files) + 1
            new_filename = os.path.join(
                data_folder, f"appointment_{next_index}.csv")

            # Save the updated appointments to a new CSV file
            appointments.to_csv(new_filename, index=False)

            # Confirm the booking and file creation
            dispatcher.utter_message(text=(f"Your appointment is booked for {date_time.strftime('%Y-%m-%d %H:%M')}. "
                                           f"The updated appointments have been saved to {new_filename}."))
            return []

        except Exception as e:
            logging.error(f"Failed to book appointment: {str(e)}")
            dispatcher.utter_message(
                text="An error occurred while booking your appointment. Please try again.")
            return []
