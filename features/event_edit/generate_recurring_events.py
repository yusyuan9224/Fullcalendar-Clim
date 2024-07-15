from datetime import datetime, timedelta

def generate_recurring_events(title, start, end, category, color, description, frequency, occurrences, attachments, reminder_start, reminder_end, reminder_time, recipients):
    events = []
    start_dt = datetime.fromisoformat(start).replace(tzinfo=None)
    end_dt = datetime.fromisoformat(end).replace(tzinfo=None)
    if frequency == "None":
        events.append({
            'title': title, 
            'start': start_dt.isoformat(), 
            'end': end_dt.isoformat(), 
            'category': category, 
            'description': description, 
            'color': color, 
            'attachments': attachments, 
            'reminder_start': reminder_start, 
            'reminder_end': reminder_end, 
            'reminder_time': reminder_time, 
            'recipients': recipients,
            'frequency': frequency,
            'occurrences': occurrences
        })
    else:
        delta = {
            "Daily": timedelta(days=1),
            "Weekly": timedelta(weeks=1),
            "Monthly": timedelta(weeks=4),  # 简化为4周
            "Yearly": timedelta(weeks=52),  # 简化为52周
        }.get(frequency)
        for i in range(occurrences):  # 根据用户输入的重复事件数量生成事件
            event_title = f"{title} ({i + 1})"  # 在事件标题中添加唯一标识符
            events.append({
                'title': event_title, 
                'start': (start_dt + i * delta).isoformat(), 
                'end': (end_dt + i * delta).isoformat(), 
                'category': category, 
                'description': description, 
                'color': color, 
                'attachments': attachments, 
                'reminder_start': reminder_start, 
                'reminder_end': reminder_end, 
                'reminder_time': reminder_time, 
                'recipients': recipients,
                'frequency': frequency,
                'occurrences': occurrences
            })
    return events
