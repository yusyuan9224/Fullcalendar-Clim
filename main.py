# main.py
from datetime import datetime

from fullcalendar import FullCalendar as fullcalendar

from nicegui import events, ui
from features.handle_click import handle_click
from features.handle_date_dblclick import handle_date_dblclick
from features.open_add_event_dialog import open_add_event_dialog
from features.event_edit.upload_to_google_sheet import load_events_from_google_sheet
from features.event_search_filter import create_search_filter_ui
from features.event_edit.upload_to_google_sheet import upload_to_google_sheet,save_event_to_google_sheet



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
    'editable': False,  # 使事件可拖放
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



calendar = fullcalendar(
    options,
    on_click=lambda event: handle_click(calendar, event),
    on_date_dblclick=lambda event: handle_date_dblclick(calendar, event),
)

# 添加一個按鈕，用於打開新增事件的對話框
ui.button('Add Event', on_click=lambda: open_add_event_dialog(calendar, {'dateStr': datetime.now().isoformat()}))
calendar.update()
# 添加搜索和過濾按鈕
# 將這行添加到您的主UI構建代碼中，可能在日曆顯示之後
create_search_filter_ui(calendar)

ui.run()
