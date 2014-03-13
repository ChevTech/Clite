# Anton Stoytchev
# 04/16/2013
# This class impliments a top-down recurssion to construct abstract syntax trees using a simple Clite grammer.

import Lexer, sys, ast

'''
This module is a Clite parser. Construct a parser with Parser("filename")
'''

class Parser(object):
    '''
    Singleton.
    '''
    def __init__(self, filename):
        self.lex = Lexer.Lexer(filename)
        self.curr_tok = self.getToken()
        
    def getToken(self):
        token = self.lex.next()
        while token[0] != Lexer.Lexer.TokenDefInt['EOF']:
            while token[0] == None:
                token = self.lex.next()
            return token
        return (Lexer.Lexer.TokenDefInt['EOF'], token[1], token[2])
                
    def parse(self):
        return self.program()
    
    def program(self):
        '''
        Program =  int  main ( ) { Declarations Statements }
        '''
        # match int
        if self.curr_tok[0] != Lexer.Lexer.TokenDefInt['INT']:
            print "int expected found a ", self.curr_tok[1], "on line:", self.curr_tok[2]
            sys.exit(1)
            
        # match main
        self.curr_tok = self.getToken()
        if self.curr_tok[0] != Lexer.Lexer.TokenDefInt['MAIN']:
            print "main expected found a ", \
            self.curr_tok[1], " on line:", self.curr_tok[2]
            sys.exit(1)
            
        # match (
        self.curr_tok = self.getToken()
        if self.curr_tok[0] != Lexer.Lexer.TokenDefInt['LPAREN']:
            print "( expected found a ", \
            self.curr_tok[1], " on line:", self.curr_tok[2]
            sys.exit(1)
            
        # match )
        self.curr_tok = self.getToken()
        if self.curr_tok[0] != Lexer.Lexer.TokenDefInt['RPAREN']:
            print ") expected found a ", \
            self.curr_tok[1], " on line:", self.curr_tok[2]
            sys.exit(1)
            
        # match {
        self.curr_tok = self.getToken()
        if self.curr_tok[0] != Lexer.Lexer.TokenDefInt['LBRACE']:
            print "{ expected found a ", \
            self.curr_tok[1], " on line:", self.curr_tok[2]
            sys.exit(1)
        
        self.curr_tok = self.getToken()
        self.decls = self.declarations()
        self.stmts = self.statements()
        
        # match }
        if self.curr_tok[0] != Lexer.Lexer.TokenDefInt['RBRACE']:
            print "} expected found a ", \
            self.curr_tok[1], " on line:", self.curr_tok[2]
            sys.exit(1)
        
        return ast.Program(self.decls, self.stmts)
    
#---------------------------------------------------------------
#--------------------------------------------------------------- 
    def declarations(self):
        '''
        Declarations = { Type Identifier ; }
        '''
        decls = {}
        
        while self.typeof():
            typtok = self.curr_tok
            self.curr_tok = self.getToken()
            if self.curr_tok[0] != Lexer.Lexer.TokenDefInt['ID']:
                print "identifier expected found a", \
                self.curr_tok[1], " on line:", self.curr_tok[2]
                sys.exit(1)
            
            idtok = self.curr_tok
            
            # match a semicolon
            self.curr_tok = self.getToken()
            if self.curr_tok[0] != Lexer.Lexer.TokenDefInt['SEMI']:
                print "semicolon expected found a ", \
                self.curr_tok[1], " on line:", self.curr_tok[2]
                sys.exit(1)
            
            # make sure identifier is not
            # already declared
            if idtok[1] in decls:
                print "identifier ", idtok[1], "already declared on line:", self.curr_tok[2]
                sys.exit(1)
            
            self.curr_tok = self.getToken()
            decls[idtok[1]] = typtok[1]

        return decls

#---------------------------------------------------------------
#---------------------------------------------------------------    
    def typeof(self):
        '''
         Type = int | bool | float | char
        '''
        return self.curr_tok[0] in [Lexer.Lexer.TokenDefInt['INT'],
                                    Lexer.Lexer.TokenDefInt['FLOAT'],
                                    Lexer.Lexer.TokenDefInt['BOOL'],
                                    Lexer.Lexer.TokenDefInt['CHAR']
                                    ]

