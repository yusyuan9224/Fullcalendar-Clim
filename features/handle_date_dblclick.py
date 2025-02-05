from nicegui import ui
from datetime import datetime
from .category_color import get_category_color_selection, get_category_color
from .recurring_events import get_recurring_event_selection
from .event_edit.handle_upload import handle_upload
from .event_edit.save_event import save_event_to_google_sheet
from .event_edit.generate_recurring_events import generate_recurring_events

def handle_date_dblclick(calendar, event):
    date_info = event.args['info'] if 'info' in event.args else {}
    if 'dateStr' not in date_info:
        ui.notify('Invalid date information.', color='red')
        return

    date_str = date_info['dateStr']
    dialog = ui.dialog()
    with dialog, ui.card().style('width: 1200px; max-width: 100%;'):
        ui.label('Add Event').style('width: 100%;')

        with ui.row().style('width: 100%; margin-bottom: 10px;'):
            ui.label('Title').style('width: 100px;')
            title_input = ui.input().style('flex-grow: 1; width: 100%;')

        with ui.row().style('width: 100%; margin-bottom: 10px;'):
            with ui.column().style('flex: 1;'):
                ui.label('Start')
                start_input = ui.input(value=f"{date_str}T00:00").props('type=datetime-local').style('width: 100%;')
                start_input.on('focus', lambda: start_input.props('type=datetime-local'))

            with ui.column().style('flex: 1;'):
                ui.label('End')
                end_input = ui.input(value=f"{date_str}T23:59").props('type=datetime-local').style('width: 100%;')
                end_input.on('focus', lambda: end_input.props('type=datetime-local'))

        with ui.row().style('width: 100%; margin-bottom: 10px;'):
            ui.label('Category').style('width: 100px;')
            category_input = ui.select(options=["Software", "Domain", "Contract", "Other"]).style('flex-grow: 1; width: 100%;')

        with ui.row().style('width: 100%; margin-bottom: 10px;'):
            ui.label('Description').style('width: 100px;')
            description_input = ui.textarea().style('width: 100%;').props('clearable;autogrow')

        uploaded_files = []

        def on_upload(e):
            uploaded_files.append(e)

        attachment_checkbox = ui.checkbox('Add Attachment').style('width: 100%; margin-top: 10px;')
        attachment_input = ui.upload(on_upload=on_upload).style('width: 100%; margin-top: 10px;')
        attachment_input.visible = False

        attachment_checkbox.on_value_change(lambda: setattr(attachment_input, 'visible', attachment_checkbox.value))

        repeat_checkbox = ui.checkbox('Repeat Event', value=False).style('width: 100%; margin-top: 10px;')
        frequency_input = get_recurring_event_selection().style('width: 100%;')
        occurrences_input = ui.number(label='Occurrences', value=10, min=1).style('width: 100%;')

        frequency_input.visible = False
        occurrences_input.visible = False

        def toggle_recurring_settings():
            frequency_input.visible = repeat_checkbox.value
            occurrences_input.visible = repeat_checkbox.value

        repeat_checkbox.on_value_change(toggle_recurring_settings)

        reminder_checkbox = ui.checkbox('Enable Reminder').style('width: 100%; margin-top: 10px;')
        reminder_time_input = ui.number(label='Reminder Time (minutes)', value=10, min=1).style('width: 100%;')
        reminder_switch_start = ui.switch('Reminder Before Start').style('width: 100%;')
        reminder_switch_end = ui.switch('Reminder Before End').style('width: 100%;')
        recipients_input = ui.input('Recipients (comma separated)').style('width: 100%;')

        reminder_time_input.visible = False
        reminder_switch_start.visible = False
        reminder_switch_end.visible = False
        recipients_input.visible = False

        def toggle_reminder_settings():
            reminder_time_input.visible = reminder_checkbox.value
            reminder_switch_start.visible = reminder_checkbox.value
            reminder_switch_end.visible = reminder_checkbox.value
            recipients_input.visible = reminder_checkbox.value

        reminder_checkbox.on_value_change(toggle_reminder_settings)

        def add_event():
            title = title_input.value
            start = start_input.value
            end = end_input.value
            category = category_input.value
            description = description_input.value
            frequency = frequency_input.value if repeat_checkbox.value else "None"
            occurrences = int(occurrences_input.value) if repeat_checkbox.value else 1
            folder_id = None
            reminder_start = reminder_switch_start.value
            reminder_end = reminder_switch_end.value
            reminder_time = int(reminder_time_input.value) if (reminder_switch_start.value or reminder_switch_end.value) else None
            recipients = recipients_input.value.split(',') if recipients_input.value else []

            color = get_category_color(category)

            # 生成重複事件
            recurring_events = generate_recurring_events(
                title, start, end, category, color, description, frequency, occurrences, folder_id, reminder_start, reminder_end, reminder_time, recipients
            )

            # 確認所有必填字段已填寫
            if not title or not start or not end or not category:
                ui.notify('Please fill in all fields.', color='red')
                return

            # 保存事件到 Google Sheet
            for event in recurring_events:
                if attachment_checkbox.value:
                    for uploaded_file in uploaded_files:
                        folder_id = handle_upload(uploaded_file, title_input.value, folder_id)
                
                save_event_to_google_sheet(
                    calendar,
                    "",  # old_title
                    "",  # old_start
                    "",  # old_end
                    event['title'],
                    event['start'],
                    event['end'],
                    event['category'],
                    event['description'],
                    event['frequency'],
                    event['occurrences'],
                    folder_id,
                    reminder_checkbox.value,
                    event['reminder_start'],
                    event['reminder_end'],
                    event['reminder_time'],
                    event['recipients'],
                    dialog
                )

                event['color'] = color

        ui.button('Add', on_click=add_event).style('width: 100%; margin-top: 10px;')
    dialog.open()
