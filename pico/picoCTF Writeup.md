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