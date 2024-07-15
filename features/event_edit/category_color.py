from nicegui import ui

categories = [
    {"name": "Software", "color": "blue"},
    {"name": "Domain", "color": "green"},
    {"name": "Contract", "color": "red"},
    {"name": "Other", "color": "gray"},
]

def get_category_color_selection():
    category_input = ui.select(options=[c["name"] for c in categories], label='Category')
    return category_input

def get_category_color(category_name):
    for category in categories:
        if category["name"] == category_name:
            return category["color"]
    return "gray"  # Default color if category is not found
