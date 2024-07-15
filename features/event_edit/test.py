import gspread
from oauth2client.service_account import ServiceAccountCredentials as SAC
Json = "python project/py-fullcalendar/features/event_edit/file.json"
Url = ["https://spreadsheets.google.com/feeds"]
Connect = SAC.from_json_keyfile_name(Json, Url)
GoogleSheets = gspread.authorize(Connect)
Sheet = GoogleSheets.open_by_key("1ILV4IFpx-Ob4TuvC5lPnFka7Go-ynaM85X1E0YiWgsU")
Sheets = Sheet.sheet1
datas = ["03/11", "15:00", "dinner", "taipei"]
Sheets.append_row(datas)
print("寫入成功")
print(Sheets.get_all_values())