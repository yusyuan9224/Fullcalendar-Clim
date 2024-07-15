# filter_event_info.py
def filter_event_info(event_info):
    extended_props = event_info.get('extendedProps', {})
    return {
        'title': event_info.get('title', ''),
        'start': event_info.get('start', ''),
        'end': event_info.get('end', ''),
        'category': extended_props.get('category', ''),
        'description': extended_props.get('description', ''),
        'attachments': extended_props.get('attachments', []),
        'frequency': extended_props.get('frequency', 'None'),
        'occurrences': int(extended_props.get('occurrences', 1)),  # 確保為整數
        'reminder_start': extended_props.get('reminder_start', 'False') == 'True',  # 確保為布爾值
        'reminder_end': extended_props.get('reminder_end', 'False') == 'True',  # 確保為布爾值
        'reminder_time': int(extended_props.get('reminder_time', 10) or 10),  # 確保為整數
        'recipients': extended_props.get('recipients', []),
    }