#---------------------------------------------------------------
#---------------------------------------------------------------
    def statements(self):
        '''
        Statements = { statement }
        '''
        stmts = []
        
        first = [Lexer.Lexer.TokenDefInt['SEMI'],
                     Lexer.Lexer.TokenDefInt['LBRACE'],
                     Lexer.Lexer.TokenDefInt['ID'],
                     Lexer.Lexer.TokenDefInt['IF'],
                     Lexer.Lexer.TokenDefInt['WHILE'],
                     Lexer.Lexer.TokenDefInt['PRINT']
                ]
        while self.curr_tok[0] in first:
            stmt = self.statement()
            stmts.append(stmt)
        
        return stmts
    
#---------------------------------------------------------------
#---------------------------------------------------------------
    def statement(self):
        '''
        Statement = ; | Block | Assignment | IfStatement | WhileStatement | PrintStatement
        '''
        if self.curr_tok[0] == Lexer.Lexer.TokenDefInt['ID']:
            stmt = self.assignment()
        elif self.curr_tok[0] == Lexer.Lexer.TokenDefInt['LBRACE']:
            stmt = self.block()
        elif self.curr_tok[0] == Lexer.Lexer.TokenDefInt['IF']:
            stmt = self.IfStatement()
        elif self.curr_tok[0] == Lexer.Lexer.TokenDefInt['WHILE']:
            stmt = self.WhileStatement()
        elif self.curr_tok[0] == Lexer.Lexer.TokenDefInt['PRINT']:
            stmt = self.PrintStatement()
        elif self.curr_tok[0] == Lexer.Lexer.TokenDefInt['SEMI']:
            stmt = self.Semi()
        return stmt
#---------------------------------------------------------------
#---------------------------------------------------------------

    def assignment(self):
        '''
        Assignment = Identifier = Expression ;
        '''
        decl = self.curr_tok  
        
        # make sure ID is declared in decls
        if decl[1] not in self.decls:
            print "Identifier,", decl[1], "not declared on line", self.curr_tok[2]
            sys.exit()
        
        # match =
        self.curr_tok = self.getToken()
        if self.curr_tok[0] != Lexer.Lexer.TokenDefInt['ASSIGNMENT']:   # match =
            print "Invalid token", self.curr_tok[1], "expected \"=\" on line:", self.curr_tok[2]
            sys.exit()
            
        self.curr_tok = self.getToken()
        expr = self.Expression()
        
        #check for semicolon
        if self.curr_tok[0] != Lexer.Lexer.TokenDefInt['SEMI']:
            print "semicolon expected found a ", self.curr_tok[1], " on line:", self.curr_tok[2]
            sys.exit()
        
        match, type_expr = self.MatchType(self.decls[decl[1]], type(expr))
        if not match:
            print "Miss-matched types. \n Identifier type", self.decls[decl[1]]," expression type", type_expr, "on line", decl[2]
            sys.exit()
            
        self.curr_tok = self.getToken()            
        return ast.AssignmentStmt(decl[1], expr)
    
#---------------------------------------------------------------
#---------------------------------------------------------------
    def MatchType(self,decl_type, expr_type):
        '''
        Check if the ident type matches the Expr type
        '''
        if expr_type == ast.IntLitExpr and decl_type != 'int':
            return False, 'int'
        elif expr_type == ast.FloatLitExpr and decl_type != 'float':
            return False, 'float'
        elif (expr_type == ast.FalseExpr or expr_type == ast.TrueExpr) and decl_type != 'bool':
            return False, 'bool'
        else:
            return True, None
    
#---------------------------------------------------------------
#---------------------------------------------------------------
    def block(self):
        '''
        Block = { Statements }
        '''
        # match statement
        self.curr_tok = self.getToken()
        stmts = self.statements()
        
        # match }
        if self.curr_tok[0] != Lexer.Lexer.TokenDefInt['RBRACE']:
            print "Error expected }, found", \
            self.curr_tok[1], " on line:", self.curr_tok[2]
            sys.exit()
        
        self.curr_tok = self.getToken()           
        return ast.Block(stmts)

