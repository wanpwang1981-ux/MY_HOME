# AI 圖片生成器

這是一個使用 Flask 和 Google Generative AI API 建立的網頁應用程式，可以讓您透過兩種模式生成圖片：

1.  **文生圖 (Text-to-Image):** 根據您提供的文字描述生成一張全新的圖片。
2.  **文+圖生圖 (Text+Image-to-Image):** 結合您上傳的圖片和文字描述，生成一張新的「二創」圖片。

## 架構

本專案採用客戶端-伺服器架構：
- **後端 (Backend):** 一個使用 Python 和 Flask 建立的輕量級網頁伺服器 (`app.py`)。它負責處理圖片生成的核心邏輯，並安全地管理您的 Google API 金鑰。
- **前端 (Frontend):** 一個放在 `templates/index.html` 的單頁 HTML 介面，使用 Tailwind CSS 和原生 JavaScript。使用者在瀏覽器上與此介面互動，介面會向後端發送請求來生成圖片。

## 先決條件

- Python 3.6+
- 一個有效的 Google API 金鑰，並已啟用 "Generative Language API" 和 "Vertex AI API"。

## 安裝與執行

1.  **複製此儲存庫：**
    ```bash
    git clone <repository-url>
    ```
    （注意：請將 `<repository-url>` 替換為您要複製的儲存庫的實際 Git 網址。）

2.  **安裝所需的相依套件：**
    ```bash
    pip install -r requirements.txt
    ```

3.  **設定您的 API 金鑰：**
    在執行程式前，您必須設定 `API_KEY` 環境變數。您的金鑰將被安全地儲存在伺服器端。

    - **Linux / macOS:**
      ```bash
      export API_KEY="YOUR_API_KEY"
      ```
    - **Windows (CMD):**
      ```batch
      set API_KEY=YOUR_API_KEY
      ```
    - **Windows (PowerShell):**
      ```powershell
      $env:API_KEY="YOUR_API_KEY"
      ```

4.  **啟動應用程式：**
    ```bash
    python app.py
    ```

5.  **開啟瀏覽器：**
    啟動後，伺服器會在您的終端機顯示一個本地網址 (通常是 `http://127.0.0.1:5000`)。在您的瀏覽器中打開此網址即可開始使用。

## 檔案結構

```
.
├── app.py                  # Flask 後端主程式
├── image_creator.py        # 圖片生成的核心邏輯函式庫
├── requirements.txt        # 專案相依套件
├── templates/
│   └── index.html          # 前端 HTML 介面
├── static/
│   ├── uploads/            # 儲存使用者上傳的圖片
│   └── generated/          # 儲存 AI 生成的圖片
└── README.md               # 本說明文件
```
