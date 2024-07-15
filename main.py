# main.py
from datetime import datetime

from fullcalendar import FullCalendar as fullcalendar

from nicegui import events, ui
from features.handle_click import handle_click
from features.handle_date_dblclick import handle_date_dblclick
from features.open_add_event_dialog import open_add_event_dialog
from features.event_edit.upload_to_google_sheet import load_events_from_google_sheet
from features.event_search_filter import search_events, filter_events
from features.event_edit.upload_to_google_sheet import upload_to_google_sheet


options = {
    'initialView': 'dayGridMonth',
    'headerToolbar': {
        'left': 'prev,next today',
        'center': 'title',
        'right': 'customThreeDayView,dayGridMonth,timeGridWeek,timeGridDay'
    },
    'footerToolbar': {'right': 'prev,next'},
    'slotMinTime': '00:00:00',
    'slotMaxTime': '24:00:00',
    'allDaySlot': False,
    'timeZone': 'local',
    'height': 'auto',
    'events': load_events_from_google_sheet(),  # 從 Google Sheets 中加載事件
    'editable': True,  # 使事件可拖放
    'views': {
        'customThreeDayView': {
            'type': 'timeGrid',
            'duration': { 'days': 3 },
            'buttonText': '3 day'
        },
        'dayGridMonth': {
            'type': 'dayGridMonth',
            'buttonText': 'Month'
        },
        'timeGridWeek': {
            'type': 'timeGridWeek',
            'buttonText': 'Week'
        },
        'timeGridDay': {
            'type': 'timeGridDay',
            'buttonText': 'Day'
        }
    }
}

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
                'occurrences': int(occurrences),
                'attachments': attachments,
                'reminder_start': reminder_start,
                'reminder_end': reminder_end,
                'reminder_time': reminder_time,
                'recipients': recipients,
            })
        else:
            updated_events.append(event)
    
    upload_to_google_sheet(updated_events)
    calendar.update_events(updated_events)  # 更新 FullCalendar 中的事件

    if dialog:
        dialog.close()

def handle_event_drop(event):
    if 'info' in event.args:
        event_info = event.args['info']['event']
        old_event_info = event.args['info']['oldEvent']
        print("Event info:", event_info)  # 調試信息
        print("Event args:", event.args)  # 調試信息

        new_start = event_info['start']
        new_end = event_info['end']
        title = event_info['title']
        category = event_info['extendedProps'].get('category', '')
        description = event_info['extendedProps'].get('description', '')
        frequency = event_info['extendedProps'].get('frequency', 'None')
        occurrences = int(event_info['extendedProps'].get('occurrences', 1))  # 確保為整數
        attachments = event_info['extendedProps'].get('attachments', [])
        reminder_start = event_info['extendedProps'].get('reminder_start', False)
        reminder_end = event_info['extendedProps'].get('reminder_end', False)
        reminder_time = event_info['extendedProps'].get('reminder_time', None)
        recipients = event_info['extendedProps'].get('recipients', [])
        dialog = None  # 適當設置此參數

        old_start = old_event_info['start']
        old_end = old_event_info['end']

        # 移除時間格式中的時區部分，保證時間格式的一致性
        old_start = old_start.split('+')[0]
        old_end = old_end.split('+')[0]
        new_start = new_start.split('+')[0]
        new_end = new_end.split('+')[0]

        print(f"Old Start: {old_start}, Old End: {old_end}")  # 調試信息

        for ev in options['events']:
            print(f"Checking event: {ev['title']} {ev['start']} {ev['end']}")  # 調試信息
            if ev['title'] == title and ev['start'].split('+')[0] == old_start and ev['end'].split('+')[0] == old_end:
                ev['start'] = new_start
                ev['end'] = new_end
                save_event_to_google_sheet(
                    calendar,
                    title,
                    old_start,
                    old_end,
                    title,  # 新標題
                    new_start,
                    new_end,
                    category,
                    description,
                    frequency,
                    occurrences,
                    attachments,
                    reminder_start,
                    reminder_end,
                    reminder_time,
                    recipients,
                    dialog
                )
                break

        calendar.update()

def handle_event_resize(event: events.GenericEventArguments):
        '''wait to add...'''
        calendar.update()

calendar = fullcalendar(
    options,
    on_click=lambda event: handle_click(calendar, event),
    on_event_drop=lambda event: handle_event_drop(event),
    on_event_resize=handle_event_resize,
    on_date_dblclick=lambda event: handle_date_dblclick(calendar, event),
)

# 添加一個按鈕，用於打開新增事件的對話框
ui.button('Add Event', on_click=lambda: open_add_event_dialog(calendar, {'dateStr': datetime.now().isoformat()}))
calendar.update()
# 添加搜索和過濾按鈕
ui.button('Search Events', on_click=lambda: search_events(calendar))
ui.button('Filter Events', on_click=lambda: filter_events(calendar))

ui.run()
