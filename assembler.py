yan_code = b"""
imm a 05
imm b 2f
stm a b
imm a 06
imm b 66
stm a b
imm a 07
imm b 6c
stm a b
imm a 08
imm b 61
stm a b
imm a 09
imm b 67
stm a b
imm a 05
imm b 00
imm c 00
imm i 15
imm b 00
imm c 40
sys open d
imm d fe
add a d
imm i 13
"""

assembly = b''

instruct = {
    b'imm': b'\x20',
    b'add': b'\x02',
    b'stk': b'\x80',
    b'stm': b'\x08',
    b'ldm': b'\x01',
    b'cmp': b'\x40',
    b'jmp': b'\x04',
    b'sys': b'\x10',
}
register = {
    b'a': b'\x20',
    b'b': b'\x40',
    b'c': b'\x08',
    b'd': b'\x02',
    b's': b'\x04',
    b'i': b'\x10',
    b'f': b'\x01',
}
syscall = {
    # b'open': b'\x04',
    b'open': b'\x16',
    b'readc': b'\x01',
    b'readm': b'\x10',
    b'write': b'\x02',
    b'sleep': b'\x20',
    b'exit': b'\x08',
}

"""
RSP + 20
CODE + 300
MEM + 100
REG + 1
CAN + 1
RBP RET
"""


def assemble(x):
    bytess = {}
    order = {
        2: 'op',
        0: 'arg1',
        1: 'arg2'
    }
    parts = x.split(b' ')
    op = parts[0]
    arg1 = parts[1]
    arg2 = parts[2]
    if op == b'imm':
        bytess['op'] = instruct[op]
        bytess['arg1'] = register[arg1]
        bytess['arg2'] = bytes.fromhex(arg2.decode())
        # print(bytess)
        assem = bytess[order[0]] + bytess[order[1]] + bytess[order[2]]
        return assem

    if op == b'add':
        bytess['op'] = instruct[op]
        bytess['arg1'] = register[arg1]
        bytess['arg2'] = register[arg2]
        assem = bytess[order[0]] + bytess[order[1]] + bytess[order[2]]
        return assem

    if op == b'stk':
        bytess['op'] = instruct[op]
        if arg1 == b'00':
            bytess['arg1'] = b'\x00'
        else:
            bytess['arg1'] = register[arg1]
        if arg2 == b'00':
            bytess['arg2'] = b'\x00'
        else:
            bytess['arg2'] = register[arg2]
        assem = bytess[order[0]] + bytess[order[1]] + bytess[order[2]]
        return assem

    if op == b'stm':
        bytess['op'] = instruct[op]
        bytess['arg1'] = register[arg1]
        bytess['arg2'] = register[arg2]
        assem = bytess[order[0]] + bytess[order[1]] + bytess[order[2]]
        return assem

    if op == b'ldm':
        bytess['op'] = instruct[op]
        bytess['arg1'] = register[arg1]
        bytess['arg2'] = register[arg2]
        assem = bytess[order[0]] + bytess[order[1]] + bytess[order[2]]
        return assem

    if op == b'sys':
        bytess['op'] = instruct[op]
        bytess['arg1'] = syscall[arg1]
        bytess['arg2'] = register[arg2]
        assem = bytess[order[0]] + bytess[order[1]] + bytess[order[2]]
        return assem


instructions = yan_code.split(b'\n')[1:-1]

for i in instructions:
    x = assemble(i)
    if x is None:
        continue
    assembly = assembly + x
print(assembly)
