from datetime import datetime, timedelta
from threading import Timer
from nicegui import ui
from .upload_to_google_sheet import upload_to_google_sheet
from .handle_upload import create_folder, upload_file_to_drive
from .send_email import send_email

def schedule_email(subject, body, recipients, send_time):
    delay = (send_time - datetime.now()).total_seconds()
    Timer(delay, send_email, args=(subject, body, recipients)).start()

def save_event_to_google_sheet(calendar, old_title, old_start, old_end, title, start, end, category, description, frequency, occurrences, attachments, reminder_checkbox, reminder_start, reminder_end, reminder_time, recipients, dialog):
    print(f"Saving event with new values: {title} {start} {end} {category} {description} {frequency} {occurrences} {attachments} {reminder_checkbox} {reminder_start} {reminder_end} {reminder_time} {recipients}")

    # 查找并更新现有事件
    event_found = False
    for event in calendar.events:
        if event['title'] == old_title and datetime.fromisoformat(event['start']).replace(tzinfo=None) == datetime.fromisoformat(old_start).replace(tzinfo=None) and datetime.fromisoformat(event['end']).replace(tzinfo=None) == datetime.fromisoformat(old_end).replace(tzinfo=None):
            event.update({
                'title': title,
                'start': start,
                'end': end,
                'category': category,
                'description': description,
                'frequency': frequency,
                'occurrences': occurrences,
                'attachments': attachments,  # 保存资料夹ID
                'reminder_start': reminder_start,
                'reminder_end': reminder_end,
                'reminder_time': reminder_time,
                'recipients': recipients,
            })
            event_found = True
            break

    # 如果未找到，则添加新事件
    if not event_found:
        calendar.events.append({
            'title': title,
            'start': start,
            'end': end,
            'category': category,
            'description': description,
            'frequency': frequency,
            'occurrences': occurrences,
            'attachments': attachments,  # 保存资料夹ID
            'reminder_start': reminder_start,
            'reminder_end': reminder_end,
            'reminder_time': reminder_time,
            'recipients': recipients,
        })

    upload_to_google_sheet(calendar.events)
    calendar.update()  # 更新 FullCalendar 中的事件

    # 使用 JavaScript 强制刷新 FullCalendar 事件
    ui.run_javascript('window.location.reload()')

    # 关闭对话框并刷新界面
    dialog.close()
    ui.notify("Event saved successfully!")

    # 如果启用了提醒，则安排发送提醒电子邮件
    if reminder_checkbox and (reminder_start or reminder_end):
        reminder_subject = f"Reminder: {title} Event"
        reminder_body = f"Reminder for event {title}:\n\nStart: {start}\nEnd: {end}\nDescription: {description}\nCategory: {category}"

        if reminder_start and reminder_time is not None:
            reminder_time_before_start = datetime.fromisoformat(start) - timedelta(minutes=reminder_time)
            # 调度发送提醒邮件
            schedule_email(reminder_subject, reminder_body, recipients, reminder_time_before_start)

        if reminder_end and reminder_time is not None:
            reminder_time_before_end = datetime.fromisoformat(end) - timedelta(minutes=reminder_time)
            # 调度发送提醒邮件
            schedule_email(reminder_subject, reminder_body, recipients, reminder_time_before_end)
