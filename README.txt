This is a simple version of a Java/C++ like language designed by implementing a Lexer, Parser and Interpreter using python.

The program is based on this Clite Syntax Grammer:

  Program         =  int  main ( ) { Declarations Statements }
  Declarations    =  Declaration Declarations | epsilon
  Declaration     =  Type  Identifier  ;
  Type            =  int | bool | float | char
  Statements      =  Statement  Statements | epsilon
  Statement       =  ; | Block | Assignment | IfStatement | WhileStatement
  Block           =  { Statements }
  Assignment      =  Identifier = Expression ;
  IfStatement     =  if ( Expression ) Statement [ else Statement ]
  WhileStatement  =  while ( Expression ) Statement  
  Expression      =  Conjunction { || Conjunction }
  Conjunction     =  Equality { && Equality }
  Equality        =  Relation [ EquOp Relation ]
  EquOp           =  == | != 
  Relation        =  Addition [ RelOp Addition ]
  RelOp           =  < | <= | > | >= 
  Addition        =  Term { AddOp Term }
  AddOp           =  + | -
  Term            =  Factor { MulOp Factor }
  MulOp           =  * | / | %
  Factor          =  [ UnaryOp ] Primary
  UnaryOp         =  - | !
  Primary         =  Identifier | IntLit | FloatLit |  ( Expression )

This program breaks down into three main parts.

1.) The Lexer - The job of the lexer is to break down a file into valid tokens that will be passed to the parser.
2.) The Parser - The parser recieves the tokens from the Lexer and does a recursive descent to construct an abstract syntax tree.
3.) The Interpreter - The job of the interpreter which is imbedded in the Abstract Syntax Tree is to traverse the program tree created by the parser and evaluate each statment.



Implemented by Anton Stoytchev


