# Anton Stoytchev
# Implementing a Lexer for a CLite programming language
# Will be ivoked by a Parser to generate program trees

import re
import sys

#Singleton (Design Pattern). Only one object of the class is ever used.
class Lexer(object):
    
    #re expressions used for determining what the token is
    intlit     = re.compile("^\d+$") # Regular expression for one or more digits
    floatlit   = re.compile("^(\d+(\.\d+))$")
    keyword    = re.compile("^bool$|^else$|^false$|^if$|^true$|^float$|^int$|^main$|^while$|^print$") #Regular expression for one or more letters
    Ident      = re.compile("^[a-zA-Z]+\d*$|^[a-zA-Z]+_[a-zA-Z]+\d*$") #one or more letters fallowed by 0 or more digits
    whitespace = re.compile("\s+")
    
    #splitting the line by all valid characters
    Intlit      = "(^\d+\.?\d*$)|" #split on one or more digits
    WhiteSpace  = "\s+|" #split on one or more strings
    operators   = "([\+\-\*\/\<\>\=\!\%])|(\|\|)|(\&\&)|" #split on + - * / < > = | & ! %
    punctuation = "([\;,\,,\},\{,\(,\)])|"
    doublechars = "(########)|(#@#@#@#@)|(@#@#@#@#)|($@$@$@$@)|(@$@$@$@$)|(@@@@@@@@)"
    
    splitstring = Intlit + WhiteSpace + operators + punctuation + doublechars
    
    splitpatt   = re.compile(splitstring)
    
    #Static Variables in Python
    TokenDefInt = {
                'EOF':0, 'ID':1, 'INTLIT':2, 'FLOATLIT':3, 'BOOL':4, 'ELSE':5, 'IF':6, 'MAIN':7, 'WHILE':8,
                'PLUS':9, 'MINUS':10, 'OR':11, 'AND':12, 'EQUAL':13, 'NOT_EQUAL':14, 'LESS':15, 'GREATER':16,
                'LESS_OR_EQUAL':17, 'GREATER_OR_EQUAL':18, 'MULT':19, 'DIV':20, 'MOD':21, 'BANG':22,
                'ASSIGNMENT':23, 'SEMI':24, 'COMMA':25, 'LBRACE':26, 'RBRACE':27, 'LPAREN':28, 'RPAREN':29,
                'FLOAT':30, 'INT':31, 'PRINT':32, 'CHAR':33, 'TRUE': 34, 'FALSE': 35, 'POWER':36
                }
   
    
    def __init__(self, filename):
        try:
            self.file = open(filename, "r")
        except IOError:
            print "Cannot open text file ", filename
            sys.exit()
        else:    
            self.toks = []
            self.gen = self.lineNumber_generator()
    
    def next(self):
        if len(self.toks) == 0:
            line = self.file.readline()
            if not line:
                return (Lexer.TokenDefInt['EOF'], "End of File", self.Line_Number)
            
            self.Line_Number = self.gen.next()
            line = line.replace("<=", "#@#@#@#@") # #@ will correspond to <=
            line = line.replace(">=", "@#@#@#@#") # @# will correspond to >=
            line = line.replace("==", "$@$@$@$@") # $@ will correspond to ==
            line = line.replace("!=", "@$@$@$@$") # @# will correspond to !=
            line = line.replace("//", "@@@@@@@@") # @@ will correspond to //
            line = line.replace("**", "########") # #$ will correspond to **
            
            self.toks = Lexer.splitpatt.split(line) # if spliting on + fails, it will place a None since we are using () to 'keep it'
            self.toks = filter(None, self.toks) # Remove all None's in the list
            self.toks.reverse() # if given [3 + 7] will return [7 + 3], we will use pop() to access last element in reversed list
        
        #Handle whitespace
        if len(self.toks) == 0:
            return (None, None)
            
        self.curr_tok = self.toks.pop() # Using pop we get the next value starting from the end of the list and moving towards the start
        
        #Handle Comments
        if self.curr_tok == "@@@@@@@@":
            self.toks = []
            return (None, None)
        
        #Handle Valid Tokens
        if self.handle_intlits():
            return self.handle_intlits()
        elif self.handle_IDs_and_Keywords():
            return self.handle_IDs_and_Keywords()
        elif self.handle_single_char_operators():
            return self.handle_single_char_operators()
        elif self.handle_double_char_operators():
            return self.handle_double_char_operators()
        elif self.handle_punctuation():
            return self.handle_punctuation()
        else:
            print "Syntax Error at line ", self.Line_Number, "Invalid Token ", self.curr_tok
            sys.exit()
    
    def handle_intlits(self):
        '''
        
        Function that checks whether the type of the token is a intlit or floatlit
        
        It takes self as the only parameter and returns a triple
            Triple composition = (# corresponding to the type of the token, the token, line number its located on)
        
        Differentiates between integers and doubles and casts the token accordingly.
        The only acceptable numbers are # for ints and #.# for floats
        '''
        if Lexer.intlit.search(self.curr_tok):
            return (Lexer.TokenDefInt['INTLIT'], int(self.curr_tok), self.Line_Number)
        elif Lexer.floatlit.search(self.curr_tok):
            return (Lexer.TokenDefInt['FLOATLIT'], float(self.curr_tok), self.Line_Number)
        
    def handle_IDs_and_Keywords(self):
        '''
        
        Function that checks whether the type of the token is an identifier or keyword
        
        It takes self as the only parameter and returns a triple
            Triple composition = (# corresponding to the type of the token, the token, line number its located on)
            
        Valid Keywords are bool, else, false, if, true, float, int, main, while
        Valid Identifiers are Any Letters, LettersIntegers, Letters_Letters or Letters_LettersIntegers
        Ex. Identifier, Identifier2, Identifier_Identifier, Identifier_Identifier2
        '''
        if Lexer.keyword.search(self.curr_tok):
            if self.curr_tok == 'if':
                return (Lexer.TokenDefInt['IF'], self.curr_tok, self.Line_Number)
            elif self.curr_tok == 'bool':
                return (Lexer.TokenDefInt['BOOL'], self.curr_tok, self.Line_Number)
            elif self.curr_tok == 'else':
                return (Lexer.TokenDefInt['ELSE'], self.curr_tok, self.Line_Number)
            elif self.curr_tok == 'float':
                return (Lexer.TokenDefInt['FLOAT'], self.curr_tok, self.Line_Number)
            elif self.curr_tok == 'int':
                return (Lexer.TokenDefInt['INT'], self.curr_tok, self.Line_Number)
            elif self.curr_tok == 'main':
                return (Lexer.TokenDefInt['MAIN'], self.curr_tok, self.Line_Number)
            elif self.curr_tok == 'while':
                return (Lexer.TokenDefInt['WHILE'], self.curr_tok, self.Line_Number)
            elif self.curr_tok == 'print':
                return (Lexer.TokenDefInt['PRINT'], self.curr_tok, self.Line_Number)
            elif self.curr_tok == 'false':
                return (Lexer.TokenDefInt['FALSE'], self.curr_tok, self.Line_Number)
            elif self.curr_tok == 'true':
                return (Lexer.TokenDefInt['TRUE'], self.curr_tok, self.Line_Number)
            
        if Lexer.Ident.search(self.curr_tok):
            return (self.TokenDefInt['ID'], self.curr_tok,self.Line_Number)
        
    def handle_single_char_operators(self):
        '''
        
        Function that checks whether the type of the token is one of the following +,-,*,/,%,<,>,=,!
        
        It takes self as the only parameter and returns a triple
            Triple composition = (# corresponding to the type of the token, the token, line number its located on)
            
        Valid Operators are +,-,*,/,%,<,>,=,!
        '''
         #Handle Single Case Operators
        if self.curr_tok == '+':
            return (Lexer.TokenDefInt['PLUS'], self.curr_tok, self.Line_Number)
        elif self.curr_tok == '-':
            return (Lexer.TokenDefInt['MINUS'], self.curr_tok, self.Line_Number)
        elif self.curr_tok == '*':
            return (Lexer.TokenDefInt['MULT'], self.curr_tok, self.Line_Number)
        elif self.curr_tok == '/':
            return (Lexer.TokenDefInt['DIV'], self.curr_tok, self.Line_Number)
        elif self.curr_tok == '%':
            return (Lexer.TokenDefInt['MOD'], self.curr_tok, self.Line_Number)
        elif self.curr_tok == '<':
            return (Lexer.TokenDefInt['LESS'], self.curr_tok, self.Line_Number)
        elif self.curr_tok == '>':
            return (Lexer.TokenDefInt['GREATER'], self.curr_tok, self.Line_Number)
        elif self.curr_tok == '=':
            return (Lexer.TokenDefInt['ASSIGNMENT'], self.curr_tok, self.Line_Number)
        elif self.curr_tok == '!':
            return (Lexer.TokenDefInt['BANG'], self.curr_tok, self.Line_Number)
        
    def handle_double_char_operators(self):
        '''
        
        Function that checks whether the type of the token is one of the following <=, >=, !=, ||, &&
        
        It takes self as the only parameter and returns a triple
            Triple composition = (# corresponding to the type of the token, the token, line number its located on)
            
        Valid Operators are <=, >=, ==, !=, ||, &&
        '''
        
        if self.curr_tok == "#@#@#@#@":
            return (Lexer.TokenDefInt['LESS_OR_EQUAL'], "<=", self.Line_Number)
        elif self.curr_tok == "@#@#@#@#":
            return (Lexer.TokenDefInt['GREATER_OR_EQUAL'], ">=", self.Line_Number)
        elif self.curr_tok == "$@$@$@$@":
            return (Lexer.TokenDefInt['EQUAL'], "==", self.Line_Number)
        elif self.curr_tok == "@$@$@$@$":
            return (Lexer.TokenDefInt['NOT_EQUAL'], "!=", self.Line_Number)
        elif self.curr_tok == "########":
            return (Lexer.TokenDefInt['POWER'], "**", self.Line_Number)
        elif self.curr_tok == '||':
            return (Lexer.TokenDefInt['OR'], self.curr_tok, self.Line_Number)
        elif self.curr_tok == '&&':
            return (Lexer.TokenDefInt['AND'], self.curr_tok, self.Line_Number)
        
    def handle_punctuation(self):
        '''

        Function that checks whether the type of the token is one of the following ;, , {, }, (, )  
        
        It takes self as the only parameter and returns a triple
            Triple composition = (# corresponding to the type of the token, the token, line number its located on)
            
        Valid Operators are ; , , {, }, (,)
        '''
        #Handle Punctuation
        if self.curr_tok == ";":
            return (Lexer.TokenDefInt['SEMI'], self.curr_tok, self.Line_Number)
        elif self.curr_tok == ',':
            return (Lexer.TokenDefInt['COMMA'], self.curr_tok, self.Line_Number)
        elif self.curr_tok == '{':
            return (Lexer.TokenDefInt['LBRACE'], self.curr_tok, self.Line_Number)
        elif self.curr_tok == '}':
            return (Lexer.TokenDefInt['RBRACE'], self.curr_tok, self.Line_Number)
        elif self.curr_tok == '(':
            return (Lexer.TokenDefInt['LPAREN'], self.curr_tok, self.Line_Number)
        elif self.curr_tok == ')':
            return (Lexer.TokenDefInt['RPAREN'], self.curr_tok, self.Line_Number)
        
    def lineNumber_generator(self):
        '''
        
        Line Number generator.
        
        Each time a new line is taken and analyzed by the next() function the generator is called to increment the line by 1.
        
        The first time the generator is called returns line number 0
        '''
        yield 1
        line_number = 1
        
        while True:
            line_number = line_number + 1
            yield line_number
        
        
        
        
        
        
