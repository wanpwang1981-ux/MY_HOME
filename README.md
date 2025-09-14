# 圖像創作者

此腳本使用 Google Gemini 和 Imagen API，根據輸入的圖像和文字提示生成新圖像。

## 運作方式

該腳本執行一個兩步驟的過程：

1.  **圖像描述：** 它使用 `gemini-2.5-flash-image-preview` 模型為輸入的圖像生成詳細的文字描述。
2.  **圖像生成：** 它將生成的描述與您的文字提示相結合，並使用 `imagen-4.0-generate-001` 模型根據結合後的文字創建一個新圖像。

這使您能夠創建受原始圖像啟發並由您的提示引導的“二創”圖像。

## 先決條件

- Python 3.6+
- 擁有已啟用 Gemini 和 Imagen API 的 Google API 金鑰。

## 安裝

1.  複製此儲存庫：
    ```bash
    git clone <repository-url>
    ```
    （注意：請將 `<repository-url>` 替換為您要複製的儲存庫的實際 Git 網址。）

2.  安裝所需的相依套件：
    ```bash
    pip install -r requirements.txt
    ```

## 使用方式 (圖形介面)

我們提供了一個簡單的網頁介面以便使用。

1.  **設定您的 API 金鑰：**
    在執行程式前，請先設定 `API_KEY` 環境變數。
    ```bash
    export API_KEY="YOUR_API_KEY"
    ```

2.  **啟動介面：**
    ```bash
    python app.py
    ```
    程式將在終端機顯示一個本地網址 (通常是 `http://127.0.0.1:7860`)。在您的瀏覽器中打開此網址即可開始使用。

## 使用方式 (命令列)

您也可以繼續使用原始的命令列工具。

1.  **設定您的 API 金鑰：**

    您可以設定 `API_KEY` 環境變數，或使用 `--api_key` 參數。

2.  **執行腳本：**

    ```bash
    python image_creator.py <您的圖像路徑> "<您的提示>" <輸出圖像路徑>
    ```

    例如：
    ```bash
    python image_creator.py my_image.jpg "這張圖片的未來主義版本" generated_image.png
    ```
