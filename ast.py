# Anton Stoytchev
# 04/16/2013
# This file represents the AST structure required by the parser

import sys

'''
This module represents our Abstract Syntax Trees (ASTs) for CLite.
'''

class Program(object):

    def __init__(self, decls, stmts):
        self.decls = decls
        self.stmts = stmts
        # The environment 
        self.env = {}

    def __str__(self):
        '''
        Returns a string representation of the program.
        '''
        
        prog = "int main () {\n"
        indent = 0
        # print the declarations
        for (ident,typ) in self.decls.items():
            prog += "\t{0} {1};\n".format(typ, ident)

        #print the statements
        for stmt in self.stmts:
            prog += stmt.__str__(indent)
        
        prog += '}'
        
        return prog
    
    def eval(self):
        '''
        To evaluate a program evaluate each of the statements
        '''
        for stmt in self.stmts:
            stmt.eval(self.env)
        return self.env
#------------------------------------------------------
#------------------------------------------------------

class Stmt(object):
    '''
    The base class of statements
    '''
    pass

#--------------------------------------------------------
#--------------------------------------------------------

class AssignmentStmt(Stmt):
    '''
    This class represents an assignment statement.
    '''
    
    def __init__(self, decl, expr):
        '''
        decl is the string name of the identifier
        expr is the expression on the right-hand-side
        '''
        self.decl = decl
        self.expr = expr
        
    def __str__(self, indent):
        '''
        Return the string representation of this assignment statement.
        '''
        indent += 1
        return '\t' * indent + self.decl + ' = ' + self.expr.__str__() + ';\n'
                 
    def eval(self, env):
        '''
        To evaluate an assignment statement just update the
        value in the environment.
        '''
        env[self.decl] = self.expr.eval(env)

#---------------------------------------------------------
#---------------------------------------------------------
class IfStatement(Stmt):
    '''
    This class represents an If Statements
    '''
    def __init__(self, expr, stmt, elstmt):
        self.expr = expr
        self.stmt = stmt
        self.elstmt = elstmt
    
    def __str__(self, indent):
        '''
        Return the string representation of an if statement.
        '''
        indent += 1
        return '\t' * indent + 'if ' + self.expr.__str__() + '\n' + self.stmt.__str__(indent)
    
    def eval(self, env):
        '''
        Using an if statement evaluate expr and determine which statement to use.
        '''
        if self.expr.eval(env):
            self.stmt.eval(env)
        else:
            if self.elstmt != None:
                self.elstmt.eval(env)
#---------------------------------------------------------
#---------------------------------------------------------
class WhileStatement(Stmt):
    '''
    This class represents a While statements
    '''
    def __init__(self, expr, stmt):
        self.expr = expr
        self.stmt = stmt
        
    def __str__(self, indent):
        '''
        Return the string representation of a while statement.
        '''
        indent += 1
        return '\t' * indent + 'while ' + self.expr.__str__() + '\n' + self.stmt.__str__(indent)
    
    def eval(self, env):
        while self.expr.eval(env):
            self.stmt.eval(env)
                
#---------------------------------------------------------
#---------------------------------------------------------
class Block(Stmt):
    '''
    This class represents a block of statements
    '''
    def __init__(self, stmt):
        self.stmt = stmt
        
    def __str__(self, indent):
        '''
        Return the string representation of this assignment statement.
        '''
        stmts = '{ \n'
        
        for stmt in self.stmt:
            stmts += stmt.__str__(indent)
        
        stmts += '} \n'
        
        return stmts
    
    def eval(self, env):
        for statement in self.stmt:
            statement.eval(env)

#---------------------------------------------------------
#---------------------------------------------------------
class PrintStatement(Stmt):
    '''
    This class represents a print statement
    '''
    def __init__(self, expr):
        self.expr = expr
        
    def __str__(self, indent):
        indent += 1
        return '\t' * indent + 'print (' + self.expr.__str__() + ') ; \n'
    
    def eval(self, env):
        print self.expr.eval(env)
        
#---------------------------------------------------------
#---------------------------------------------------------
class Semi(Stmt):
    def __init__(self):
        pass
    def __str__(self, indent):
        return '; \n'
#---------------------------------------------------------
#---------------------------------------------------------    
class Expr(object):
    '''
    The base class of all expressions.
    '''
    pass

#---------------------------------------------------------
#---------------------------------------------------------    
class TrueExpr(Expr):
    '''
    This class represents a True Boolean
    '''
    def __init__(self, Bool):
        self.Bool = Bool
        
    def __str__(self):
        return str(self.Bool)
        
    def eval(self, env):
        return True

