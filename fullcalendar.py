from pathlib import Path
from typing import Any, Callable, Dict, Optional
from datetime import datetime

from nicegui.element import Element
from nicegui.events import handle_event

class FullCalendar(Element, component='fullcalendar.js'):

    def __init__(self, options: Dict[str, Any], on_click: Optional[Callable] = None, on_event_drop: Optional[Callable] = None, on_event_resize: Optional[Callable] = None, on_date_dblclick: Optional[Callable] = None) -> None:
        """FullCalendar

        An element that integrates the FullCalendar library (https://fullcalendar.io/) to create an interactive calendar display.

        :param options: dictionary of FullCalendar properties for customization, such as "initialView", "slotMinTime", "slotMaxTime", "allDaySlot", "timeZone", "height", "events".
        :param on_click: callback that is called when a calendar event is clicked.
        :param on_event_drop: callback that is called when a calendar event is dragged and dropped.
        :param on_event_resize: callback that is called when a calendar event is resized.
        :param on_date_dblclick: callback that is called when a calendar date is double-clicked.
        """
        super().__init__()
        self.add_resource(Path(__file__).parent / 'lib')
        self._props['options'] = options

        if on_click:
            self.on('click', lambda e: handle_event(on_click, e))
        if on_event_drop:
            self.on('eventDrop', lambda e: handle_event(on_event_drop, e))
        if on_event_resize:
            self.on('eventResize', lambda e: handle_event(on_event_resize, e))
        if on_date_dblclick:
            self.on('dateDblClick', lambda e: handle_event(on_date_dblclick, e))

    def add_event(self, title: str, start: str, end: str, **kwargs) -> None:
        """Add an event to the calendar.

        :param title: title of the event
        :param start: start time of the event
        :param end: end time of the event
        """
        event_dict = {'title': title, 'start': start, 'end': end, **kwargs}
        self._props['options']['events'].append(event_dict)
        self.update()
        self.run_method('update_calendar')

    def remove_event(self, title: str, start: str, end: str) -> None:
        """Remove an event from the calendar.

        :param title: title of the event
        :param start: start time of the event
        :param end: end time of the event
        """
        start_dt = datetime.fromisoformat(start).replace(tzinfo=None).isoformat()
        end_dt = datetime.fromisoformat(end).replace(tzinfo=None).isoformat()
        for event in self._props['options']['events']:
            event_start_dt = datetime.fromisoformat(event['start']).replace(tzinfo=None).isoformat()
            event_end_dt = datetime.fromisoformat(event['end']).replace(tzinfo=None).isoformat()
            if event['title'] == title and event_start_dt == start_dt and event_end_dt == end_dt:
                self._props['options']['events'].remove(event)
                print(f"Removed event: {event}")  # 调试信息
                break

        self.update()
        self.run_method('update_calendar')

    def edit_event(self, old_title: str, old_start: str, old_end: str, new_title: str, new_start: str, new_end: str, **kwargs) -> None:
        """Edit an event in the calendar.

        :param old_title: original title of the event
        :param old_start: original start time of the event
        :param old_end: original end time of the event
        :param new_title: new title of the event
        :param new_start: new start time of the event
        :param new_end: new end time of the event
        """
        old_start_dt = datetime.fromisoformat(old_start).replace(tzinfo=None)
        old_end_dt = datetime.fromisoformat(old_end).replace(tzinfo=None)
        new_start_dt = datetime.fromisoformat(new_start).replace(tzinfo=None)
        new_end_dt = datetime.fromisoformat(new_end).replace(tzinfo=None)

        for event in self._props['options']['events']:
            event_start_dt = datetime.fromisoformat(event['start']).replace(tzinfo=None)
            event_end_dt = datetime.fromisoformat(event['end']).replace(tzinfo=None)
            if event['title'] == old_title and event_start_dt == old_start_dt and event_end_dt == old_end_dt:
                event.update({'title': new_title, 'start': new_start_dt.isoformat(), 'end': new_end_dt.isoformat(), **kwargs})
                print(f"Updated event: {event}")  # 调试信息
                break
        else:
            print(f"Event not found: {old_title}, {old_start}, {old_end}")  # 调试信息

        self.update()
        self.run_method('update_calendar')

    @property
    def events(self) -> list:
        """List of events currently displayed in the calendar."""
        return self._props['options']['events']
