"""
*  
*  Copyright (c) Peregrine-lang, 2021. All rights reserved.
*
"""

from parser import ast
from lexer.tokens import *
from errors.errors import *
from typing import Dict, List
from enum import IntEnum, auto
from sys import exit

class Precedence(IntEnum):
    pr_lowest = auto()   # lowest possible precedence
    pr_and = auto()      # and, or
    pr_not = auto()      # not
    pr_equal = auto()    # ==, !=, <, >, <=, >=
    pr_sum = auto()      # +, -
    pr_mul = auto()      # *, /, %, //
    pr_prefix = auto()   # -x

precedenceMap: Dict[TokenType, Precedence] = {
    TokenType.tk_and : Precedence.pr_and,
    TokenType.tk_or : Precedence.pr_and,

    TokenType.tk_not : Precedence.pr_not,

    TokenType.tk_equal : Precedence.pr_equal,
    TokenType.tk_not_equal : Precedence.pr_equal,
    TokenType.tk_greater : Precedence.pr_equal,
    TokenType.tk_less : Precedence.pr_equal,
    TokenType.tk_gr_or_equ : Precedence.pr_equal,
    TokenType.tk_less_or_equ : Precedence.pr_equal,

    TokenType.tk_plus : Precedence.pr_sum,
    TokenType.tk_minus : Precedence.pr_sum,

    TokenType.tk_asterisk : Precedence.pr_mul,
    TokenType.tk_divide : Precedence.pr_mul,
}

LangTypes = [ 
    TokenType.tk_str,
	TokenType.tk_bool,
	TokenType.tk_char,
	TokenType.tk_float,
	TokenType.tk_float32,
	TokenType.tk_void,
	TokenType.tk_int,
	TokenType.tk_int32,
	TokenType.tk_int16,
	TokenType.tk_int8,
	TokenType.tk_uint32,
	TokenType.tk_uint16,
	TokenType.tk_uint8,
	TokenType.tk_uint
]

