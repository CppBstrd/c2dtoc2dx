#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Cocos2d to Cocos2d-x-2 parsing tools."""

import file_tools
import help2dx
import ply.lex as lex

class BracketsStack(list):
    """Brackets stack for CocosLexer."""
    def __init__(self):
        """Stack creation."""
        super(BracketsStack, self).__init__()

    def push(self, objccall):
        """Push item."""
        # [ Obj-C call flag, get the 1st method's part ]
        super(BracketsStack, self).append([objccall, False, False])

    def pop(self):
        """Pop stack item."""
        poped = super(BracketsStack, self).pop()
        if not self.empty():
            self[-1][1] = bool(self[-1][1] + poped[1])

    def empty(self):
        """Checks if stack is empty"""
        return len(self) == 0

    def objc_call(self):
        """Checks if it is Obj-C call."""
        return not self.empty() and self[-1][0]

    def object_parsed(self):
        """Returns info."""
        return self[-1][1]

    def header_parsed(self):
        """Returns info."""
        return self[-1][2]

    def set_object_parsed(self):
        """Sets the 1st part as parsed."""
        self[-1][1] = self[-1][0]

    def set_header_parsed(self):
        """Sets the 1st part as parsed."""
        self[-1][2] = self[-1][0]

# pylint: disable=attribute-defined-outside-init
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-public-methods
# pylint: disable=invalid-name, no-self-use
class CocosLexer(object):
    """Cocos Lexer."""
    #####################
    # Create the Lexer. #
    #####################
    def __init__(self):
        """Lexer creation."""
        self._lexer = None
        self._stack = BracketsStack()
        self.refresh()  # remaining flags are there

    ###############
    # Properties. #
    ###############
    @property
    def is_header(self):
        """Checks if header file is being parsed."""
        return self._header

    @is_header.setter
    def is_header(self, value):
        """Setter."""
        self._header = value

    @property
    def brace_counter(self):
        """Left braces count."""
        return self._brace_counter

    @brace_counter.setter
    def brace_counter(self, value):
        """Setter."""
        pass

    ###################
    # Useful methods. #
    ###################
    def discard_class_name(self):
        """Discards class name."""
        self._class_name = None

    def discard_method_flags(self):
        """Discards method flags."""
        self._static_method = False
        self._1st_part_parsed = False

    def inc_brace(self):
        """Add brace."""
        self._brace_counter += 1

    def dec_brace(self):
        """Delete brace."""
        self._brace_counter -= 1
        if self._brace_counter < 0:
            raise Exception("Brace count error")

    def method_decl_ability(self):
        """Checks method declaration ability."""
        return self._last_symbol is None or self._last_symbol in '};'

    def method_call_ability(self):
        """Checks if [-symbol is begin of Obj-C call."""
        return self._last_symbol is None or \
            not self.message_ability() or \
            self._last_word in ('do', 'else', 'in', 'return')

    def message_ability(self):
        """Checks if \\w+ is an Obj-C message."""
        return self._last_symbol.isalnum() or self._last_symbol in '_)]'

    def refresh(self):
        """Refreshes internal state."""
        # is file header
        self._header = False
        # is there '#pragma once'
        self._pragma_onced = False
        # is inside @interface .. @end
        self._in_class_zone = False
        # is method started with '+'
        self._static_method = False
        # is first part of obj-c method parsed
        self._1st_part_parsed = False
        # last actual symbol
        self._last_symbol = None
        # last actual word
        self._last_word = None
        # current class name
        self._class_name = None
        # count of unclosed left braces
        self._brace_counter = 0

    ####################
    # Build the Lexer. #
    ####################
    def build(self, **kwargs):
        """Lexer Building."""
        self._lexer = lex.lex(module=self, **kwargs)

    #################
    # Data feeding. #
    #################
    def feed(self, code):
        """Feeds input data to parsing."""
        self._lexer.input(code)

    def feed_from_file(self, file_name):
        """Feeds input data to parsing from file."""
        with open(file_name, 'r') as in_file:
            self.feed(''.join(in_file.readlines()))
            self.is_header = file_tools.is_header(file_name)

    ################
    # Lexer items. #
    ################
    states = (('methoddecl', 'inclusive'),)

    # Tokens
    tokens = (# basic
              'NUMBER', 'STRING', 'CHAR', 'NEWLINE',
              # comments
              'SLCOMMENT', 'MLCOMMENT',
              # preprocessor
              'IMPORT', 'PRAGMA_ONCE', 'DEFINE', 'PREPROCESSOR',
              # @.*
              'CLASSDECL', 'IMPLEMENTATION', 'PROPERTYPLUS',
              'SELECTOR', 'END', 'ATSIGNCLASS',
              # {}
              'LBRACE', 'RBRACE',
              # []
              'LSQBRACKET', 'RSQBRACKET',
              # for method declaration
              'PLUSMINUS', 'PARAMCLASS', 'METHODPART',
              # certain cases
              'SELFPOINT', 'COCOSWORD', 'ID', 'COMPLEXOP',
              # other
              'OTHER')

    # TODO: update numbers, dirty realization
    def t_ANY_NUMBER(self, tok):
        r'[+-]?\d+(\.\d*([eE][+-]?\d+)?)?[fFlL]?'
        return tok

    def t_ANY_CHAR(self, tok):
        r"'([^\\]|\\.)'"
        return tok

    def t_ANY_SLCOMMENT(self, tok):
        r'//(.|\\\n)*'
        return tok

    def t_ANY_MLCOMMENT(self, tok):
        r'/\*(.|\n)*?\*/'
        return tok

    def t_ANY_STRING(self, tok):
        r'@?(?P<str>"(\\\n|\\"|.)*?")'
        tok.value = help2dx.update_format(tok.lexer.lexmatch.group('str'))
        self._last_symbol = '"'
        self._last_word = 'nsstring'
        return tok

    def t_ANY_NEWLINE(self, tok):
        r'(?P<long>\s*\n){2,}|(\s*\n)'
        tok.value = '\n\n' if tok.lexer.lexmatch.group('long') else '\n'
        return tok

    def t_ANY_IMPORT(self, tok):
        r'\#import\s*(?P<header>[<"].*?[>"])'
        header = tok.lexer.lexmatch.group('header')
        tok.value = '//' + tok.value \
            if help2dx.ignored_header(header[1:-1].strip()) \
            else '#include ' + header
        return tok

    def t_ANY_PRAGMAONCE(self, tok):
        r'\#pragma\s+once'
        self._pragma_onced = True
        return tok

    def t_ANY_DEFINE(self, tok):
        r'\#define\s+'
        tok.value = '#define '
        return tok

    def t_ANY_PREPROCESSOR(self, tok):
        r'\#((\\\n)|.)*'
        return tok

    def t_ANY_CLASSDECL(self, tok):
        r'@(interface|protocol)\s+(?P<name_of_class>\w+)'
        self._class_name = tok.lexer.lexmatch.group('name_of_class')
        self._in_class_zone = True
        self._last_symbol = '_'
        tok.value = 'class ' + self._class_name
        return tok

    def t_ANY_IMPLEMENTATION(self, tok):
        r'@implementation\s+(?P<name_of_class>\w+)'
        self._class_name = tok.lexer.lexmatch.group('name_of_class')
        tok.value = '//' + tok.value
        return tok

    def t_ANY_PROPERTYPLUS(self, tok):
        r'@\s*(property|synthesize|optional).*'
        tok.value = '//' + tok.value
        return tok

    def t_ANY_SELECTOR(self, tok):
        r'@selector\s*\(\s*(?P<method>\w+)\s*(?P<callfunc>:?)\s*\)'
        if self._last_word in ('schedule', 'unschedule'):
            prefix = 'schedule_selector('
        elif not tok.lexer.lexmatch.group('callfunc'):
            prefix = 'callfunc_selector('
        else:
            prefix = '@selector('
        tok.value = prefix + \
                    self._class_name + '::' + \
                    tok.lexer.lexmatch.group('method') + ')'
        return tok

    def t_ANY_END(self, tok):
        r'@end'
        if self._in_class_zone:
            tok.value = '}; // ' + str(self._class_name)
            try:
                self.dec_brace()
            except Exception:
                #print '@end and brace counter dirty hack'
                self._brace_counter = 0
            self._in_class_zone = False
        else:
            tok.value = '//@end'
        self.discard_class_name()
        self._last_symbol = ';'
        return tok

    def t_ANY_ATSIGNCLASS(self, tok):
        r'@class'
        tok.value = 'class'
        return tok

    def t_INITIAL_LBRACE(self, tok):
        r'\{'
        self.inc_brace()
        self._last_symbol = '{'
        self._last_word = None
        return tok

    def t_methoddecl_LBRACE(self, tok):
        r'\{|;'
        if tok.value == '{':
            self.inc_brace()
        self._last_symbol = tok.value
        tok.value = ')' + tok.value
        tok.lexer.begin('INITIAL')
        self.discard_method_flags()
        self._last_word = None
        return tok

    def t_ANY_RBRACE(self, tok):
        r'\}'
        if self.brace_counter == 1 and self._in_class_zone:
            return None
        self.dec_brace()
        self._last_symbol = '}'
        return tok

    def t_ANY_LSQBRACKET(self, tok):
        r'\['
        flag = self.method_call_ability()
        self._stack.push(objccall=flag)
        self._last_symbol = '['
        if not flag:
            return tok
        else:
            return None

    def t_ANY_RSQBRACKET(self, tok):
        r'\]'
        if self._stack.objc_call():
            tok.value = ')'
        self._stack.pop()
        self._last_symbol = tok.value
        return tok

    def t_ANY_COMPLEXOP(self, tok):
        r'(([-+*!%<>^=/]|<<|>>)=)|([-+&|><:]{2,2})|\.(\.\.|\*)|->\*?'
        self._last_symbol = tok.value[-1]
        return tok

    def t_ANY_PLUSMINUS(self, tok):
        r'[+-]'
        if self.method_decl_ability():
            self._static_method = tok.lexer.lexdata[tok.lexer.lexpos - 1] == '+'
            tok.lexer.begin('methoddecl')
            return None
        self._last_symbol = tok.value
        return tok

    def t_methoddecl_PARAMCLASS(self, tok):
        r'\(\s*(?P<name>[a-zA-Z_]\w*)(?P<ast>\s*\*)*?\s*\)'
        name = help2dx.to2dx(tok.lexer.lexmatch.group('name'), self.is_header)
        ast = tok.lexer.lexmatch.group('ast')
        tok.value = ('static '
                     if self._static_method and self.is_header else '') \
                    + name + (' ' + str(ast).replace(" ", "") if ast else '')
        return tok

    def t_INITIAL_PARAMCLASS(self, tok):  # type casting patch
        r'\(\s*(?P<name>[a-zA-Z_]\w*)(?P<ast>\s*\*)*?\s*\)'
        name = help2dx.to2dx(tok.lexer.lexmatch.group('name'), self.is_header)
        ast = tok.lexer.lexmatch.group('ast')
        tok.value = '(' + name + ' ' + \
            (str(ast).replace(" ", "") if ast else '') + ')'
        self._last_word = None
        return tok

    def t_methoddecl_METHODPART(self, tok):
        r'(?P<part>[a-zA-Z_]\w*)\s*:(?!:)'
        initial = tok.value = tok.lexer.lexmatch.group('part')
        if not self._1st_part_parsed:
            tok.value += '('
            self._1st_part_parsed = True
            if not self._in_class_zone:
                tok.value = self._class_name + '::' + tok.value
            self._last_word = initial
        else:
            tok.value = ', /*' + tok.value + '*/'
        return tok

    def t_INITIAL_METHODPART(self, tok):
        r'(?P<part>[a-zA-Z_]\w*)\s*:(?!:)'
        if not self._stack.objc_call():
            return tok
        initial = tok.value = tok.lexer.lexmatch.group('part')
        if not self._stack.header_parsed():
            tok.value = help2dx.method2dx(tok.value, self._last_word)
            self._stack.set_header_parsed()
            self._last_word = initial
        else:
            tok.value = ', /*' + tok.value + '*/'
        self._last_symbol = ':'
        return tok

    def t_ANY_SELFPOINT(self, tok):
        r'self\s*\.'
        tok.value = 'this->'
        self._last_symbol = '>'
        return tok

    def t_ANY_COCOSWORD(self, tok):
        r'cocos2d\s*::\s*[a-zA-Z_]\w*'
        tok.value.replace(' ', '')
        return tok

    def t_INITIAL_ID(self, tok):
        r'[a-zA-Z_]\w*'
        initial = tok.lexer.lexmatch.group(0)
        if self._stack.objc_call():
            # object which is got message
            if not self._stack.object_parsed():
                tok.value = help2dx.to2dx(tok.value, prefix=False)
                self._stack.set_object_parsed()
            # no args message
            elif not self._stack.header_parsed() and self.message_ability():
                tok.value = help2dx.method2dx(tok.value, self._last_word)
                self._stack.set_header_parsed()
            else:  # just a parameter name or part of object
                tok.value = help2dx.to2dx(tok.value, prefix=False)
        else:
            tok.value = help2dx.to2dx(tok.value, prefix=self.is_header)
        self._last_symbol = '_'
        self._last_word = initial if initial != 'super' else 'Super'
        return tok

    def t_methoddecl_ID(self, tok):
        r'[a-zA-Z_]\w*'
        if not self._1st_part_parsed:
            tok.value += '('
            if not self._in_class_zone:
                tok.value = self._class_name + '::' + tok.value
        self._last_word = None
        return tok

    # Ignored symbols.
    t_ANY_ignore = ' \t'

    def t_ANY_OTHER(self, tok):
        r'.'
        self._last_symbol = tok.value
        return tok

    def t_ANY_error(self, tok):
        """Error processing."""
        print "Illegal character '%s'" % tok.value[0]
        tok.lexer.skip(len(tok.lexer.lexdata) - tok.lexer.lexpos)

    def console_output(self):
        """Console output: <token_type> <token_value>"""
        if self.is_header and not self._pragma_onced:
            print '#pragma once'
        for tok in self._lexer:
            print tok.type, tok.value

    def console_output2(self):
        """Console output: new unformatted code."""
        if self.is_header and not self._pragma_onced:
            print '#pragma once'
        for tok in self._lexer:
            print tok.value,
            if tok.type == 'NEWLINE':
                print '\t' * self.brace_counter,

    def file_output(self, file_name):
        """File output."""
        with open(file_name, 'w') as out:
            if self.is_header and not self._pragma_onced:
                out.write('#pragma once\n')
            for tok in self._lexer:
                out.write('%s ' % tok.value)
                if tok.type == 'NEWLINE':
                    out.write('\t' * self.brace_counter)

# TODO:
# 1. if/for/while(..) [..] issue
# 2. [[@"some_nsstring" copy] retain]
