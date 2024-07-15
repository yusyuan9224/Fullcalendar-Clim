from nicegui import ui
from datetime import datetime
from .event_edit.upload_to_google_sheet import upload_to_google_sheet
from .event_edit.handle_upload import delete_file_from_drive, get_files_in_folder, delete_local_files, delete_folder_from_drive

def delete_event(calendar, title, start, end, dialog):
    # 格式化輸入的開始和結束時間
    start_dt = datetime.fromisoformat(start).replace(tzinfo=None)
    end_dt = datetime.fromisoformat(end).replace(tzinfo=None)

    print(f"Deleting event: {title} {start_dt} {end_dt}")

    # 查找並刪除事件
    event_found = False
    event_to_delete = None
    for event in calendar.events:
        event_start_dt = datetime.fromisoformat(event['start']).replace(tzinfo=None)
        event_end_dt = datetime.fromisoformat(event['end']).replace(tzinfo=None)

        if event['title'] == title and event_start_dt == start_dt and event_end_dt == end_dt:
            event_to_delete = event
            event_found = True
            break

    if not event_found:
        ui.notify("Event not found.", color='red')
        return

    if event_to_delete:
        # 刪除雲端文件
        folder_id = event_to_delete.get('attachments', [])
        if folder_id:
            files = get_files_in_folder(folder_id)
            for file in files:
                delete_file_from_drive(file['id'])
            delete_folder_from_drive(folder_id)

        # 刪除本地文件
        local_folder_path = f"uploads/{title}"
        delete_local_files(local_folder_path)

        # 刪除事件
        calendar.events.remove(event_to_delete)

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