#---------------------------------------------------------------
#---------------------------------------------------------------
    def IfStatement(self):
        '''
        IfStatement = if ( Expression ) Statement [ else Statement ]
        '''
        
        # consume the IF token
        self.curr_tok = self.getToken()
        
        # match a (
        if self.curr_tok[0] != Lexer.Lexer.TokenDefInt['LPAREN']:
            print "Error expected left paren recieved ", \
            self.curr_tok[1], " on line:", self.curr_tok[2]
            sys.exit()
        
        # match expr
        self.curr_tok = self.getToken()
        expr = self.Expression()
        
        # match )
        if self.curr_tok[0] != Lexer.Lexer.TokenDefInt['RPAREN']:
            print "Error expected right paren recieved ", \
            self.curr_tok[1], " on line:", self.curr_tok[2]
            sys.exit()
        
        # match statement
        self.curr_tok = self.getToken()
        stmt = self.statement()
            
        # match else statement
        if self.curr_tok[0] == Lexer.Lexer.TokenDefInt['ELSE']: 
            self.curr_tok = self.getToken()
            elstmt = self.statement()
        else:
            elstmt = None
            
        return ast.IfStatement(expr, stmt, elstmt)

#---------------------------------------------------------------
#---------------------------------------------------------------        
    def WhileStatement(self):
        '''
        WhileStatement = while ( Expression ) Statement
        '''
        # match a (
        self.curr_tok = self.getToken()
        if self.curr_tok[0] != Lexer.Lexer.TokenDefInt['LPAREN']:
            print "Error expected left paren recieved ", \
            self.curr_tok[1], " on line:", self.curr_tok[2]
            sys.exit()
        
        # match an expr
        self.curr_tok = self.getToken()
        expr = self.Expression()
            
        # match a )
        if self.curr_tok[0] != Lexer.Lexer.TokenDefInt['RPAREN']:
            print "Error expected right paren recieved ", \
            self.curr_tok[1], " on line:", self.curr_tok[2]
            sys.exit()
                
        # match stmt
        self.curr_tok = self.getToken()
        stmt = self.statement()
        
        return ast.WhileStatement(expr, stmt)

#---------------------------------------------------------------
#---------------------------------------------------------------
    def PrintStatement(self):
        '''
        PrintStatement = print( Expression ) ;
        '''
        self.curr_tok = self.getToken()
        
        if self.curr_tok[0] != Lexer.Lexer.TokenDefInt['LPAREN']:
            print "Error expected left paren recieved ", \
            self.curr_tok[1], " on line:", self.curr_tok[2]
            sys.exit()
        
        self.curr_tok = self.getToken()
        expr = self.Expression()
        
        if self.curr_tok[0] != Lexer.Lexer.TokenDefInt['RPAREN']:
            print "Error expected right paren recieved ", \
            self.curr_tok[1], " on line:", self.curr_tok[2]
            sys.exit()
        
        self.curr_tok = self.getToken()
        if self.curr_tok[0] != Lexer.Lexer.TokenDefInt['SEMI']:
            print "Error expected ; recieved ", \
            self.curr_tok[1], " on line:", self.curr_tok[2]
            sys.exit()
            
        self.curr_tok = self.getToken()  
        return ast.PrintStatement(expr)
#---------------------------------------------------------------
#---------------------------------------------------------------
    def Semi(self):
        self.curr_tok = self.getToken()
        return ast.Semi()
#---------------------------------------------------------------
#---------------------------------------------------------------
    def Expression(self):
        '''
        Expression = Conjunction { || Conjunction }
        '''
        left = self.Conjunction()
        
        while self.curr_tok[0] == Lexer.Lexer.TokenDefInt['OR']:
            self.curr_tok = self.getToken()
            right = self.Conjunction()
            left = ast.Expression(left, right)
        return left

