from cpu.memory import Memory
from cpu.cpu import CPU

memory = Memory(256)

# Load programs/fives.obj
with open("programs/obj/fives.obj") as f:
    for addr, line in enumerate(f):
        line = line.strip()
        if line != "":
            memory.put(addr, int(line))

cpu = CPU(memory)

cpu.run()

print("\nFinal register values:")
for i, reg in enumerate(cpu.registers):
    print(f"r{i} =", reg.get())