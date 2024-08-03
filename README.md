# 事件管理系統

本系統是一個基於 FullCalendar 和 Google Sheets 的事件管理應用程式，允許使用者新增、編輯、刪除、拖放事件，並能夠上傳和下載附件。

## 功能特點

1. **新增事件**：使用者可以新增事件，並填寫標題、開始時間、結束時間、類別、描述等信息。
2. **編輯事件**：使用者可以編輯已存在的事件，包括修改標題、時間、類別、描述等信息。
3. **刪除事件**：使用者可以刪除事件，並且會同步刪除 Google Drive 上的附件和本地存儲的附件。
4. **拖放事件**：使用者可以通過拖放事件來改變事件的時間，並自動保存更新到 Google Sheets。
5. **附件管理**：使用者可以為事件上傳附件，並能夠下載和打開附件。
6. **事件提醒**：使用者可以設置事件提醒，並指定提醒的時間和收件人。
7. **事件搜尋與過濾**：使用者可以搜尋和過濾事件。

## 安裝與設定

### 先決條件

- Python 3.8 或以上版本
- 安裝所需的 Python 套件

### 安裝步驟

1. 下載或克隆本專案的程式碼：

2. 安裝所需的 Python 套件：
    ```bash
    pip install -r requirements.txt
    ```

3. 配置 Google Sheets 和 Google Drive API：
    - 申請 Google Cloud Platform 的 API 金鑰，並啟用 Google Sheets 和 Google Drive API。
    - 下載 `credentials.json` 並放置在專案的根目錄。
    - 更新 `features/file.json` 檔案，將內容替換為您的 Google API 憑證。

4. 修改 `upload_to_google_sheet.py`，設定您的 Google Sheets 表單 ID：
    ```python
    SPREADSHEET_ID = 'your_spreadsheet_id'
    ```

## 使用方法

1. 執行應用程式：
    ```bash
    python main.py
    ```

2. 打開瀏覽器，訪問 `http://localhost:8080`，進入事件管理系統。

### 主要操作說明

- **新增事件**：點擊 `Add Event` 按鈕，填寫事件相關信息後點擊 `Add` 按鈕。
- **編輯事件**：點擊事件進行編輯，修改信息後點擊 `Save` 按鈕。
- **刪除事件**：點擊事件進行編輯，點擊 `Delete` 按鈕。
- **拖放事件**：在日曆視圖中拖放事件以改變時間，系統會自動保存更新。
- **管理附件**：在編輯事件時，可以上傳附件並下載或打開已上傳的附件。
- **事件提醒**：在編輯事件時，可以設置提醒時間和收件人。

### 程式碼結構

- `main.py`：應用程式的主要入口，負責配置日曆和處理事件。
- `features/`：包含各種功能模組，包括事件編輯、上傳附件、刪除事件等。
- `fullcalendar/`：包含 FullCalendar 的相關配置和操作。

## 貢獻

歡迎對本專案的貢獻！如果您有任何建議或改進，請提出 Issue 或提交 Pull Request。

## 版權聲明

本專案基於 MIT 授權許可。詳細信息請參閱 LICENSE 檔案。

---

感謝使用本事件管理系統，祝您使用愉快！
