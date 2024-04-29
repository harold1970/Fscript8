import sys
"""
define syntax
new [name] [value]: create new variable
load [name] [value]: add new data to a variable
add [variable 3] [variable 1] [variable 2]: adds two variables and stores it in third 
sub [variable 3] [variable 1] [variable 2]: subs two variables and stores it in third 
div [variable 3] [variable 1] [variable 2]: divs two variables and stores it in third 
mul [variable 3] [variable 1] [variable 2]: muls two variables and stores it in third 
if [variable 1] [operator] [variable 2] [label]: performs the operator on the first and second variable
print [variable 1]: print value to out
mov [variable 1] -> [variable 2]: move a variable to a differant variable
get [variable]: get user input from keyboard
push [variable 1] [location]: push a value on stack
pull [variable 1] [location]: pull a value off stack
ptr new [name] [variable 2]: creates a pointer to a location at were a variable is stored
_ [name]: create a label at a location in your script
return: ends the script
"""

filename = sys.argv[1]
with open(filename, 'r') as rawFile:
    rawFile = rawFile.read()
    cleanFile = rawFile.replace('\n', '')
    
class UserVar:
    def __init__(self, name, ptr, val=None):
        self.Name = name
        self._value = val
        self.ptr = ptr


lines = cleanFile.split(';')
commands = ['new', 'load', 'add', 'sub', 'div', 'mul', 'if', 'print', 'mov', 'get', 'push', 'pull', 'ptr', '_']
userVars = {}
compiledScript = []
emptySpace = 0
labels = {}
pc = 0  
for line in lines:
    # line = line.lower()
    components = line.split(" ")
    print(components)
    if components[0] == 'new':
        userVars[components[1]] = UserVar(components[1], int(components[2]), emptySpace)
        compiledScript.append(f'lda {int(components[2])};')
        compiledScript.append(f'mov a r0;')
        compiledScript.append(f'mov *{emptySpace} r0;')
        emptySpace += 1
    if components[0] == 'add':
        userVars[components[1]]._value = userVars[components[2]]._value + userVars[components[3]]._value
        compiledScript.append(f"mov *{userVars[components[1]].ptr} a;")
        compiledScript.append(f"mov *{userVars[components[1]].ptr} r1;")
        compiledScript.append("add r1;")
        compiledScript.append(f"mov r0 *{userVars[components[1]].ptr};")
    if components[0] == '_':
        labels.update({components[1] : pc})
        compiledScript.append(f'_ {components[1]};')
        compiledScript.append('mov ')
    pc += 1

    if components[0] == 'return':
        compiledScript.append('hlt;')
print('_____ compiled Script _____')
for i in compiledScript:
    print(i)
print('_____ end of compiled script _____')