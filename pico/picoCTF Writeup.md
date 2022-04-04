# picoCTF Writeup

# Web Exploitation
## GET aHEAD
打開Burp Suite後先切到Proxy頁開啟瀏覽器

![](https://i.imgur.com/lm5M9Lf.png)

可以看到它是使用get方法來取得資料

![](https://i.imgur.com/dRto8F3.png)

接著嘗試按下Forward讓瀏覽器繼續後按下 Choose Blue來觀察請求

![](https://i.imgur.com/FDysBFr.png)

可以看到請求方法變成了post，結合題目標題GET aHEAD，試著把請求變為HEAD方法試試
方法為按下右鍵選擇Send to Repeater

![](https://i.imgur.com/wRiBRHz.png)


將前方POST改為HEAD後送出，就可以看到flag了

![](https://i.imgur.com/6LT5EqA.png)

## Cookies
進入網頁後按F12 切到application慢慢改cookie的值
一個一個試到18之後flag就出來了

## Insp3ct0r
flag藏在原始碼裡面，打開F12要慢慢找吧 = =
flag的三個部分分別藏在html css js裡
可以切到網路頁面按F5重新整理後在同一個地方一起找

## Scavenger Hunt
可先從html檔和css檔中找到兩段flag
js檔中提示要如何使網站不要被搜尋到，所以網址列輸入robots.txt找到下一段flag
接著提示說這是個apache server因此猜想會用.htaccess檔來對系統目錄檔進行權限管理
提示說是用mac電腦與儲存檔案，猜想.DS_Store(應該是用作於儲存這個資料夾的顯示屬性的或是說作為一種更通用的有關顯示設定的元資料儲存)

## where are the robots
網址後輸入robots.txt發現他不希望/8028f.html被看到
這個檔案裡面就有flag了

## logon
先隨便輸入個帳號密碼登入後
把cookie的admin改為True後就有flag了

## dont-use-client-side
F12看原始碼就可以看到密碼的驗證方法(flag)了

## It is my Birthday
他需要兩個md5值一樣但內容不一樣的文件
上網隨便查個碰撞的md5值後寫進檔案丟上網站就好了

```python=
def main():
    data1 = "d131dd02c5e6eec4693d9a0698aff95c2fcab58712467eab4004583eb8fb7f8955ad340609f4b30283e488832571415a085125e8f7cdc99fd91dbdf280373c5bd8823e3156348f5bae6dacd436c919c6dd53e2b487da03fd02396306d248cda0e99f33420f577ee8ce54b67080a80d1ec69821bcb6a8839396f9652b6ff72a70"
    data2 = "d131dd02c5e6eec4693d9a0698aff95c2fcab50712467eab4004583eb8fb7f8955ad340609f4b30283e4888325f1415a085125e8f7cdc99fd91dbd7280373c5bd8823e3156348f5bae6dacd436c919c6dd53e23487da03fd02396306d248cda0e99f33420f577ee8ce54b67080280d1ec69821bcb6a8839396f965ab6ff72a70"

    f1 = open('./asset/data1.pdf', 'wb')
    hex_data = bytes.fromhex(data1)
    f1.write(hex_data)
    f1.close()

    f2 = open('./asset/data2.pdf', 'wb')
    hex_data = bytes.fromhex(data2)
    f2.write(hex_data)
    f2.close()


if __name__ == '__main__':
    main()

```

## Who are you?
這個網站有關於http request header的介紹，可以從這邊參考每個欄位的意義:https://developer.mozilla.org/zh-TW/docs/Web/HTTP/Headers
首先他要求要用pico瀏覽器，所以就打開burp suite開始改請求了
瀏覽器的部分就把User-Agent的值改為PicoBrowser
接著他說他不信任外來者，所以把Referer改為http://mercury.picoctf.net:38322/
然後他說這網站只在2018年執行，所以把Date改為2018 例:Wed, 21 Oct 2018 07:28:00 GMT
接著他又說不信任會被追蹤的人所以把DNT改成1
接著他要求要從瑞典來的人 需要個瑞典的ip 把X-Forwarded-For改為31.3.152.55
接著他要我們說瑞典語 把Accept-Language改為sv
然後就終於結束了 (汗

## login
這個網站把驗證程序放在javascript裡，打開讀一下就知道flag了。

## Includes
打開原始碼後觀察js和css檔裡的flag

## Inspect HTML
F12 看原始碼 結束。

## Local Authority
一開始先隨便打個帳號密碼後，會跳轉到一個登入失敗頁面，然後發現他把帳號密碼寫在了javascript裡。

## Search source
flag藏在了某個css檔裡，慢慢ctrl F就好

## Super Serial
一開始先查看robots.txt後發現有phps檔案，之後便知道可查看index.phps等檔案來得知原始碼。

然後從authentication.phps中發現read_log()函式中會將檔案給讀取出來，並搭配cookies.phps中的例外顯示該變數，因此可得知要以serialize方法寫入payload到login的cookie中

```php=
$log = new access_log("../flag");
echo urlencode(base64_encode(serialize($log)));
```

## Most Cookies
這題已flask的session來儲存cookie，而其機制是將cookie進行加密來進行認證，避免被隨意更改。

但原始碼中有寫出可能的key值，一一進行嘗試找到key後，再修改cookie即可



## picobrowser
開burp suite改請求
把User-Agent的值改為picobrowser