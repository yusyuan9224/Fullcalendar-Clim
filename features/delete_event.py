from nicegui import ui
from datetime import datetime
from .event_edit.upload_to_google_sheet import upload_to_google_sheet

def delete_event(calendar, title, start, end, dialog):


    # 格式化輸入的開始和結束時間
    start_dt = datetime.fromisoformat(start).replace(tzinfo=None)
    end_dt = datetime.fromisoformat(end).replace(tzinfo=None)

    print(f"Deleting event: {title} {start_dt} {end_dt}")

    # 查找並刪除事件
    event_found = False
    for event in calendar.events:
        event_start_dt = datetime.fromisoformat(event['start']).replace(tzinfo=None)
        event_end_dt = datetime.fromisoformat(event['end']).replace(tzinfo=None)

        if event['title'] == title and event_start_dt == start_dt and event_end_dt == end_dt:
            calendar.events.remove(event)
            event_found = True
            break

    if not event_found:
        ui.notify("Event not found.", color='red')
        return

    print("Current events in calendar:")
    for event in calendar.events:
        print(event)

    # 更新 Google Sheet
    upload_to_google_sheet(calendar.events)
    calendar.update()  # 更新 FullCalendar 中的事件

    # 使用 JavaScript 強制刷新 FullCalendar 事件
    ui.run_javascript('window.location.reload()')

    # 關閉對話框並刷新界面
    dialog.close()
    ui.notify("Event deleted successfully!")
