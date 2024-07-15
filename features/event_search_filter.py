from nicegui import ui

categories = ["Software", "Domain", "Contract", "Other"]

def search_events(calendar):
    dialog = ui.dialog()
    with dialog, ui.card():
        ui.label('Search Events')
        title_input = ui.input('Title')
        category_input = ui.select(options=categories, label='Category')
        date_input = ui.date()
        ui.button('Search', on_click=lambda: perform_search(calendar, title_input.value, category_input.value, date_input.value, dialog))
    dialog.open()

def perform_search(calendar, title, category, date, dialog):
    results = []
    for event in calendar.events:
        if (not title or title.lower() in event['title'].lower()) and \
           (not category or category.lower() == event.get('category', '').lower()) and \
           (not date or date == event['start'][:10]):
            results.append(event)
    show_results(results)
    dialog.close()

def show_results(results):
    result_dialog = ui.dialog()
    with result_dialog, ui.card():
        ui.label('Search Results')
        for event in results:
            with ui.row():
                ui.label(f"Title: {event['title']}")
                ui.label(f"Category: {event.get('category', 'N/A')}")
                ui.label(f"Start: {event['start']}")
                ui.label(f"End: {event['end']}")
        ui.button('Close', on_click=result_dialog.close)
    result_dialog.open()

def filter_events(calendar):
    dialog = ui.dialog()
    with dialog, ui.card():
        ui.label('Filter Events')
        category_input = ui.select(options=categories, label='Category')
        date_range_start_input = ui.date()
        date_range_end_input = ui.date()
        ui.button('Filter', on_click=lambda: perform_filter(calendar, category_input.value, date_range_start_input.value, date_range_end_input.value, dialog))
    dialog.open()

def perform_filter(calendar, category, date_range_start, date_range_end, dialog):
    results = []
    for event in calendar.events:
        if (not category or category.lower() == event.get('category', '').lower()) and \
           (not date_range_start or date_range_start <= event['start'][:10]) and \
           (not date_range_end or date_range_end >= event['start'][:10]):
            results.append(event)
    show_results(results)
    dialog.close()
