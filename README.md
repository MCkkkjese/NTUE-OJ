# NTUE-OJ 全新上線 🎉

NTUE-OJ 是國立臺北教育大學專為程式設計教學與線上練習打造的線上評測系統，結合直覺的 GUI 與即時判題功能，提供學生一個完整的程式練習生態，從題目選擇、程式撰寫到提交歷史追蹤，一切盡在同一視窗完成。  

![啟動畫面示意](Extension_modules/open_picture.png)

---

## 系統特色 ✨

- **多語言支援**：Python（目前）與 C++（未來擴充）  
- **即時評測**：自動比對測資與使用者程式輸出，支援 AC / WA / TLE  
- **提交歷史追蹤**：每日 Commit History 自動記錄每次提交結果與執行時間  
- **直覺 GUI**：選擇題號、輸入程式、檢視結果一目了然  
- **啟動畫面與版本資訊**：增添專業感與使用者體驗  
- **安全執行**：程式判題使用 subprocess 執行，避免無限迴圈造成系統掛起  

![程式主介面示意](Extension_modules/background.png)

---

## 技術架構 🛠️

- **Python 3.x**：程式語言核心  
- **Tkinter / ttkbootstrap**：GUI 介面  
- **PIL (Pillow)**：圖片處理與背景顯示  
- **subprocess**：程式判題與執行  
- **模組化管理**：`Extension_modules` 包含判題、路徑管理與解析度檢查  

程式核心流程：

1. 啟動 GUI 並檢查螢幕解析度與縮放比例  
2. 使用者選擇語言與題號，輸入學號  
3. 將程式碼提交後，Python 程式直接執行判題  
4. 判題結果即時顯示，並記錄在每日 Commit History  

---

## 使用方式 📌

1. Clone 專案：
   ```bash
   git clone https://github.com/MCkkkjese/Computer-Programming-Final-Project.git

2.安裝必要套件：
```bash
pip install ttkbootstrap Pillow

3.執行程式：
```bash
python NTUE_OJ.py

4.使用步驟：
```bash
a.選擇程式語言（Python / C++）

b.選擇題號

c.輸入學生證號碼

d.在程式輸入區撰寫程式

e.點擊 Submit 提交程式

f.查看程式執行結果與 Commit History

---

## 專案來源與致謝

本專案改寫自原始專案 [Computer-Programming-Final-Project](https://github.com/MCkkkjese/Computer-Programming-Final-Project.git)，在原有架構上做了全面優化與功能擴充。

本計劃源自於我和[Liyue-Wei](https://github.com/Liyue-Wei)在國立臺東大學大一上的程式設計課的專題。

特別感謝 [Liyue-Wei](https://github.com/Liyue-Wei) 的構想與啟發，讓 NTUE-OJ 成為可落地運作的專案，沒有他就沒有今天的我。

---
