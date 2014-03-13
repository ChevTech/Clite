#!/usr/bin/python

# Anton Stoytchev
# CS 364 Clite Main Program
# 04/23/2013
# This class combines the Lexer, Parser and Interpreter to construct an abstract syntax tree and evaluate it.

import sys
from parser import Parser

# our sample main program  

if __name__ == '__main__':
        pars = Parser(sys.argv[1])
	prog = pars.parse()
	prog.eval()
