import sys

"""
00: NOP - Nothing
01: HLT - Halt program
02: OUT [id] - Output the accumulator out of an output
03: LDI A, [d8] - Loads immediate 8 bit word into the accumulator
04: MOV [r], A - Move register to accumulator
05: MOV A, [r] - Move accumulator to register
06: INC [r] - Increment a register
07: DEC [r] - Decrememt a register
08: ADD [r], A - Add the accumulator from a register
09: SUB [r], A - Subtract the accumulator from a register
0A: AND [r], A - And the register and accumulator
0B: IOR [r], A - OR the register and accumulator
0C: XOR [r], A - XOR the register and accumulator
0D: NOT [r] - NOT a register
0E: SAR [d8] - Barrel shift accumulator right
0F: SAL [d8] - Barrel shift accumulator left
10: JUP [d8] - Jump to a location
11: JPP [r] - Jump to a register value
12: JPL A, [d8] - Jump if accumulator is less than 0
13: JZO A, [d8] - Jump if accumulator is 0
14: JPG A, [d8] - Jump if accumulator is greater than 0
15: JLE A, [d8] - Jump if accumulator is less than or equal to 0
16: JGE A, [d8] Jump if accumulator is greater than or equal to 0
17: JNZ A, [d8] Jump if accumulator is not 0
18: CLR [r] - Clear a register
19: INP [id] - Store INPUT id in accumulator
1A: MOV pA, [r] - Move the value at address A register r
1B: MOV [r], pA - Move register r into address A
1C: MOV [p], A - Move a value in a pointer to the accumulator
1D: MOV A, [p] - Move the accumulator to a location
1E: MLT [r], A - Multiply register r by the accumulator
1F: DIV [r], A - Divide register r by accumulator
"""


def help():
	print('00: NOP - Nothing')
	print('01: HLT - Halt program')
	print('02: OUT [id] - Output the accumulator out of an output')
	print("03: LDI A, [d8] - Loads immediate 8 bit word into the accumulator (just use lda [d8])")
	print('04: MOV [r], A - Move register to accumulator')
	print('05: MOV A, [r] - Move accumulator to register')
	print('06: INC [r] - Increment a register')
	print('07: DEC [r] - Decrememt a register')
	print('08: ADD [r], A - Add the accumulator from a register')
	print('09: SUB [r], A - Subtract the accumulator from a register')
	print('0A: AND [r], A - And the register and accumulator')
	print('0B: IOR [r], A - OR the register and accumulator')
	print('0C: XOR [r], A - XOR the register and accumulator')
	print('0D: NOT [r] - NOT a register')
	print('0E: SAR [d8] - Barrel shift accumulator right')
	print('0F: SAL [d8] - Barrel shift accumulator left')
	print('10: JUP [d8] - Jump to a location')
	print('11: JPP [r] - Jump to a register value')
	print('12: JPL A, [d8] - Jump if accumulator is less than 0')	
	print('13: JZO A, [d8] - Jump if accumulator is 0')
	print('14: JPG A, [d8] - Jump if accumulator is greater than 0')
	print('15: JLE A, [d8] - Jump if accumulator is less than or equal to 0')
	print('16: JGE A, [d8] Jump if accumulator is greater than or equal to 0')
	print('17: JNZ A, [d8] Jump if accumulator is not 0')
	print('18: CLR [r] - Clear a register')
	print('19: INP [id] - Store INPUT id in accumulator')
	print('1A: MOV pA, [r] - Move the value at address A register r')
	print('1B: MOV [r], pA - Move register r into address A')
	print('1C: MOV [p], A - Move a value in a pointer to the accumulator') #
	print('1D: MOV A, [p] - Move the accumulator to a location') 
	print('1E: MLT [r], A - Multiply register r by the accumulator')
	print('1F: DIV [r], A - Divide register r by accumulator')
	print("type 'compile' to compile your scripts, else type 'help' to see the commands.")
	
	
def getRegister(register):
	if register == 'r0':
		return '0'
	if register == 'r1':
		return '1'
	if register == 'r2':
		return '2'
	if register == 'r3':
		return '3'
	else:
		print("register not found")
		return False

size = 0
pc = 0
commands = ['hlt', 'out', 'lda', 'mov', 'inc', 'dec', 'add', 'sub', 'and', 'ior', 'xor', 'not', 'sar', 'sal', 'jup', 'jpp', 'jpl','jzo','jpg','jle','jge','jnz','_', 'exit', 'help','//','']
script = []

filename = sys.argv[1]
output = sys.argv[2]
with open(filename, 'r') as rawFile:
	rawFile = rawFile.read()
	cleanFile = rawFile.replace('\n', '')