class Parser:
    tk_index: int = 0 # index of the current token
    filename: str = ""
    tokens: List[Token]
    errors: List[PEError] = []
    current_token: Token

    def __init__(self, filename: str,tokens: List[Token]) -> None:
        self.tokens = tokens
        self.filename = filename
        self.advance()

    def parse(self) -> ast.Node:
        programNode =  ast.Program()

        while self.tk_index < len(self.tokens):
            programNode.nodes.append(self.parseStatement())
            self.advance()

        # display the errors if there is any
        if len(self.errors):
            for err in self.errors:
                err.display()

            exit(1)

        return programNode

    def error(self, message: str, errorCode: str) -> None:
        codeBlock = ""

        with open(self.filename) as code:
            for i, line in enumerate(code):
                if i == self.current_token.line:
                    codeBlock = line
                    break

        newError = PEError(Location(
            self.current_token.line, self.current_token.index, self.filename, codeBlock
        ), "error code str", message, "error code hint", errorCode)

        self.errors.append(newError)

    # TODO: check to see if we failed to advance, otherwise it could lead to an infinite loop
    def advance(self) -> None:
        if self.tk_index >= len(self.tokens):
            return

        self.current_token = self.tokens[self.tk_index]
        self.tk_index += 1

    def expect(self, tokenType: TokenType) -> None:
        if self.nextToken().tk_type != tokenType:
            pass # panic

        self.advance()

    # always check to see if the result is not None
    def nextToken(self) -> Token:
        if self.tk_index < len(self.tokens):
            return self.tokens[self.tk_index]

        return None

    def nextPrecedence(self) -> int:
        if self.nextToken() and self.nextToken().tk_type in precedenceMap:
            return precedenceMap[self.nextToken().tk_type]

        return Precedence.pr_lowest

    def parseStatement(self) -> ast.Node:
        newNode: ast.Node

        if self.current_token.tk_type == TokenType.tk_identifier:
            if self.nextToken() and self.nextToken().tk_type != TokenType.tk_assign:
                newNode = self.parseExpression(Precedence.pr_lowest)

            newNode = self.parseVariableReassignment()

        elif self.current_token.tk_type in LangTypes:
            newNode = self.parseVariableDeclaration()

        elif self.current_token.tk_type == TokenType.tk_if:
            newNode = self.parseIf()
        
        elif self.current_token.tk_type == TokenType.tk_while:
            newNode = self.parseWhile()

        elif self.current_token.tk_type == TokenType.tk_for:
            newNode = self.parseFor()

        elif self.current_token.tk_type == TokenType.tk_match:
            newNode = self.parseMatch()

        elif self.current_token.tk_type == TokenType.tk_def:
            newNode = self.parseFunctionDeclaration()

        elif self.current_token.tk_type == TokenType.tk_ccode:
            newNode = self.parseCcode()

        # no matches found, current token must be part of an expression    
        else:
            newNode = self.parseExpression(Precedence.pr_lowest)

        return newNode

    def parseInteger(self) -> ast.Node:
        return ast.IntegerLiteral(self.current_token.keyword)

    def parseString(self) -> ast.Node:
        return ast.StringLiteral(self.current_token.keyword)

    def parseBool(self) -> ast.Node:
        return ast.BoolLiteral(self.current_token.tk_type == TokenType.tk_true)

    def parseIdentifier(self) -> ast.Node:
        return ast.Identifier(self.current_token.keyword)

    def parseBinaryOperation(self, left: ast.Node) -> ast.Node:
        currentPrecedence = precedenceMap[self.current_token.tk_type]
        operator = self.current_token.keyword

        self.advance()

        right = self.parseExpression(currentPrecedence)

        return ast.BinaryOperation(left, operator, right)

    def parsePrefixExpression(self) -> ast.Node:
        prefix = self.current_token.keyword

        self.advance()

        right = self.parseExpression(Precedence.pr_prefix)

        return ast.PrefixExpression(prefix, right)
 
    # this parses expressions enclosed by parenthesis, like (5 + 3)
    def parseGroupedExpression(self) -> ast.Node:
        self.advance()

        node = self.parseExpression(Precedence.pr_lowest)

        self.expect(TokenType.tk_r_paren)

        return node

    def parseExpression(self, precedence: int) -> ast.Node:
        left: ast.Node

        if self.current_token.tk_type == TokenType.tk_int:
            left = self.parseInteger()
        elif self.current_token.tk_type == TokenType.tk_str:
            left = self.parseString()
        elif self.current_token.tk_type == TokenType.tk_bool:
            left = self.parseBool()
        elif self.current_token.tk_type == TokenType.tk_identifier:
            left = self.parseIdentifier()
        elif self.current_token.tk_type == TokenType.tk_l_paren:
            left = self.parseGroupedExpression()
        elif self.current_token.tk_type == TokenType.tk_minus:
            left = self.parsePrefixExpression()
        else:
            print("Error: ")
            print(self.current_token.tk_type)
            pass #panic

        while self.nextPrecedence() > precedence:
            self.advance()

            left = self.parseBinaryOperation(left) # not only binary operatios

        return left

    def parseVariableReassignment(self) -> ast.Node:
        identifier = self.current_token.keyword

        # we already made sure that the next token is =
        self.advance()
        self.advance()

        newValue = self.parseExpression(Precedence.pr_lowestr)

        return ast.VariableReassignment(identifier, newValue)

    def parseVariableDeclaration(self) -> ast.Node:
        varType = self.current_token

        self.expect(TokenType.tk_identifier)

        name = self.current_token.keyword

        # uninitialized variable
        if self.nextToken() and self.nextToken().tk_type != TokenType.tk_assign:
            return ast.VariableDeclaration(varType, name)
        
        self.advance()
        self.advance()

        value = self.parseExpression(Precedence.pr_lowest)

        return ast.VariableDeclaration(varType, name, value)

    def parseIf(self) -> ast.Node:
        pass

    def parseWhile(self) -> ast.Node:
        pass

    def parseFor(self) -> ast.Node:
        pass

    def parseMatch(self) -> ast.Node:
        pass

    def parseFunctionDeclaration(self) -> ast.Node:
        pass