#---------------------------------------------------------
#---------------------------------------------------------   
class FalseExpr(Expr):
    '''
    This class represents a False Boolean
    '''
    def __init__(self, Bool):
        self.Bool = Bool
    
    def __str__(self):
        return str(self.Bool)
    
    def eval(self, env ):
        return False
    
#---------------------------------------------------------
#---------------------------------------------------------
class IntLitExpr(Expr):
    '''
    This class represents integer literals that appear in
    expressions. Inherits Expr. 
    '''
    def __init__(self, val):
        self.val = val
        
    def __str__(self):
        return str(self.val)
    
    def eval(self, env):
        return self.val
    
#---------------------------------------------------------
#---------------------------------------------------------
class FloatLitExpr(Expr):
    '''
    This class represents float literals that appear in
    expressions. Inherits Expr. 
    '''
    def __init__(self, val):
        self.val = val
        
    def __str__(self):
        return str(self.val)
    
    def eval(self, env):
        return self.val
    
#---------------------------------------------------------
#---------------------------------------------------------
class IdentExpr(Expr):
    '''
    The class represents identifiers that appear in expressions.
    Inherits Expr.
    '''

    def __init__(self, ident):
        self.ident = ident
                
    def __str__(self):
        return str(self.ident)
    
    def eval(self, env):
        # see if ident has been initialized
        if self.ident not in env:
            print "Error: ", self.ident, "not initialized"
            sys.exit(1)
        
        return env[self.ident]
    
#---------------------------------------------------------
#---------------------------------------------------------
class UnaryExpr(Expr):
    '''
    Base class for unary expressions such as
    -(7 * B) and !(A || B)
    '''
    def __init__(self, expr):
        self.expr = expr
#---------------------------------------------------------
#---------------------------------------------------------
class NegExpr(UnaryExpr):
    '''
    A negation unary expression. -7, -a, -(7*b). In general -expr.
    '''
    def __init__(self, expr):
        UnaryExpr.__init__(self, expr)
    
    def __str__(self):
        return '-' + '(' + str(self.expr) + ')'

    def eval(self, env):
        return -self.expr.eval(env)
    
#---------------------------------------------------------
#---------------------------------------------------------    
class NotExpr(UnaryExpr):
    '''
    A not unary expression: not expr.
    '''
    def __init__(self, expr):
        UnaryExpr.__init__(self, expr)
    
    def __str__(self):
        return '!' + '(' + str(self.expr) + ')'

    def eval(self, env):
        return not self.expr.eval(env)
    
#---------------------------------------------------------
#---------------------------------------------------------
class BinaryExpr(Expr):
    '''
    Base class for binary expressions such a * b, a + (b - c)
    '''
    
    def __init__(self, left, right):
        self.left  = left
        self.right = right
        
#---------------------------------------------------------
#---------------------------------------------------------        
class Expression(BinaryExpr):
    '''
    This class represents an Expression: Expr || Expr
    '''
    def __init__(self, left, right):
        BinaryExpr.__init__(self, left, right)
    
    def __str__(self):
        return '(' + self.left.__str__() + ' || ' + self.right.__str__() + ')'
    
    def eval(self, env):
        return self.left.eval(env) or self.right.eval(env)
        
#---------------------------------------------------------
#---------------------------------------------------------        
class Conjunction(BinaryExpr):
    '''
    This class represents a Conjuction: Expr && Expr
    '''
    def __init__(self, left, right):
        BinaryExpr.__init__(self, left, right)
    
    def __str__(self):
        return '(' + self.left.__str__() + ' && ' + self.right.__str__() + ')'
    
    def eval(self, env):
        return self.left.eval(env) and self.right.eval(env)
    
#---------------------------------------------------------
#---------------------------------------------------------
class BinaryEqual(BinaryExpr):
    '''
    This class represents an 'Equal' Equality Expression: Expr == Expr
    '''
    def __init__(self, left, right):
        BinaryExpr.__init__(self, left, right)
    
    def __str__(self):
        return '(' + self.left.__str__() + ' == ' + self.right.__str__() + ')'
    
    def eval(self, env):
        return self.left.eval(env) == self.right.eval(env)

#---------------------------------------------------------
#---------------------------------------------------------
class BinaryNotEqual(BinaryExpr):
    '''
    This class represents a 'Not Equal' Equality Expression: Expr != Expr
    '''
    def __init__(self, left, right):
        BinaryExpr.__init__(self, left, right)
    
    def __str__(self):
        return '(' + self.left.__str__() + ' != ' + self.right.__str__() + ')'
    
    def eval(self, env):
        return (self.left.eval(env) != self.right.eval(env))
    
