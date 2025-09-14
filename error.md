# 錯誤處理

本文件描述了使用圖像創作者腳本時可能遇到的常見錯誤以及如何解決它們。

## 1. 缺少 API 金鑰

**錯誤訊息：**
```
Error: API key not provided. Please set the API_KEY environment variable or use the --api_key argument.
```

**原因：**
該腳本需要 Google API 金鑰才能運作，但未提供。

**解決方案：**
您可以透過以下兩種方式之一提供 API 金鑰：
- **環境變數：** 設定名為 `API_KEY` 的環境變數。
  ```bash
  export API_KEY="YOUR_API_KEY"
  ```
- **命令列參數：** 執行腳本時使用 `--api_key` 旗標。
  ```bash
  python image_creator.py ... --api_key "YOUR_API_KEY"
  ```

## 2. API 金鑰無效或 API 未啟用

**錯誤訊息：**
您可能會看到來自 Google API 客戶端程式庫的錯誤訊息，通常包含 `PERMISSION_DENIED` 或類似的身份驗證相關錯誤。

**原因：**
- 提供的 API 金鑰不正確或已過期。
- 與該 API 金鑰關聯的 Google 專案未啟用 "Generative Language API" (用於 Gemini) 和 "Vertex AI API" (用於 Imagen)。

**解決方案：**
- 再次檢查您的 API 金鑰是否正確。
- 前往您的 [Google Cloud Console](https://console.cloud.google.com/)，並確保您的專案已啟用 "Generative Language API" 和 "Vertex AI API"。

## 3. 找不到輸入檔案

**錯誤訊息：**
```
FileNotFoundError: [Errno 2] No such file or directory: '<your-image-path>'
```

**原因：**
為輸入圖像提供的路徑不正確，腳本找不到該檔案。

**解決方案：**
- 確認您輸入圖像的路徑是否正確。
- 確保圖像檔案存在於您指定的位置。
- 檢查檔案名稱或路徑中是否有任何拼寫錯誤。

## 4. 未生成圖像

**錯誤訊息：**
```
Error: No image was generated.
```

**原因：**
Imagen API 未返回任何圖像。這可能由以下幾個原因造成：
- 您的提示可能違反了 Google 的安全政策。
- API 服務可能出現了暫時性問題。

**解決方案：**
- 嘗試修改您的提示，使其更具體，並確保其符合安全指南。
- 稍等片刻，然後再次嘗試執行腳本。

## 5. 相依套件問題

**錯誤訊息：**
```
ModuleNotFoundError: No module named 'google'
```
或類似的關於缺少模組的訊息。

**原因：**
您的環境中未安裝所需的 Python 程式庫。

**解決方案：**
使用 pip 安裝 `requirements.txt` 檔案中列出的相依套件：
```bash
pip install -r requirements.txt
```
