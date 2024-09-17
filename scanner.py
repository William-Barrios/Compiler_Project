
import re

class TokenType:
    IDENTIFIER = 'IDENTIFIER'
    INTEGER = 'INTEGER'
    ASSIGN_OP = 'ASSIGN_OP'
    ADD_OP = 'ADD_OP'
    OR_LOG = 'OR_LOG'
    SUB_OP = 'SUB_OP'
    MULT = 'MULT'
    DIV = 'DIV'
    PRINT_KEY = 'PRINT_KEY'
    OPEN_PAR = 'OPEN_PAR'
    OPEN_CHE = 'OPEN_CHE'
    CLOSE_PAR = 'CLOSE_PAR'
    CLOSE_CHE = 'CLOSE_CHE'
    EOP = 'EOP'
    KEYS_O = 'KEYS_O'
    KEYS_C = 'KEYS_'
    POW = 'POW'
    FIN_L = 'FIN_L'
    INCR_OP = 'INCR_OP'
    DECR_OP = 'DECR_OP'
    UNKNOWN = 'UNKNOWN'
    COMMENT = 'COMMENT'
    ARRAY_D = "ARRAY_D"
    BOOL_D = 'BOOL_D'
    CHAR_D ='CHAR_D'
    ELSE_D = 'ELSE_D'
    FALSE_D = 'FALSE_D'
    FOR_D = 'FOR_D'
    MOD = 'MOD'
    DECLA_OP = 'DECLA_OP'
    STRING_D = 'STRING'
    TRUE_D = 'TRUE'
    VOID_D = 'VOID'
    IF_D = 'IF'
    RETURN_D = 'RETURN'
    WHILE_D = 'WHILE'
    FUNCTION_D = 'FUNCTION'
    COMPARE_OP = 'COMPARE_OP'
    DIFF_OP = 'DIFF_OP'
    NEG_OP = 'NEG_OP'
    ANDLOG = 'ANDLOG'
    MINOR_OP = 'MINOR_OP'
    MINOREQ_OP = 'MINOREQ_OP'
    GREAT_OP = 'GREAT_OP'
    GREATEQ_OP = 'GREATEQ_OP'
    COMA = "COMA"

class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column


current_char = None
current_line = 1
current_column = 0
file_content = None
file_index = 0


keywords = {
    "array": TokenType.ARRAY_D,
    "boolean": TokenType.BOOL_D,
    "char": TokenType.CHAR_D,
    "else": TokenType.ELSE_D,
    "false": TokenType.FALSE_D,
    "for": TokenType.FOR_D,
    "function":TokenType.FUNCTION_D,
    "if": TokenType.IF_D,
    "integer": TokenType.INTEGER,
    "print": TokenType.PRINT_KEY,
    "return": TokenType.RETURN_D,
    "string": TokenType.STRING_D,
    "true": TokenType.TRUE_D,
    "void": TokenType.VOID_D,
    "while": TokenType.WHILE_D
}

def is_keyword(word):
    return word in keywords


def getchar():
    global file_index, current_char, current_line, current_column
    if file_index < len(file_content):
        current_char = file_content[file_index]
        file_index += 1
        current_column += 1
        if current_char == '\n':
            current_line += 1
            current_column = 0
        return current_char
    return None


def peekchar():
    if file_index < len(file_content):
        return file_content[file_index]
    return None


def skip_single_line_comment():
    while getchar() != '\n' and current_char is not None:
        continue


def skip_multi_line_comment():
    getchar()  
    while True:
        if getchar() == '*' and peekchar() == '/':
            getchar() 
            break
        elif current_char is None:
            print("ERROR SCAN - Unclosed multi-line comment")
            break