#---------------------------------------------------------
#---------------------------------------------------------
class BinaryGreater(BinaryExpr):
    '''
    A Relation expression: expr > expr
    ''' 
    def __init__(self, left, right):
        BinaryExpr.__init__(self, left, right)
    
    def __str__(self):
        return '(' + self.left.__str__() + ' > ' + self.right.__str__() + ')'

    def eval(self, env):
        return self.left.eval(env) > self.right.eval(env)
#---------------------------------------------------------
#---------------------------------------------------------
class BinaryLess(BinaryExpr):
    '''
    A Relation expression: expr < expr
    ''' 
    def __init__(self, left, right):
        BinaryExpr.__init__(self, left, right)
        
    def eval(self, env):
        return self.left.eval(env) < self.right.eval(env)
    
    def __str__(self):
        return '(' + self.left.__str__() + ' < ' + self.right.__str__() + ')'

#---------------------------------------------------------
#---------------------------------------------------------
class BinaryGreater_or_Equal(BinaryExpr):
    '''
    A Relation expression: expr >= expr
    ''' 
    def __init__(self, left, right):
        BinaryExpr.__init__(self, left, right)
        
    def eval(self, env):
        return self.left.eval(env) >= self.right.eval(env)
    
    def __str__(self):
        return '(' + self.left.__str__() + ' >= ' + self.right.__str__() + ')'

#---------------------------------------------------------
#---------------------------------------------------------
class BinaryLess_or_Equal(BinaryExpr):
    '''
    A Relation expression: expr <= expr
    ''' 
    def __init__(self, left, right):
        BinaryExpr.__init__(self, left, right)
        
    def eval(self, env):
        return self.left.eval(env) <= self.right.eval(env)
    
    def __str__(self):
        return '(' + self.left.__str__() + ' <= ' + self.right.__str__() + ')'
#---------------------------------------------------------
#---------------------------------------------------------
class BinaryPlus(BinaryExpr):
    '''
    An addition expression: expr + expr.
    '''
    
    def __init__(self, left, right):
        BinaryExpr.__init__(self, left, right)
        
    def eval(self, env):
        return self.left.eval(env) + self.right.eval(env)

    def __str__(self):
        return '(' + self.left.__str__() + ' + ' + self.right.__str__() + ')'
    
#---------------------------------------------------------
#---------------------------------------------------------
class BinaryMinus(BinaryExpr):
    '''
    An addition expression: expr - expr.
    '''
    
    def __init__(self, left, right):
        BinaryExpr.__init__(self, left, right)
        
    def eval(self, env):
        return self.left.eval(env) - self.right.eval(env)

    def __str__(self):
        return '(' + self.left.__str__() + ' - ' + self.right.__str__() + ')'

#---------------------------------------------------------
#---------------------------------------------------------
class BinaryTimes(BinaryExpr):
    '''
    An addition expression: expr * expr.
    '''
    
    def __init__(self, left, right):
        BinaryExpr.__init__(self, left, right)
        
    def __str__(self):
        return "(" + self.left.__str__() + " * " + self.right.__str__() + ")"
    
    def eval(self, env):
        return self.left.eval(env) * self.right.eval(env)

#---------------------------------------------------------
#---------------------------------------------------------
class BinaryDivide(BinaryExpr):
    '''
    A Division expression: expr / expr.
    '''
    def __init__(self, left, right):
        BinaryExpr.__init__(self, left, right)
        
    def __str__(self):
        return "(" + self.left.__str__() + " / " + self.right.__str__() + ")"
    
    def eval(self, env):
        if self.right.eval(env) == 0:
            print "Error Attempt to divide by 0 in expression " + "(" + self.left.__str__() + " / " + self.right.__str__() + ")"
            sys.exit()
            
        return self.left.eval(env) / self.right.eval(env)

#---------------------------------------------------------
#---------------------------------------------------------
class BinaryModule(BinaryExpr):
    '''
    A Module expression: expr % expr.
    '''
    def __init__(self, left, right):
        BinaryExpr.__init__(self, left, right)
        
    def __str__(self):
        return "(" + self.left.__str__() + " % " + self.right.__str__() + ")"
    
    def eval(self, env):
        return self.left.eval(env) % self.right.eval(env)

#---------------------------------------------------------
#---------------------------------------------------------
class BinaryPower(BinaryExpr):
    '''
    An exponential expression: expr ** expr.
    '''
    def __init__(self, left, right):
        BinaryExpr.__init__(self, left, right)
        
    def __str__(self):
        return "(" + self.left.__str__() + "**" + self.right.__str__() + ")"
    
    def eval(self, env):
        return self.left.eval(env) ** self.right.eval(env)