#---------------------------------------------------------------
#---------------------------------------------------------------
    def Conjunction(self):
        '''
        Conjunction = Equality { && Equality }
        '''
        left = self.Equality()
        
        while self.curr_tok[0] == Lexer.Lexer.TokenDefInt['AND']:
            self.curr_tok = self.getToken()
            right = self.Equality()
            left = ast.Conjunction(left, right)
        return left

#---------------------------------------------------------------
#---------------------------------------------------------------
    def Equality(self):
        '''
        Equality = Relation [ EquOp Relation ]
        '''
        left = self.Relation()
        
        if self.EquOp():
            if self.curr_tok[0] == Lexer.Lexer.TokenDefInt['EQUAL']:
                self.curr_tok = self.getToken()
                right = self.Relation()
                left = ast.BinaryEqual(left, right)
            else:
                self.curr_tok = self.getToken()
                right = self.Relation()
                left = ast.BinaryNotEqual(left, right)
        return left

#---------------------------------------------------------------
#---------------------------------------------------------------
    def EquOp(self):
        '''
        EquOp = == | !=
        '''
        return self.curr_tok[0] in [Lexer.Lexer.TokenDefInt['EQUAL'],
                                    Lexer.Lexer.TokenDefInt['NOT_EQUAL']]

#---------------------------------------------------------------
#---------------------------------------------------------------   
    def Relation(self):
        '''
        Relation = Addition [ RelOp Addition ]
        '''
        left = self.addition()
        
        if self.RelOp():
            if self.curr_tok[0] == Lexer.Lexer.TokenDefInt['GREATER']:
                self.curr_tok = self.getToken()
                right = self.addition()
                left = ast.BinaryGreater(left, right)
            elif self.curr_tok[0] == Lexer.Lexer.TokenDefInt['LESS']:
                self.curr_tok = self.getToken()
                right = self.addition()
                left = ast.BinaryLess(left, right)
            elif self.curr_tok[0] == Lexer.Lexer.TokenDefInt['GREATER_OR_EQUAL']:
                self.curr_tok = self.getToken()
                right = self.addition()
                left = ast.BinaryGreater_or_Equal(left, right)
            else:
                self.curr_tok = self.getToken()
                right = self.addition()
                left = ast.BinaryLess_or_Equal(left, right)
        return left
    
#---------------------------------------------------------------
#---------------------------------------------------------------
    def RelOp(self):
        '''
        RelOp = < | <= | > | >=
        '''
        return self.curr_tok[0] in [Lexer.Lexer.TokenDefInt['LESS'], \
                                    Lexer.Lexer.TokenDefInt['GREATER'], \
                                    Lexer.Lexer.TokenDefInt['LESS_OR_EQUAL'], \
                                    Lexer.Lexer.TokenDefInt['GREATER_OR_EQUAL']]

#---------------------------------------------------------------
#---------------------------------------------------------------
    def addition(self):
        '''
           Addition = Term { Addop Term }
        '''
        left = self.term()
        
        while self.addop():
            if self.curr_tok[0] == Lexer.Lexer.TokenDefInt['PLUS']:
                self.curr_tok = self.getToken()
                right = self.term()
                left = ast.BinaryPlus(left,right)
            else:
                self.curr_tok = self.getToken()
                right = self.term()
                left = ast.BinaryMinus(left,right)    
        return left

#---------------------------------------------------------------
#---------------------------------------------------------------
    def addop(self):
        '''
           AddOp =  + | -
           return: return true if we are looking at a '+' or '-' token
        '''
        return self.curr_tok[0] in \
               [Lexer.Lexer.TokenDefInt['PLUS'], Lexer.Lexer.TokenDefInt['MINUS']]

