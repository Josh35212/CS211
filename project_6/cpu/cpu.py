"""
Josh Gilliam
Info: CS211 2/24/26
Credit: ChatGPT helped debug step method in CPU

Duck Machine model DM2022 CPU
"""

import context  #  Python import search from project root
from instruction_set.instr_format import Instruction, OpCode, CondFlag, decode
from cpu.memory import Memory
from cpu.register import Register, ZeroRegister
from cpu.mvc import MVCEvent, MVCListenable

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
#log.setLevel(logging.INFO)
log.setLevel(logging.WARNING)

class ALU(object):
    """The arithmetic logic unit (also called a "functional unit"
    in a modern CPU) executes a selected function but does not
    otherwise manage CPU state. A modern CPU core may have several
    ALUs to boost performance by performing multiple operatons
    in parallel, but the Duck Machine has just one ALU in one core.
    """
    # The ALU chooses one operation to apply based on a provided
    # operation code.  These are just simple functions of two arguments;
    # in hardware we would use a multiplexer circuit to connect the
    # inputs and output to the selected circuitry for each operation.
    ALU_OPS = {
        OpCode.ADD: lambda x, y: x + y,
        OpCode.SUB: lambda x, y: x - y,
        OpCode.MUL: lambda x, y: x * y,
        OpCode.DIV: lambda x, y: x // y,
        # For memory access operations load, store, the ALU
        # performs the address calculation
        OpCode.LOAD: lambda x, y: x + y,
        OpCode.STORE: lambda x, y: x + y,
        # Some operations perform no operation
        OpCode.HALT: lambda x, y: 0
    }

    def exec(self, op: OpCode, in1: int, in2: int) -> tuple[int, CondFlag]:
        try:
            result = self.ALU_OPS[op](in1, in2)
        except Exception:
            return 0, CondFlag.V
        
        if result == 0:
            flag = CondFlag.Z
        elif result < 0:
            flag = CondFlag.M
        else: 
            flag = CondFlag.P

        return result, flag
    

class CPUStep(MVCEvent):
    """CPU is beginning step with PC at a given address"""
    def __init__(self, subject: "CPU", pc_addr: int,
                 instr_word: int, instr: Instruction)-> None:
        self.subject = subject
        self.pc_addr = pc_addr
        self.instr_word = instr_word
        self.instr = instr


class CPU(MVCListenable):
    """Duck Machine central processing unit (CPU)
    has 16 registers (including r0 that always holds zero
    and r15 that holds the program counter), a few
    flag registers (condition codes, halted state),
    and some logic for sequencing execution.  The CPU
    does not contain the main memory but has a bus connecting
    it to a separate memory.
    """
    def __init__(self, memory: Memory):
        super().__init__()
        self.memory = memory  # Not part of CPU; what we really have is a connection
        self.registers = [ ZeroRegister(), Register(), Register(), Register(),
                           Register(), Register(), Register(), Register(),
                           Register(), Register(), Register(), Register(),
                           Register(), Register(), Register(), Register() ]
        self.condition = CondFlag.ALWAYS
        self.halted = False
        self.alu = ALU()

    def step(self):
        """One fetch/decode/execute step"""
        
        ### Fetch ###

        instr_addr = self.registers[15].get()
        log.debug(f"Fetch: PC = {instr_addr}")
        instr_word = self.memory.get(instr_addr)
        log.debug(f"Fetch: Memory [{instr_addr}] = {instr_word}")

        ### Decode ###

        instr = decode(instr_word)
        # Display the CPU state when we have decoded the instruction,
        # before we have executed it
        self.notify_all(CPUStep(self, instr_addr, instr_word, instr))

        ### Execute ###

        # Check instruction predicate
        predicate_satisfied = (self.condition & instr.cond) != 0
        log.debug(f"Execute: Predicate Satisfied?: {predicate_satisfied}")

        if predicate_satisfied:
            # Get operands
            left = self.registers[instr.reg_src1].get()
            right = self.registers[instr.reg_src2].get() + instr.offset
            log.debug(f"Left: {left}, Right: {right}")

            # ALU opperation 
            result, new_cond = self.alu.exec(instr.op, left, right)
            log.debug(f"ALU result = {result}, New Condition = {new_cond}")
        
            if instr.op == OpCode.STORE:
                # Store reg_target into memory at address
                self.memory.put(result, self.registers[instr.reg_target].get())
            elif instr.op == OpCode.LOAD:
                # Load value from memory at result address into reg_target
                val = self.memory.get(result)
                self.registers[instr.reg_target].put(val)
                if val == 0:
                    self.condition = CondFlag.Z
                elif val < 0:
                    self.condition = CondFlag.M
                else:
                    self.condition = CondFlag.P
            elif instr.op == OpCode.HALT:
                self.halted = True
                log.debug("HALT: CPU halted")
            elif instr.op in {OpCode.ADD, OpCode.SUB, OpCode.MUL, OpCode.DIV}:
                # Arithmetic operations
                self.registers[instr.reg_target].put(result)
                self.condition = new_cond

        # Finally increment PC if instruction didn’t modify it
        if instr.reg_target != 15 and instr.op != OpCode.HALT:
            self.registers[15].put(instr_addr + 1)
            log.debug(f"PC incremented to {self.registers[15].get()}")

    def run(self, from_addr=0,  single_step=False) -> None:
        """Step the CPU until it executes a HALT"""
        self.halted = False
        self.registers[15].put(from_addr)
        step_count = 0
        while not self.halted:
            if single_step:
                input(f"Step {step_count}; press enter")
            self.step()
            step_count += 1