from nicegui import ui
from datetime import datetime, timedelta

categories = ["Software", "Domain", "Contract", "Other"]

def create_search_filter_ui(calendar):
    search_card = ui.card().style('width: 1200px; max-width: 100%; margin: 20px auto;')
    search_card.visible = False

    results_card = ui.card().style('width: 1200px; max-width: 100%; margin: 20px auto;')
    results_card.visible = False

    def toggle_search():
        search_card.visible = not search_card.visible
        if not search_card.visible:
            results_card.visible = False

    ui.button('Search/Filter Events', on_click=toggle_search).style('margin: 20px;')

    with search_card:
        ui.label('Search and Filter Events').style('font-size: 24px; margin-bottom: 20px;')

        with ui.row().style('width: 100%; margin-bottom: 10px;'):
            ui.label('Title').style('width: 100px;')
            title_input = ui.input().style('flex-grow: 1; width: 100%;')

        with ui.row().style('width: 100%; margin-bottom: 10px;'):
            ui.label('Category').style('width: 100px;')
            category_input = ui.select(options=categories).style('flex-grow: 1; width: 100%;')

        with ui.row().style('width: 100%; margin-bottom: 10px;'):
            with ui.column().style('flex: 1;'):
                ui.label('Start')
                start_input = ui.input(value=datetime.now().strftime("%Y-%m-%dT00:00")).props('type=datetime-local').style('width: 100%;')

            with ui.column().style('flex: 1;'):
                ui.label('End')
                end_input = ui.input(value=(datetime.now() + timedelta(days=1)).strftime("%Y-%m-%dT23:59")).props('type=datetime-local').style('width: 100%;')

        def perform_search():
            results = []
            for event in calendar.events:
                event_start = datetime.fromisoformat(event['start'])
                event_end = datetime.fromisoformat(event['end'])
                search_start = datetime.fromisoformat(start_input.value) if start_input.value else None
                search_end = datetime.fromisoformat(end_input.value) if end_input.value else None
                
                if (not title_input.value or title_input.value.lower() in event['title'].lower()) and \
                   (not category_input.value or category_input.value == event['category']) and \
                   (not search_start or search_start <= event_start) and \
                   (not search_end or search_end >= event_end):
                    results.append(event)
            
            show_results(results)

        ui.button('Search', on_click=perform_search).style('width: 100%; margin-top: 20px;')

    def show_results(results):
        with results_card:
            results_card.clear()
            ui.label('Search Results').style('font-size: 24px; margin-bottom: 20px;')
            
            if not results:
                ui.label('No events found matching the criteria.')
            else:
                with ui.scroll_area().style('height: 400px;'):
                    for event in results:
                        with ui.card().style('margin-bottom: 10px; padding: 10px;'):
                            ui.label(f"Title: {event['title']}").style('font-weight: bold;')
                            ui.label(f"Category: {event.get('category', 'N/A')}")
                            ui.label(f"Start: {datetime.fromisoformat(event['start']).strftime('%Y-%m-%d %H:%M')}")
                            ui.label(f"End: {datetime.fromisoformat(event['end']).strftime('%Y-%m-%d %H:%M')}")
                            ui.label(f"Description: {event.get('description', 'N/A')}")
                            if event.get('attachments'):
                                ui.label(f"Attachments: {event['attachments']}")
                            ui.label(f"Frequency: {event.get('frequency', 'None')}")
                            if event.get('reminder_start') or event.get('reminder_end'):
                                ui.label(f"Reminder: {'Start' if event.get('reminder_start') else ''} {'End' if event.get('reminder_end') else ''}")
                                ui.label(f"Reminder Time: {event.get('reminder_time', 'N/A')} minutes before")
                            if event.get('recipients'):

                                recipients = event.get('recipients', [])
                                if isinstance(recipients, list):
                                        recipients_str = ", ".join(recipients)
                                elif isinstance(recipients, str):
                                        recipients_str = recipients
                                else:
                                        recipients_str = ""

                                ui.label(f"Recipients: {', '.join(event['recipients'])}")

            ui.button('Hide Results', on_click=lambda: setattr(results_card, 'visible', False)).style('width: 100%; margin-top: 20px;')

        results_card.visible = True
        ui.notify('Results updated', color='green')

    return create_search_filter_ui