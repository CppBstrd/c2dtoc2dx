#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Helpful tools for Cocos2d to Cocos2d-x translator."""
from data2dx import *
import re

def to2dx2(some_id, prefix=False):
    return to2dx(some_id, prefix, True)

def to2dx3(some_id, prefix=False):
    return to2dx(some_id, prefix, False)

def to2dx(some_id, prefix=False, use_v2=False):
    """Returns correspondence name if possible."""
    ans = OBJC_TO_CPP.get(some_id, some_id)
    starts_with_cc = ans[0:2].upper() == 'CC'
    if use_v2:
        if prefix and starts_with_cc and ans not in CC_MACROS:
            ans = 'cocos2d::' + ans
    else:
        ans = getV3Name(ans)
        if prefix and starts_with_cc:
            ans = 'cocos2d::' + ans
    return ans
    
def getV3Name(some_id):
    """Returns Cocos2d-x-v-3.* name."""
    if some_id in DEPRECATED_V3:
        return some_id
    elif some_id in V2_TO_V3:
        return V2_TO_V3[some_id]
    elif some_id.startswith('CC'):
        return some_id[2:]
    else:
        return some_id
    

def method2dx(method_name, last_word):
    """Returns correspondence method with prefix."""
    if method_name in CREATE_METHODS:
        return '::create('
    elif method_name in STATIC_METHODS:
        return '::' + STATIC_METHODS[method_name] + '('
    else:
        return ('::' if last_word[0].isupper() and \
                last_word != last_word.upper() else '->') + method_name + '('

def ignored_header(header_name):
    """Checks if file is unused in C++/Cocos2d-x."""
    return header_name in IGNORED_HEADERS

def update_format(str_value):
    """%@ -> %s"""
    def repl(match_obj):
        """%@ -> %s match object function."""
        count = len(match_obj.group(1))
        return count * r'%' + 's' if count % 2 else match_obj.group(0)
    return re.sub(r'(?<!%)(%+)@', repl, str_value)
