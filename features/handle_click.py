from nicegui import ui
from datetime import datetime
from .category_color import get_category_color_selection
from .recurring_events import get_recurring_event_selection
from .event_edit.handle_upload import handle_upload, get_files_in_folder, get_file_download_link, get_file_open_link, get_folder_open_link
from .event_edit.save_event import save_event_to_google_sheet
from .delete_event import delete_event
from .event_edit.filter_event_info import filter_event_info

def handle_click(calendar, event):
    if 'info' in event.args:
        event_info = filter_event_info(event.args['info']['event'])
        print("Event info:", event_info)  # 调试信息
        dialog = ui.dialog()
        with dialog, ui.card().style('width: 1200px; max-width: 100%;'):
            ui.label('Edit Event').style('width: 100%;')

            with ui.row().style('width: 100%; margin-bottom: 10px;'):
                ui.label('Title').style('width: 100px;')
                title_input = ui.input(value=event_info.get('title', '')).style('flex-grow: 1; width: 100%;')

            with ui.row().style('width: 100%; margin-bottom: 10px;'):
                with ui.column().style('flex: 1;'):
                    ui.label('Start')
                    start_input = ui.input(value=event_info.get('start', '')[:16]).props('type=datetime-local').style('width: 100%;')
                    start_input.on('focus', lambda: start_input.props('type=datetime-local'))

                with ui.column().style('flex: 1;'):
                    ui.label('End')
                    end_input = ui.input(value=event_info.get('end', '')[:16]).props('type=datetime-local').style('width: 100%;')
                    end_input.on('focus', lambda: end_input.props('type=datetime-local'))

            with ui.row().style('width: 100%; margin-bottom: 10px;'):
                ui.label('Category').style('width: 100px;')
                category_input = ui.select(options=["Software", "Domain", "Contract", "Other"], value=event_info.get('category', 'Other')).style('flex-grow: 1; width: 100%;')

            with ui.row().style('width: 100%; margin-bottom: 10px;'):
                ui.label('Description').style('width: 100px;')
                description_input = ui.textarea(value=event_info.get('description', '')).style('width: 100%;').props('clearable;autogrow')

            uploaded_files = []

            def on_upload(e):
                uploaded_files.append(e)

            attachment_checkbox = ui.checkbox('Add Attachment').style('width: 100%; margin-top: 10px;')
            attachment_input = ui.upload(on_upload=on_upload).style('width: 100%; margin-top: 10px;')
            attachment_input.visible = False

            if event_info.get('attachments'):
                folder_id = event_info.get('attachments')
                folder_open_link = get_folder_open_link(folder_id)
                ui.button('Open Folder', on_click=lambda link=folder_open_link: ui.open(link,new_tab=True)).style('width: 100%; margin-top: 10px;')
                files = get_files_in_folder(folder_id)
                for file in files:
                    download_link = get_file_download_link(file['id'])
                    open_link = get_file_open_link(file['id'])
                    ui.label(f"Current Attachment: {file['name']}").style('width: 100%; margin-top: 10px;')
                    with ui.row().style('width: 100%; margin-bottom: 10px;'):
                        ui.button('Download Attachment', on_click=lambda link=download_link: ui.open(link,new_tab=True)).style('width: 48%; margin-top: 10px;')
                        ui.button('Open Attachment', on_click=lambda link=open_link: ui.open(link,new_tab=True)).style('width: 48%; margin-top: 10px;')

            attachment_checkbox.on_value_change(lambda: setattr(attachment_input, 'visible', attachment_checkbox.value))

            repeat_checkbox = ui.checkbox('Repeat Event', value=event_info.get('frequency', 'None') != 'None').style('width: 100%; margin-top: 10px;')
            frequency_input = get_recurring_event_selection().style('width: 100%;')
            occurrences_input = ui.number(label='Occurrences', value=event_info.get('occurrences', 10), min=1).style('width: 100%;')

            frequency_input.visible = repeat_checkbox.value
            occurrences_input.visible = repeat_checkbox.value

            def toggle_recurring_settings():
                frequency_input.visible = repeat_checkbox.value
                occurrences_input.visible = repeat_checkbox.value

            repeat_checkbox.on_value_change(toggle_recurring_settings)

            reminder_checkbox = ui.checkbox('Enable Reminder', value=event_info.get('reminder_start', False) or event_info.get('reminder_end', False)).style('width: 100%; margin-top: 10px;')
            reminder_time_input = ui.number(label='Reminder Time (minutes)', value=event_info.get('reminder_time', 10), min=1).style('width: 100%;')
            reminder_switch_start = ui.switch('Reminder Before Start', value=event_info.get('reminder_start', False)).style('width: 100%;')
            reminder_switch_end = ui.switch('Reminder Before End', value=event_info.get('reminder_end', False)).style('width: 100%;')
            recipients_input = ui.input('Recipients (comma separated)', value=",".join(event_info.get('recipients', []))).style('width: 100%;')

            reminder_time_input.visible = reminder_checkbox.value
            reminder_switch_start.visible = reminder_checkbox.value
            reminder_switch_end.visible = reminder_checkbox.value
            recipients_input.visible = reminder_checkbox.value

            def toggle_reminder_settings():
                reminder_time_input.visible = reminder_checkbox.value
                reminder_switch_start.visible = reminder_checkbox.value
                reminder_switch_end.visible = reminder_checkbox.value
                recipients_input.visible = reminder_checkbox.value

            reminder_checkbox.on_value_change(toggle_reminder_settings)

            def save_event():
                folder_id = event_info.get('attachments',None)
                if attachment_checkbox.value:
                    for uploaded_file in uploaded_files:
                        folder_id = handle_upload(uploaded_file, title_input.value,folder_id)
                
                save_event_to_google_sheet(
                    calendar,
                    event_info.get('title', ''),
                    event_info.get('start', ''),
                    event_info.get('end', ''),
                    title_input.value,
                    start_input.value,
                    end_input.value,
                    category_input.value,
                    description_input.value,
                    frequency_input.value if repeat_checkbox.value else "None",  # 仅当勾选复选框时传递频率
                    int(occurrences_input.value) if repeat_checkbox.value else 1,  # 确保传递的重复次数为整数
                    folder_id or event_info.get('attachments', None),
                    reminder_checkbox.value,
                    reminder_switch_start.value,
                    reminder_switch_end.value,
                    int(reminder_time_input.value) if (reminder_switch_start.value or reminder_switch_end.value) else None,
                    recipients_input.value.replace(" ", "").split(',') if recipients_input.value else [],
                    dialog
                )

            ui.button('Save', on_click=save_event).style('width: 100%; margin-top: 10px;')

            ui.button('Delete', on_click=lambda: delete_event(
                calendar,
                event_info.get('title', ''),
                event_info.get('start', ''),
                event_info.get('end', ''),
                dialog
            )).style('width: 100%; margin-top: 10px;')
        dialog.open()

        calendar.update()