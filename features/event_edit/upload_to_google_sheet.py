# upload_to_google_sheet.py
import gspread
from google.oauth2.service_account import Credentials

SERVICE_ACCOUNT_FILE = 'features/file.json'
SPREADSHEET_ID = '1ILV4IFpx-Ob4TuvC5lPnFka7Go-ynaM85X1E0YiWgsU'

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(credentials)

def load_events_from_google_sheet():
    sheet = client.open_by_key(SPREADSHEET_ID).sheet1
    events = sheet.get_all_records()
    for event in events:
        event['recipients'] = event['recipients'].split(', ') if event['recipients'] else []
        event['attachments'] = event['attachments'].split(', ') if event['attachments'] else []
    return events

def save_event_to_google_sheet(calendar, old_title, old_start, old_end, new_title, new_start, new_end, category, description, frequency, occurrences, attachments, reminder_start, reminder_end, reminder_time, recipients, dialog):
    events = calendar.events
    updated_events = []
    for event in events:
        if event['title'] == old_title and event['start'] == old_start and event['end'] == old_end:
            updated_events.append({
                'title': new_title,
                'start': new_start,
                'end': new_end,
                'category': category,
                'description': description,
                'frequency': frequency,
                'attachments': ', '.join(attachments),
                'reminder_start': reminder_start,
                'reminder_end': reminder_end,
                'reminder_time': reminder_time,
                'recipients': ', '.join(recipients)
            })
        else:
            updated_events.append(event)
    
    upload_to_google_sheet(updated_events)
    calendar.update_events(updated_events)  # 更新 FullCalendar 中的事件
    dialog.close()

def upload_to_google_sheet(events):
    sheet = client.open_by_key(SPREADSHEET_ID).sheet1
    sheet.clear()
    

    # 如果事件列表為空，提供默認標題行
    if not events:
        headers = ["title", "start", "end", "category", "description", "frequency", "occurrences", "attachments", "reminder_start", "reminder_end", "reminder_time", "recipients"]
        data = [headers]
    else:
        headers = list(events[0].keys())
        for event in events:
            for key, value in event.items():
                if isinstance(value, list):
                    event[key] = ', '.join(value)
                elif value is None:
                    event[key] = ''
                else:
                    event[key] = str(value)
        data = [headers] + [list(event.values()) for event in events]
    
    sheet.update(data)

def delete_from_google_sheet(title, start, end):
    events = load_events_from_google_sheet()
    updated_events = [event for event in events if not (event['title'] == title and event['start'] == start and event['end'] == end)]
    upload_to_google_sheet(updated_events)


