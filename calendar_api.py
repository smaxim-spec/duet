#!/usr/bin/env python3
"""
Duet Calendar API — Google Calendar integration.
Provides functions to read busy times and create events.
Used by duet_server.py as calendar endpoints.
"""

import json
import os
from datetime import datetime, timedelta

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Scopes: contacts + calendar
SCOPES = [
    'https://www.googleapis.com/auth/contacts',
    'https://www.googleapis.com/auth/calendar'
]
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDS_FILE = os.path.join(BASE_DIR, 'google_credentials.json')
TOKEN_FILE = os.path.join(BASE_DIR, 'google_token.json')
CALENDAR_ID = 'primary'  # User's default calendar


def get_credentials():
    """Get valid Google credentials, refreshing or re-authing as needed."""
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as f:
            f.write(creds.to_json())

    return creds


def get_calendar_service():
    """Return authenticated Google Calendar API service."""
    creds = get_credentials()
    return build('calendar', 'v3', credentials=creds)


def get_busy_times(start_date, num_days=5):
    """
    Get busy time blocks for the next N business days starting from start_date.
    Returns dict: { 'YYYY-MM-DD': ['10:00','10:30',...], ... }
    Each value is a list of 30-min slot start times that are busy.
    """
    service = get_calendar_service()

    # Collect business days
    dates = []
    d = datetime.strptime(start_date, '%Y-%m-%d')
    while len(dates) < num_days:
        if d.weekday() < 5:  # Mon-Fri
            dates.append(d)
        d += timedelta(days=1)

    # Query range — use Eastern time offset
    time_min = dates[0].replace(hour=0, minute=0).strftime('%Y-%m-%dT%H:%M:%S') + '-04:00'
    time_max = dates[-1].replace(hour=23, minute=59).strftime('%Y-%m-%dT%H:%M:%S') + '-04:00'

    # FreeBusy query
    body = {
        'timeMin': time_min,
        'timeMax': time_max,
        'timeZone': 'America/New_York',
        'items': [{'id': CALENDAR_ID}]
    }
    result = service.freebusy().query(body=body).execute()
    busy_periods = result.get('calendars', {}).get(CALENDAR_ID, {}).get('busy', [])

    # Parse busy periods into local datetime pairs
    # API returns times with offset like '2026-04-03T10:00:00-04:00'
    parsed_busy = []
    for bp in busy_periods:
        # Parse ISO with offset, then strip tzinfo to get naive local time
        start_str = bp['start']
        end_str = bp['end']
        # fromisoformat handles the -04:00 offset — gives us aware datetime
        bp_start_aware = datetime.fromisoformat(start_str)
        bp_end_aware = datetime.fromisoformat(end_str)
        # Convert: the offset already represents local time, just strip tzinfo
        bp_start_local = bp_start_aware.replace(tzinfo=None)
        bp_end_local = bp_end_aware.replace(tzinfo=None)
        parsed_busy.append((bp_start_local, bp_end_local))

    # Convert busy periods to 1-hour slot format
    # Slots: 8:30, 9:30, 10:30, 11:30, 12:30, 1:30, 2:30, 3:30, 4:30
    slot_times = [
        (8, 30), (9, 30), (10, 30), (11, 30),
        (12, 30), (13, 30), (14, 30), (15, 30), (16, 30)
    ]

    busy_by_date = {}
    for date in dates:
        ds = date.strftime('%Y-%m-%d')
        busy_slots = []
        for sh, sm in slot_times:
            slot_start = date.replace(hour=sh, minute=sm, second=0)
            slot_end = slot_start + timedelta(minutes=60)
            # Check if any busy period overlaps this slot
            for bp_start_local, bp_end_local in parsed_busy:
                if bp_start_local < slot_end and bp_end_local > slot_start:
                    # Format slot like APPT_SLOTS: "10:00", "1:00", etc.
                    display_hr = sh if sh <= 12 else sh - 12
                    slot_label = f"{display_hr}:{sm:02d}"
                    busy_slots.append(slot_label)
                    break
        busy_by_date[ds] = busy_slots

    return busy_by_date


def create_event(title, date, time, duration_minutes=60, location='', description=''):
    """
    Create a Google Calendar event.
    time format: "10:00", "1:30" etc (matching APPT_SLOTS)
    Returns the created event's htmlLink.
    """
    service = get_calendar_service()

    # Parse time
    parts = time.split(':')
    hr = int(parts[0])
    mn = int(parts[1]) if len(parts) > 1 else 0
    # Hours < 9 are PM (matching APPT_SLOTS: 1:00 = 13:00)
    if hr < 9:
        hr += 12

    start_dt = datetime.strptime(date, '%Y-%m-%d').replace(hour=hr, minute=mn)
    end_dt = start_dt + timedelta(minutes=duration_minutes)

    event = {
        'summary': title,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_dt.strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': 'America/New_York',
        },
        'end': {
            'dateTime': end_dt.strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': 'America/New_York',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': 30},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }

    created = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    return {
        'id': created.get('id'),
        'link': created.get('htmlLink'),
        'status': 'created'
    }


if __name__ == '__main__':
    # Test: print busy times for next 5 business days
    from datetime import date as dt_date
    today = dt_date.today().strftime('%Y-%m-%d')
    print(f"Busy times starting {today}:")
    busy = get_busy_times(today)
    for d, slots in sorted(busy.items()):
        print(f"  {d}: {slots if slots else 'all clear'}")
