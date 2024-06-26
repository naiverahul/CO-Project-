
from encoding import *
from function import *
from helper import *
import sys
# from Assembler import *
input_file = sys.argv[0]
output_file = sys.argv[1]
res1= open(input_file, 'r')
test1 = open(output_file ,'w')
line = res1.readlines()

# lin = []
# print(lin)
# for i in line:
#     lin.append(i.split())
#     print(i)

regis_value = {
    "prog"  : "00000000000000000000000000000000",
    "00000" : "00000000000000000000000000000000",
    "00001" : "00000000000000000000000000000000",
    "00010" : "00000000000000000000000000000000",
    "00011" : "00000000000000000000000000000000",
    "00100" : "00000000000000000000000000000000",
    "00101" : "00000000000000000000000000000000",
    "00110" : "00000000000000000000000000000000",
    "00111" : "00000000000000000000000000000000",
    "01000" : "00000000000000000000000000000000",
    "01001" : "00000000000000000000000000000000",
    "01010" : "00000000000000000000000000000000",
    "01011" : "00000000000000000000000000000000",
    "01100" : "00000000000000000000000000000000",
    "01101" : "00000000000000000000000000000000",
    "01110" : "00000000000000000000000000000000",
    "01111" : "00000000000000000000000000000000",
    "10000" : "00000000000000000000000000000000",
    "10001" : "00000000000000000000000000000000",
    "10010" : "00000000000000000000000000000000",
    "10011" : "00000000000000000000000000000000",
    "10100" : "00000000000000000000000000000000",
    "10101" : "00000000000000000000000000000000",
    "10110" : "00000000000000000000000000000000",
    "10111" : "00000000000000000000000000000000",
    "11000" : "00000000000000000000000000000000",
    "11001" : "00000000000000000000000000000000",
    "11010" : "00000000000000000000000000000000",
    "11011" : "00000000000000000000000000000000",
    "11100" : "00000000000000000000000000000000",
    "11101" : "00000000000000000000000000000000",
    "11110" : "00000000000000000000000000000000",
    "11111" : "00000000000000000000000000000000"
}

mem = ["0b00000000000000000000000000000000"]

mem_count = {}

@staticmethod
def type_of_ins(instruction):
    type_dict = {
        "R": ["0110011"],
        "I": ["0000011","0010011","0010011","1100111"],
        "S": ["0100011"],
        "B": ["1100011"],
        "U": ["0010111", "0110111"],
        "J": ["1101111"],
        #"BONUS": ["mull", "rst", "halt", "rvrs"]
    }
    for key,values in type_dict.items():
        for j in values:
            if j == instruction:
                return key



def prog_count(pc):
    pc_decimal = int(pc,2)
    pc_decimal = pc_decimal + 4
    pc_bin = registers.sext_binary_U(pc_decimal)
    return pc_bin

