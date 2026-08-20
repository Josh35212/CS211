import context
from memory import Memory
from register import Register, ZeroRegister
from instruction_set.instr_format import OpCode, CondFlag
from cpu.cpu import ALU


# Create memory with 16 locations
mem = Memory(16)

# Put a value into memory address 0
mem.put(0, 42)

# Read it back
val = mem.get(0)
print("Memory[0] =", val)  # Should print 42

# Try another address
mem.put(5, 99)
print("Memory[5] =", mem.get(5))  # Should print 99

#-------------------------------------------------------------------------------------------#

# r0 should always be zero
r0 = ZeroRegister()
print("r0 =", r0.get())  # Should print 0
r0.put(123)
print("r0 after put =", r0.get())  # Still 0

# Test a normal register
r1 = Register()
r1.put(7)
print("r1 =", r1.get())  # Should print 7

r1.put(-3)
print("r1 after put =", r1.get())  # Should print -3

#-------------------------------------------------------------------------------------------#

alu = ALU()

# ADD
res, flag = alu.exec(OpCode.ADD, 5, 3)
print("5 + 3 =", res, "Flag:", flag)  # 8, P

# SUB
res, flag = alu.exec(OpCode.SUB, 2, 5)
print("2 - 5 =", res, "Flag:", flag)  # -3, M

# MUL
res, flag = alu.exec(OpCode.MUL, -2, 4)
print("-2 * 4 =", res, "Flag:", flag)  # -8, M

# DIV
res, flag = alu.exec(OpCode.DIV, 10, 2)
print("10 // 2 =", res, "Flag:", flag)  # 5, P

# DIV resulting in zero
res, flag = alu.exec(OpCode.SUB, 3, 3)
print("3 - 3 =", res, "Flag:", flag)  # 0, Z

# LOAD/STORE address calculation
res, flag = alu.exec(OpCode.LOAD, 4, 5)
print("LOAD addr 4+5 =", res, "Flag:", flag)  # 9, P

res, flag = alu.exec(OpCode.STORE, 7, 3)
print("STORE addr 7+3 =", res, "Flag:", flag)  # 10, P