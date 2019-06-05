import sys

A_COMMAND = 1
C_COMMAND = 2
L_COMMAND = 3


class SymbolTable(object):
    def __init__(self):
        self.symbol_table = {
            "R0":0,
            "R1":1,
            "R2":2,
            "R3":3,
            "R4":4,
            "R5":5,
            "R6":6,
            "R7":7,
            "R8":8,
            "R9":9,
            "R10":10,
            "R11":11,
            "R12":12,
            "R13":13,
            "R14":14,
            "R15":15,
            "SCREEN":16384,
            "KBD":24576,
            "SP":0,
            "LCL":1,
            "ARG":2,
            "THIS":3,
            "THAT":4
        }

    def addEntry(self,symbol,address):
        if not self.contains(symbol):
            self.symbol_table[symbol] = address

    def contains(self,symbol):
        return symbol in self.symbol_table

    def getAddress(self,symbol):
        return self.symbol_table.get(symbol,-1)

    def __repr__(self):
        return str(self.symbol_table)



class Code(object):
    def __init__(self):
        self.dest_table = {
        "None": "000",
        "M": "001",
        "D": "010",
        "MD": "011",
        "A":"100",
        "AM": "101",
        "AD": "110",
        "AMD":"111"
        }

        self.comp_table = {
            "0": "0101010",
            "1": "0111111",
            "-1": "0111010",
            "D":  "0001100",
            "A":  "0110000",
            "!D": "0001101",
            "!A": "0110001",
            "-D": "0001111",
            "-A": "0110011",
            "D+1": "0011111",
            "A+1": "0110111",
            "D-1": "0001110",
            "A-1": "0110010",
            "D+A": "0000010",
            "D-A": "0010011",
            "A-D": "0000111",
            "D&A": "0000000",
            "D|A": "0010101",
            "M":   "1110000",
            "!M":  "1110001",
            "-M":  "1110011",
            "M+1": "1110111",
            "M-1": "1110010",
            "D+M": "1000010",
            "D-M": "1010011",
            "M-D": "1000111",
            "D&M": "1000000",
            "D|M": "1010101"
        }

        self.jump_table = {
            "None": "000",
            "JGT" : "001",
            "JEQ" : "010",
            "JGE" : "011",
            "JLT" : "100",
            "JNE" : "101",
            "JLE" : "110",
            "JMP" : "111"
        }


    def comp(self,mnemonic):
        if mnemonic in self.comp_table:
            return self.comp_table[mnemonic]
        else:
            print(mnemonic)
            print("error finding when code comp")

    def dest(self,mnemonic):
        if mnemonic in self.dest_table:
            return self.dest_table[mnemonic]
        else:
            print("error finding when code dest")

    def jump(self,mnemonic):
        if mnemonic in self.jump_table:
            return self.jump_table[mnemonic]
        else:
            print("error finding when code jump")


class Parser(object):

    def __init__(self, filename):
        self.file = open(filename,"r")
        self.current_command = None


    def __uncomment__(self):
        index = self.current_command.find("//")
        if index != -1:
            self.current_command = self.current_command[:index]

    def hasMoreCommands(self):
        line = self.file.readline()
        if line:
            self.current_command = line
            return True
        else:
            return False


    def advance(self):
        if self.hasMoreCommands():
            self.current_command = self.current_command.strip()
            self.__uncomment__()
            if self.current_command == "":
                self.advance()
            return self.current_command
        else:
            return None


    def commandType(self):
        if self.current_command.startswith("@"):
            return A_COMMAND
        elif self.current_command.startswith("("):
            return L_COMMAND
        else:
            return C_COMMAND


    def symbol(self):
        if self.commandType() == A_COMMAND:
            return self.current_command[1:]
        elif self.commandType() == L_COMMAND:
            return self.current_command[1:-1]

    def dest(self):
        # dest = comp ; jump
        if self.commandType() == C_COMMAND:
            if "=" in self.current_command:
                return self.current_command.split("=")[0]
            else:
                return "None"
        else:
            raise("error find in dest in parser")



    def comp(self):
        if self.commandType() == C_COMMAND:
            result = ""
            if "=" in self.current_command and ";" in self.current_command:
                result = self.current_command.split("=")[1].strip()
                result = result.split(";")[0].strip()
            elif "=" in self.current_command:
                result = self.current_command.split("=")[1].strip()
            elif ";" in self.current_command:
                result = self.current_command.split(";")[0].strip()
            return result
        else:
            raise("error find in comp in parser")

    def jump(self):
        if self.commandType() == C_COMMAND:
            if ";" in self.current_command:
                return self.current_command.split(";")[-1].strip()
            else:
                return "None"
        else:
            raise("error find in jump in parser")
           


def main(file):
    symbol_table = SymbolTable()
    coder = Code()


    output_file = open(file.split(".")[0]+"."+"hack","w")

    parser = Parser(file)
    command_index = 0
    while True:
        current_command = parser.advance()
        if not current_command:
            break
        # print(current_command)
        if parser.commandType() == L_COMMAND:
            symbol_table.addEntry(parser.symbol(),command_index)
            continue

        command_index+=1


    parser = Parser(file)
    command_index = 16

    while True:
        current_command = parser.advance()
        if not current_command:
            break
        # print(current_command)
        if parser.commandType() == A_COMMAND:
            symbol = parser.symbol()
            if symbol_table.contains(symbol):
                address = symbol_table.getAddress(symbol)
            else:
                if symbol.isdigit():
                    address = int(symbol)
                else:
                    symbol_table.addEntry(symbol,command_index)
                    address = command_index
                    command_index += 1

            # print("{:0>16b}".format(address))
            output_file.write("{:0>16b}\n".format(address))

        elif parser.commandType() ==  C_COMMAND:   

            c=parser.comp()
            d=parser.dest()
            j=parser.jump()

            # print(c)
            # print(d)
            # print(j)

            cc = coder.comp(c)
            dd = coder.dest(d)
            jj = coder.jump(j)

            # print(cc)
            # print(dd)
            # print(jj)


            # print("111" + cc + dd + jj)
            output_file.write("111" + cc + dd + jj + "\n")
    


    
if __name__ == '__main__':
    file = sys.argv[1]
    main(file)



    






            