# Function to get the next token
def get_token():
    token = None
    while getchar() is not None:
        if current_char.isspace():
            continue  
        elif current_char.isalpha():  
            start_column = current_column
            identifier = current_char
            while peekchar() and (peekchar().isalnum() or peekchar() == '_'):
                identifier += getchar()

            if is_keyword(identifier):
                key_identifier = keywords[identifier]
                token = Token(key_identifier, identifier, current_line, start_column)
                print(f"DEBUG SCAN - KEYWORD [ {identifier} ] of type [{key_identifier}] found at ({current_line}:{start_column})")
                
            else:
                token = Token(TokenType.IDENTIFIER, identifier, current_line, start_column)
                print(f"DEBUG SCAN - IDENTIFIER [ {identifier} ] found at ({current_line}:{start_column})")
        elif current_char.isdigit():  # Check for integers
            start_column = current_column
            number = current_char
            while peekchar() and peekchar().isdigit():
                number += getchar()
            token = Token(TokenType.INTEGER, number, current_line, start_column)
            print(f"DEBUG SCAN - INTEGER [ {number} ] found at ({current_line}:{start_column})")
        elif current_char == '=':
            if peekchar() == '=':
                token = Token(TokenType.COMPARE_OP, '==', current_line, current_column)
                print(f"DEBUG SCAN - COMPARE_OP [ == ] found at ({current_line}:{current_column})")
                getchar()

            else:
                token = Token(TokenType.ASSIGN_OP, '=', current_line, current_column)
                print(f"DEBUG SCAN - ASSIGN_OP [ = ] found at ({current_line}:{current_column})")
        elif current_char == '+':
            if peekchar() == '+':
                token = Token(TokenType.INCR_OP, '++', current_line, current_column)
                print(f"DEBUG SCAN - INCR_OP [ ++ ] found at ({current_line}:{current_column})")
                getchar()
            else:   
                token = Token(TokenType.ADD_OP, '+', current_line, current_column)
                print(f"DEBUG SCAN - ADD_OP [ + ] found at ({current_line}:{current_column})")
        elif current_char == '-':
            if peekchar() == '-':
                token = Token(TokenType.DECR_OP, '--', current_line, current_column)
                print(f"DEBUG SCAN - DECR_OP [ -- ] found at ({current_line}:{current_column})")
                getchar()
            else:
                token = Token(TokenType.SUB_OP, '-', current_line, current_column)
                print(f"DEBUG SCAN - SUB_OP [ - ] found at ({current_line}:{current_column})")
        elif current_char == '(':
            token = Token(TokenType.OPEN_PAR, '(', current_line, current_column)
            print(f"DEBUG SCAN - OPEN_PAR [ ( ] found at ({current_line}:{current_column})")

        elif current_char == '^':
            token = Token(TokenType.POW, '^', current_line, current_column)
            print(f"DEBUG SCAN - POW [ ^ ] found at ({current_line}:{current_column})")
        elif current_char == '"':
            start_column = current_column
            string_value=current_char
            while True:
                #next_char = getchar()
                if peekchar() == None:
                    print(f"ERROR SCAN - Unclosed string starting at ({current_line}:{start_column})")
                    return Token(TokenType.UNKNOWN, string_value, current_line, start_column)
                if peekchar() == '"':  # String end detected
                    token = Token(TokenType.STRING_D, string_value, current_line, start_column)
                    string_value += getchar()
                    print(f"DEBUG SCAN - STRING [ {string_value} ] found at ({current_line}:{start_column})")
                    break
                string_value += getchar()
        elif current_char == '%':
            token = Token(TokenType.MOD, '%', current_line, current_column)
            print(f"DEBUG SCAN - MOD [ % ] found at ({current_line}:{current_column})")
        elif current_char == ':':
            token = Token(TokenType.DECLA_OP, ':', current_line, current_column)
            print(f"DEBUG SCAN - DECLA_OP [ : ] found at ({current_line}:{current_column})")
        elif current_char == '{':
            token = Token(TokenType.KEYS_C, '{', current_line, current_column)
            print("DEBUG SCAN - KEYS_O [" + " { ] found at",end=' ')
            print(f"({current_line}:{current_column})")
        elif current_char == '}':
            token = Token(TokenType.KEYS_O, '}', current_line, current_column)
            print("DEBUG SCAN - KEYS_O [" + " } ] found at",end=' ')
            print(f"({current_line}:{current_column})")

        elif current_char == ',':
            token = Token(TokenType.COMA, ',', current_line, current_column)
            print(f"DEBUG SCAN - COMA [ , ] found at ({current_line}:{current_column})")
        elif current_char == ';':
            token = Token(TokenType.FIN_L, ';', current_line, current_column)
            print(f"DEBUG SCAN - FIN_L [ ; ] found at ({current_line}:{current_column})")
        elif current_char == "'":
            token = Token(TokenType.CHAR_D, "'", current_line, current_column)
            print(f"DEBUG SCAN - CHAR_D [ ' ] found at ({current_line}:{current_column})")
        elif current_char == '!':
            if peekchar()== '=':
                token = Token(TokenType.DIFF_OP, '!=', current_line, current_column)
                print(f"DEBUG SCAN - DIFF_OP [!=] found at ({current_line}:{current_column})")
                getchar()
            else:
                token = Token(TokenType.NEG_OP, '!', current_line, current_column)
                print(f"DEBUG SCAN - NEG_OP [ ! ] found at ({current_line}:{current_column})")
        elif current_char == '|':
            if peekchar()== '|':
                token = Token(TokenType.OR_LOG, '||', current_line, current_column)
                print(f"DEBUG SCAN - OR_LOG [||] found at ({current_line}:{current_column})")
                getchar()
        elif current_char == ')':
            token = Token(TokenType.CLOSE_PAR, ')', current_line, current_column)
            print(f"DEBUG SCAN - CLOSE_PAR [ ) ] found at ({current_line}:{current_column})")
        elif current_char == '[':
            token = Token(TokenType.OPEN_CHE, '[', current_line, current_column)
            print(f"DEBUG SCAN - OPEN_CHE [ [ ] found at ({current_line}:{current_column})")
        elif current_char == ']':
            token = Token(TokenType.CLOSE_CHE, ']', current_line, current_column)
            print(f"DEBUG SCAN - CLOSE_CHE [ ] ] found at ({current_line}:{current_column})")
        elif current_char == '*':
            token = Token(TokenType.MULT, '*', current_line, current_column)
            print(f"DEBUG SCAN - MULT [ * ] found at ({current_line}:{current_column})")
        elif current_char == '$':
            token = Token(TokenType.EOP, '$', current_line, current_column)
            print(f"DEBUG SCAN - EOP [ $ ] found at ({current_line}:{current_column})")
        elif current_char == '/':
            if peekchar() == '/':  # Single-line comment
                skip_single_line_comment()
            elif peekchar() == '*':  # Multi-line comment
                skip_multi_line_comment()
            else:
                token = Token(TokenType.DIV, '/', current_line, current_column)
                print(f"DEBUG SCAN - DIV [ / ] found at ({current_line}:{current_column})")
        elif current_char == '<':
            if peekchar()== '=':
                token = Token(TokenType.MINOREQ_OP, '<=', current_line, current_column)
                print(f"DEBUG SCAN - MINOREQ_OP [<=] found at ({current_line}:{current_column})")
                getchar()
            else:
                token = Token(TokenType.MINOR_OP, '<', current_line, current_column)
                print(f"DEBUG SCAN - MINOR_OP [ < ] found at ({current_line}:{current_column})")
        elif current_char == '>':
            if peekchar()== '=':
                token = Token(TokenType.GREATEQ_OP, '>=', current_line, current_column)
                print(f"DEBUG SCAN - MINOREQ_OP [>=] found at ({current_line}:{current_column})")
                getchar()
            else:
                token = Token(TokenType.GREAT_OP, '<', current_line, current_column)
                print(f"DEBUG SCAN - GREAT_OP [ < ] found at ({current_line}:{current_column})")
        elif current_char == '&':
            if peekchar()== '&':
                token = Token(TokenType.ANDLOG, '&&', current_line, current_column)
                print(f"DEBUG SCAN - ANDLOG [&&] found at ({current_line}:{current_column})")
                getchar()
            else:
                token = Token(TokenType.UNKNOWN, '&', current_line, current_column)
                print(f"DEBUG SCAN - UNKNOWN [ & ] found at ({current_line}:{current_column})")
        else:
            token = Token(TokenType.UNKNOWN, current_char, current_line, current_column)
            print(f"ERROR SCAN - Unknown token [ {current_char} ] at ({current_line}:{current_column})")
        
        if token:
            return token
    return None

# Function to scan a file
def scan_file(filename):
    global file_content, file_index
    with open(filename, 'r') as f:
        file_content = f.read()
    
    file_index = 0
    tokens_list = []
    while peekchar() is not None:
        tokens_list.append(get_token())
    print("holis")

    


scan_file('main.txt')


