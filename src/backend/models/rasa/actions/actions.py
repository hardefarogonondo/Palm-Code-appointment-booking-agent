from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Dict, List, Text
import dateparser
import logging
import os
import pandas as pd
import re


class ActionBookAppointment(Action):
    def name(self) -> Text:
        return "action_book_appointment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            date = tracker.get_slot("date")
            time = tracker.get_slot("time")
            duration = tracker.get_slot("duration")
            logging.info(f"Extracted date: {date}, time: {time}, duration: {duration}")
            if not date:
                dispatcher.utter_template("utter_ask_date", tracker)
                return []
            if not time:
                dispatcher.utter_template("utter_ask_time", tracker)
                return []
            if not duration:
                dispatcher.utter_template("utter_ask_duration", tracker)
                return []
            date_time_str = f"{date} {time}"
            date_time = dateparser.parse(date_time_str)
            logging.info(f"Parsed date_time: {date_time}")
            if not date_time:
                dispatcher.utter_template("utter_ask_date_time_clear", tracker)
                return []
            try:
                duration_minutes = int(re.sub(r'\D', '', duration))
                end_time = (
                    date_time + pd.Timedelta(minutes=duration_minutes)).time()
            except ValueError:
                dispatcher.utter_template("utter_invalid_duration", tracker)
                return []
            current_dir = os.path.dirname(os.path.realpath(__file__))
            data_folder = os.path.join(current_dir, '../../../../../data')
            appointments_file = os.path.join(data_folder, 'appointments.csv')
            logging.info(f"DEBUG: appointments_file: {appointments_file}")
            if not os.path.exists(data_folder):
                dispatcher.utter_template("utter_no_data_folder", tracker)
                return []
            try:
                appointments = pd.read_csv(appointments_file)
                appointments["Date"] = pd.to_datetime(
                    appointments["Date"], format='%Y-%m-%d')
                appointments["Start"] = pd.to_datetime(
                    appointments["Start"], format='%H:%M:%S').dt.time
                appointments["End"] = pd.to_datetime(
                    appointments["End"], format='%H:%M:%S').dt.time
                logging.info(f"Appointments data:\n{appointments.head()}")
            except FileNotFoundError:
                dispatcher.utter_template(
                    "utter_no_appointments_file", tracker)
                return []
            except Exception:
                dispatcher.utter_template(
                    "utter_load_appointments_error", tracker)
                return []
            start_time = date_time.time()
            for _, row in appointments.iterrows():
                if row["Date"].date() == date_time.date():
                    if (row["Start"] <= start_time < row["End"]) or (row["Start"] < end_time <= row["End"]):
                        dispatcher.utter_template(
                            "utter_slot_unavailable", tracker)
                        return []
            dispatcher.utter_template(
                "utter_ask_confirmation", tracker, date=date, time=time, duration=duration)
            return [SlotSet("pending_appointment", {"date": date, "time": time, "duration": duration})]
        except Exception as error:
            logging.error(f"Failed to book appointment: {str(error)}")
            dispatcher.utter_template("utter_booking_error", tracker)
            return []


class ActionAskConfirmation(Action):
    def name(self) -> str:
        return "action_ask_confirmation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:
        dispatcher.utter_template("utter_ask_confirmation", tracker)
        return []


class ActionConfirmBooking(Action):
    def name(self) -> Text:
        return "action_confirm_booking"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        pending_appointment = tracker.get_slot("pending_appointment")
        if not pending_appointment:
            dispatcher.utter_template(
                "utter_no_appointment_to_confirm", tracker)
            return []
        date = pending_appointment.get("date")
        time = pending_appointment.get("time")
        duration = pending_appointment.get("duration")
        current_dir = os.path.dirname(os.path.realpath(__file__))
        data_folder = os.path.join(current_dir, '../../../../../data')
        date_time_str = f"{date} {time}"
        date_time = dateparser.parse(date_time_str)
        duration_minutes = int(re.sub(r'\D', '', duration))
        end_time = (date_time + pd.Timedelta(minutes=duration_minutes)).time()
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)
        try:
            existing_files = [f for f in os.listdir(data_folder) if f.startswith("appointment_") and f.endswith(".csv")]
            next_index = len(existing_files) + 1
            new_filename = os.path.join(data_folder, f"appointment_{next_index}.csv")
            new_appointment = pd.DataFrame([{"Name": "New User", "Date": date_time.date(), "Start": date_time.time(), "End": end_time}])
            new_appointment.to_csv(new_filename, index=False)
            dispatcher.utter_template("utter_confirm_appointment", tracker, date=date, time=time, duration=duration)
        except Exception as error:
            logging.error(f"Could not save the appointment: {str(error)}")
            dispatcher.utter_template("utter_save_appointment_error", tracker)
            return []
        dispatcher.utter_template("utter_ask_anything_else", tracker)
        return [SlotSet("pending_appointment", None)]


class ActionEndConversation(Action):
    def name(self) -> Text:
        return "action_end_conversation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_template("utter_end_conversation", tracker)
        return [SlotSet(slot, None) for slot in tracker.slots]


class ActionAskAvailability(Action):
    def name(self) -> str:
        return "action_ask_availability"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:
        dispatcher.utter_template("utter_ask_availability", tracker)
        return []