print("type 'help' for list of commands and uses")

while True:
	userInput  = input("> ")
	if userInput == 'help':
		help()
	elif userInput == 'compile':
		break
	elif userInput == 'cancel':
		exit()

labelCounter = 0
lines = cleanFile.split(";")
labels = {}

for line in lines:
	line = line.lower()
	components = line.split(" ")
	if components[0] == '_':
		labels.update({components[1] : pc})
	pc += 1		

for line in lines:
	line = line.lower()
	components = line.split(" ")

	print(components)
	if components[0] not in commands:
		print(f'unknown memonic {components[0]}')
	else:
		

		if components[0] == 'hlt':
			script.append('1')
			size += 8		
		
		if components[0] == 'out': 
			script.append(f'2 {components[1]}')
			size += 16		
		
		if components[0] == 'lda':
			if int(components[1]) > 255:
				print('value to large will cause overflow max(255)')
			else:
				script.append(f'3 {components[1]}')
			size += 16		
		
		if components[0] == 'mov':
			moveTo = components[1]
			moveFrom = components[2] 
			
			if moveTo == 'a':
				r = getRegister(components[2])
				script.append(f'5 {r}')
			if moveFrom == '*a':
				script.append(f'26 {moveTo}')
			if moveTo == '*a':
				r = getRegister(moveFrom)
				script.append(f'27 {r}')
			if moveTo[0] == '*':
				script.append(f'28 {moveTo[1:]}')
			if moveFrom == 'a':
				r = getRegister(moveTo)
				script.append(f'29 {r}')
			if moveFrom == 'a' and moveTo == getRegister != False:
				r = getRegister(components[1])
				script.append(f'4 {r}')
			size += 16;	
		
		if components[0] == 'inc':
			r = getRegister(components[1])
			script.append(f'6 {r}')		
		
		if components[0] == 'dec':
			r = getRegister(components[1])
			script.append(f'7 {r}')
			size += 16		
		
		if components[0] == 'add':
			r = getRegister(components[1])
			script.append(f'8 {r}')
			size += 16			
		
		if components[0] == 'sub':
			r = getRegister(components[1])
			script.append(f'9 {r}')
			size += 16		
		
		if components[0] == 'and':
			r = getRegister(components[1])
			script.append(f'10 {r}')
			size += 16		
		
		if components[0] == 'ior':
			r = getRegister(components[1])
			script.append(f'11 {r}')
			size += 16		
		
		if components[0] == 'xor':
			r = getRegister(components[1])
			script.append(f'12 {r}')
			size += 16		
		
		if components[0] == 'not':
			r = getRegister(components[1])
			script.append(f'13 {r}')
			size += 16		
		
		if components[0] == 'sar':
			script.append(f'14 {components[1]}')
			size += 16
		
		if components[0] == 'sal':
			script.append(f'15 {components[1]}')
			size += 16
		
		if components[0] == 'jup':
			la = labels.get(components[1])
			la -= 1
			script.append(f'16 {la}')
		
		if components[0] == 'jpp':
			la = labels.get(components[1])
			la -= 1
			script.append(f'17 {la}')
		
		if components[0] == 'jpl':
			la = labels.get(components[1] )
			la -= 1
			script.append(f'18 {la}')
		
		if components[0] == 'jzo':
			la = labels.get(components[1] )
			la -= 1
			script.append(f'19 {la}')

		if components[0] == 'jpg':
			la = labels.get(components[1] )
			la -= 1
			script.append(f'20 {la}')

		if components[0] == 'jle':
			la = labels.get(components[1])
			la -= 1
			script.append(f'21 {la}')

		if components[0] == 'jge':
			la = labels.get(components[1] )
			la -= 1
			script.append(f'22 {la}')
		if components[0] == 'jnz':
			la = labels.get(components[1] )
			la -= 1
			script.append(f'23 {la}')
		if components[0] == 'clr':
			r = getRegister(components[1])	
			la -= 1 	
			script.append(f'24 {r}')
		if components[0] == 'inp':
			script.append(f'25 {components[1]}')
		
		if components[0] == 'mlt':
			r = getRegister(components[1])
			script.append(f'30 {r}')
		
		if components[0] == 'div':
			r = getRegister(components[1])
			script.append(f'31 {r}')
		
		if components[0] == 'help':
			help()
		if components[0] == 'exit':
			break
		if components[0] == '//':
			continue
	pc += 1



print("___ compiled script ___")

for i in script:
	print(i)

print("___ end of compiled script ___")

with open(output, "w") as file:
	for i in script:
		file.write(i + '\n')
	print(f"written to file: {output}")
print(f'script size: WIP')
