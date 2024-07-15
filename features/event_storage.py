import gspread
from google.oauth2.service_account import Credentials

# 使用您的憑證文件
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
creds = Credentials.from_service_account_file('py-fullcalendar/features/file.json', scopes=scopes)
client = gspread.authorize(creds)

# 使用 Google Sheet ID 打開 Google Sheet
sheet_id = '1ILV4IFpx-Ob4TuvC5lPnFka7Go-ynaM85X1E0YiWgsU'  # 替換為您的 Google Sheet ID
sheet = client.open_by_key(sheet_id).sheet1

def load_events():
    # 讀取 Google Sheet 中的資料
    events = []
    rows = sheet.get_all_records()
    for row in rows:
        events.append({
            'title': row['Title'],
            'start': row['Start'],
            'end': row['End'],
            'category': row['Category'],
            'description': row['Description'],
            'color': row['Color'],
            'frequency': row['Frequency'],
            'attachments': row['Attachments'].split(", ") if row['Attachments'] else [],
            'reminder_start': row['Reminder Start'] == 'True',
            'reminder_end': row['Reminder End'] == 'True',
            'reminder_time': int(row['Reminder Time']) if row['Reminder Time'] else None,
            'recipients': row['Recipients'].split(", ") if row['Recipients'] else []
        })
    return events

def save_events(events):
    # 清空 Google Sheet
    sheet.clear()

    # 設置表頭
    headers = ['Title', 'Start', 'End', 'Category', 'Description', 'Color', 'Frequency', 'Attachments', 'Reminder Start', 'Reminder End', 'Reminder Time', 'Recipients']
    sheet.append_row(headers)

    # 將事件資料上傳到 Google Sheet
    for event in events:
        attachments = event.get('attachments', [])
        if not isinstance(attachments, list):
            attachments = [attachments]
        # 移除 None 值
        attachments = [att for att in attachments if att]

        row = [
            event.get('title', ''),
            event.get('start', ''),
            event.get('end', ''),
            event.get('category', ''),
            event.get('description', ''),
            event.get('color', ''),
            event.get('frequency', ''),
            ", ".join(attachments),  # 確保附件是可迭代的
            event.get('reminder_start', False),
            event.get('reminder_end', False),
            event.get('reminder_time', None),
            ', '.join(event.get('recipients', []))
        ]
        sheet.append_row(row)

    print("Events successfully uploaded to Google Sheet.")