pc = 0
prog_track = []
while pc< 4 * len(line):
    
    i = line[int(pc/4)]
    if i == "00000000000000000000000001100011" :
        break
    opcode = i[-7:]
    type_ins = type_of_ins(opcode)
    if type_ins == "R":
        rs2 = i[-25:-20]
        rs1 = i[-20:-15]
        rd =  i[-12:-7]
        rs1_value = regis_value[rs1]
        rs2_value = regis_value[rs2]
        rd_value = regis_value[rd]
        func3 = i[-15:-12]
        func7 = i[-32:-25]
        if func3 == "000":
            if func7 == "0100000":
                rd_value = function.sub(rd_value,rs1_value,rs2_value)
                regis_value[rd] = rd_value
            else:
                rd_value = function.add(rd_value,rs1_value, rs2_value)
                regis_value[rd] = rd_value
        elif func3 == "001":
            rd_value = function.sll(rd_value,rs1_value, rs2_value)
            regis_value[rd] = rd_value
        elif func3 == "010":
            rd_value = function.slt(rd_value, rs1_value, rs2_value)
            regis_value[rd] = rd_value
        elif func3 == "011":
            rd_value = function.sltu(rd_value, rs1_value, rs2_value)
            regis_value[rd] = rd_value
        elif func3 == "100":
            rd_value = function.xor(rd_value, rs1_value, rs2_value)
            regis_value[rd] = rd_value
        elif func3 == "101":
            rd_value = function.srl(rd_value, rs1_value, rs2_value)
            regis_value[rd] = rd_value
        elif func3 == "110":
            rd_value = function.bitwise_or(rd_value, rs1_value, rs2_value)
            regis_value[rd] = rd_value
        elif func3 == "111":
            rd_value = function.bitwise_and(rd_value, rs1_value, rs2_value)
            regis_value[rd] = rd_value
        pc_bin = prog_count(regis_value["prog"])
        regis_value["prog"] = pc_bin
    elif type_ins == "I":
        rd = i[-12:-7]
        rs1 = i[-20:-15]
        imm = i[-32:-20]
        func3 = i[-15:-12]
        rd_value = regis_value[rd]
        rs1_value = regis_value[rs1]
        if opcode == "1100111":
            rd_value = function.jalr(rs1_value, imm,prog,rd_value)[0]
            prog_value = function.jalr(rs1_value, imm,prog,rd_value)[1]
            regis_value[rd] = rd_value
            regis_value["prog"] = prog_value
            # prog_track.append(int(int(regis_value["prog"],2)))
        elif opcode == "0010011":
            if func3 == "000":
                rd_value = function.addi(imm,rs1_value)
                regis_value[rd] = rd_value
                pc_bin = prog_count(regis_value["prog"])
                regis_value["prog"] = pc_bin
            elif func3 =="011":
                rd_value = function.stliu(imm, rs1_value,rd_value)
                regis_value[rd] = rd_value
                pc_bin = prog_count(regis_value["prog"])
                regis_value["prog"] = pc_bin
        elif opcode == "0000011":
            if func3 == "010":
                rd_value = function.lw(imm,rs1_value)
                regis_value[rd] = rd_value
                pc_bin = prog_count(regis_value["prog"])
                regis_value["prog"] = pc_bin

    elif type_ins =="S":
        rs1 = i[-20:-15]
        rs2 = i[-25:-20]
        imm = i[-32:-25] + i[-12:-7]
        rs1_value = regis_value[rs1]
        rd_value = function.sw(rs1_value,imm)
        regis_value[rs2] = rd_value
        mem[0] = "0b" + rd_value
        pc_bin = prog_count(regis_value["prog"])
        regis_value["prog"] = pc_bin

    elif type_ins == "U":
        imm = i[-32:-12]
        rd = i[-12:-7]
        if opcode  == "0110111":
            rd_value = function.lui(imm,prog)
            regis_value[rd] = rd_value
            pc_bin = prog_count(regis_value["prog"])
            regis_value["prog"] = pc_bin
        else:
            rd_value = function.auipc(imm,prog)
            regis_value[rd] = rd_value
            pc_bin = prog_count(regis_value["prog"])
            regis_value["prog"] = pc_bin

    elif type_ins == "B":
        prog = int(regis_value["prog"],2)
        rs1 = i[-20:-15]
        rs2 = i[-25:-20]
        imm1 = i[-32:-25]+i[-12:-7]
        imm = imm1[-12] +imm1[-1] + imm1[-11:-5] + imm1[-5:-1] + "0"
        func3 = i[-15:-12]
        rs1_value = regis_value[rs1]
        rs2_value = regis_value[rs2]
        if func3 == "000":
            prog_value = function.beq(rs2_value,rs1_value,imm,prog)
            regis_value["prog"] =prog_value
            # prog_track.append(int(int(regis_value["prog"],2)))
            # i = lin[int(int(prog_value,2)/4)]
        elif func3 == "001":
            prog_value = function.bne(rs2_value,rs1_value,imm,prog)
            regis_value["prog"] =prog_value
            # prog_track.append(int(int(regis_value["prog"],2)))
            # i = lin[int(int(prog_value,2)/4)]
        elif func3 == "100":
            prog_value = function.blt(rs2_value,rs1_value,imm,prog)
            regis_value["prog"] =prog_value
            # prog_track.append(int(int(regis_value["prog"],2)))
            # i = lin[int(int(prog_value,2)/4)]
        elif func3 == "101":
            prog_value = function.bge(rs2_value,rs1_value,imm,prog)
            regis_value["prog"] =prog_value
            # prog_track.append(int(int(regis_value["prog"],2)))
            # i = lin[int(int(prog_value,2)/4)]
        elif func3 == "110":
            prog_value = function.bltu(rs2_value,rs1_value,imm,prog)
            regis_value["prog"] =prog_value
            # prog_track.append(int(int(regis_value["prog"],2)))
            # i = lin[int(int(prog_value,2)/4)]
        elif func3 == "111":
            prog_value = function.bgeu(rs2_value,rs1_value,imm,prog)
            regis_value["prog"] =prog_value
            # prog_track.append(int(int(regis_value["prog"],2)))
            # i = lin[int(int(prog_value,2)/4)]
        # pc = int(int(prog_value,2)/4)
        # print(pc)
    elif type_ins == "J":
        rd = i[-12:-7]
        imm1 = i[-32:-12]
        imm = imm1[-20]+imm1[-8:]+imm1[-9]+imm1[-19:-9]
        prog = int(regis_value["prog"],2)
        rd_value = regis_value[rd]
        rd_value1 = function.jal(rd_value,prog,imm)[0]
        prog_value = function.jal(rd_value,prog,imm)[1]
        regis_value[rd] = rd_value1
        regis_value["prog"] = prog_value
        # prog_track.append(int(int(regis_value["prog"],2)))
        # i = lin[int(int(prog_value,2)/4)]
        # pc = int(int(prog_value,2)/4)
        # print(pc)

    pc = int(int(regis_value["prog"],2))
    pc_hex = format(pc+4096,'08X')

    mem_count[pc_hex] =  mem[0]
    # print(pc)
    # pc = pc+1
    # print(regis_value["prog"])
    test1.write(" ".join(["0b" + value for value in regis_value.values()]))
    # print(pc)

for key,value in mem_count.items():
    test1.write(key, ":",value)

















