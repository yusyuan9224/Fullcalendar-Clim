from nicegui import ui

frequencies = ["None", "Daily", "Weekly", "Monthly", "Yearly"]

def get_recurring_event_selection():
    return ui.select(options=frequencies, label='Repeat Frequency')
