# Copy Translation

## Introduction
+ 這個工具會在你複製文字的時候進行翻譯
+ 原本是因為讀論文常常需要用到 Google 翻譯
+ 在 PDF 檔裡複製的行為表現十分怪異
+ 在網頁和閱讀器之間切換也是相當麻煩
+ 所以搭配一個可以 Always on top 的命令視窗加上這個工具就可以方便查詢

## Usage
+ `Usage: py translate.py [-t update_time] [-d destination language] [-n]`
  + `-t, --update-time`
    + 檢查黏貼版的間隔時間，預設為 1 秒
  + `-d, --destination-lang`
    + 指定要翻譯到什麼語言，預設為英文
  + `-n, --no-first`
    + 加入這個指標來避免程式一啟動就翻譯當前複製的文字
  + `-f, --first`
    + 加入這個指標指定程式啟動後翻譯當前複製的文字

## Demo
  + 打開要閱讀的論文
      ![](https://i.imgur.com/xCnRzQF.png)
  + 使用喜歡的命令視窗打開本程式，喬好位置
      ![](https://i.imgur.com/0P21GgV.png)
  + 選取看不懂的段落，複製，得到翻譯結果
      ![](https://i.imgur.com/bYOOnRH.png)

## Requirements
+ Python requirements
    + googletrans
    + pyperclip
+ Recommends Terminal
    + Windows: [Cmder](https://cmder.net/)