#---------------------------------------------------------------
#---------------------------------------------------------------
    def term(self):
        '''
           Term =  ExpOp { MulOp ExOp }
        '''
        
        left = self.ExpOp()
        
        while self.mulop():
            if self.curr_tok[0] == Lexer.Lexer.TokenDefInt['MULT']:
                self.curr_tok = self.getToken()
                right = self.ExpOp()
                left = ast.BinaryTimes(left,right)
            elif self.curr_tok[0] == Lexer.Lexer.TokenDefInt['DIV']:
                self.curr_tok = self.getToken()
                right = self.ExpOp()
                left = ast.BinaryDivide(left,right)
            else:
                self.curr_tok = self.getToken()
                right = self.ExpOp()
                left = ast.BinaryModule(left,right)
        return left
    
#---------------------------------------------------------------
#---------------------------------------------------------------
    def ExpOp(self):
        '''
           ExpOp = {factor **} factor
        '''
        left = self.factor()
        if self.curr_tok[0] == Lexer.Lexer.TokenDefInt['POWER']:
            self.curr_tok = self.getToken()
            right = self.ExpOp()
            left = ast.BinaryPower(left, right)
        return left

#---------------------------------------------------------------
#---------------------------------------------------------------
    def mulop(self):
        '''
           MulOp =  * | / | %
           return: return true of we are
           looking at a '*' or '/', or '%' token
        '''
        return self.curr_tok[0] in \
               [Lexer.Lexer.TokenDefInt['MULT'], Lexer.Lexer.TokenDefInt['DIV'],
                Lexer.Lexer.TokenDefInt['MOD']]

#---------------------------------------------------------------
#---------------------------------------------------------------
    def unaryop(self):
        '''
           UnaryOp = - | !
        '''
        return self.curr_tok[0] in [Lexer.Lexer.TokenDefInt['MINUS'],
                                    Lexer.Lexer.TokenDefInt['BANG']]

#---------------------------------------------------------------
#---------------------------------------------------------------
    def factor(self):
        '''
           Factor =  [ UnaryOp ] Primary
        '''
        if self.unaryop():
            if self.curr_tok[0] == Lexer.Lexer.TokenDefInt['MINUS']:
                self.curr_tok = self.getToken()
                expr = ast.NegExpr(self.primary())
            elif self.curr_tok[0] == Lexer.Lexer.TokenDefInt['BANG']:
                self.curr_tok = self.getToken()
                expr = ast.NotExpr(self.primary())
        else:
            expr = self.primary()
        return expr

#---------------------------------------------------------------
#---------------------------------------------------------------
    def primary(self):
        '''
           Primary =  Identifier | IntLit | FloatLit | ( Expression ) | True | False
        '''
        if self.curr_tok[0] == Lexer.Lexer.TokenDefInt['ID']:
            t = self.curr_tok[1]
            self.curr_tok = self.getToken()
            return ast.IdentExpr(t)
        elif self.curr_tok[0] == Lexer.Lexer.TokenDefInt['INTLIT']:
            t = self.curr_tok[1]
            self.curr_tok = self.getToken()
            return ast.IntLitExpr(t)
        elif self.curr_tok[0] == Lexer.Lexer.TokenDefInt['FLOATLIT']:
            t = self.curr_tok[1]
            self.curr_tok = self.getToken()
            return ast.FloatLitExpr(t)
        elif self.curr_tok[0] == Lexer.Lexer.TokenDefInt['TRUE']:
            t = self.curr_tok[1]
            self.curr_tok = self.getToken()
            return ast.TrueExpr(t)
        elif self.curr_tok[0] == Lexer.Lexer.TokenDefInt['FALSE']:
            t = self.curr_tok[1]
            self.curr_tok = self.getToken()
            return ast.FalseExpr(t)
        elif self.curr_tok[0] == Lexer.Lexer.TokenDefInt['LPAREN']:
            self.curr_tok = self.getToken()
            expr = self.Expression()
            if self.curr_tok[0] == Lexer.Lexer.TokenDefInt['RPAREN']:
                self.curr_tok = self.getToken()
                return expr
            else:
                print 'syntax error missing right paren on line', self.curr_tok[2]
                sys.exit(1)
        else:
            print 'syntax error: unexpected input', self.curr_tok[1], " on line:", self.curr_tok[2]
            sys.exit(1)

