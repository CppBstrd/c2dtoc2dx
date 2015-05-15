#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Helpful tools for Cocos2d to Cocos2d-x translator."""

import re

DICT2DX = {
        'BOOL' : 'bool',
        'CGPoint' : 'CCPoint',
        'CGPointEqualToPoint' : 'CCPointEqualToPoint',
        'CGPointZero' : 'CCPointZero',
        'CGRect' : 'CCRect',
        'CGRectContainsPoint' : 'CCRectContainsPoint',
        'CGRectMake' : 'CCRectMake',
        'CGSize' : 'CCSize',
        'CGSizeMake' : 'CCSizeMake',
        'FALSE' : 'false',
        'id' : 'CCObject *',
        'nil' : 'nullptr',
        'NO' : 'false',
        'NSArray' : 'CCArray',
        'NSAssert' : 'CCAssert',
        'NSDictionary' : 'CCDictionary',
        'NSLog' : 'CCLog',
        'NSMutableArray' : 'CCArray',
        'NSMutableDictionary' : 'CCDictionary',
        'NSNumber' : 'CCInteger',
        'NSObject' : 'CCObject',
        'NSSet' : 'CCSet',
        'NSString' : 'CCString',
        'NSUserDefaults' : 'CCUserDefault',
        'NSValue' : 'CCValue',
        'NULL' : 'nullptr',
        'SEL' : '@selector',
        'self' : 'this',
        'super' : '__SUPER_CLASS__',
        'TRUE' : 'true',
        'UIEvent' : 'CCEvent',
        'UITouch' : 'CCTouch',
        'YES' : 'true',
        }

CC_MACROS = ('CCAssert', 'ccc3', 'CCLog', 'ccp', 'CCPointZero',
             'CCPointEqualToPoint', 'CCRectContainsPoint',
             'CCRectMake', 'CCSizeMake',)

CREATE_METHODS = (
                  'actions',
                  'actionWithAction',
                  'actionWithDuration',
                  'actionWithTarget',
                  'array',
                  'arrayWithObjects',
                  'labelWithString',
                  'node',
                  'numberWithInt',
                  'spriteWithFile',
                  'stringWithCString',
                  'stringWithString',
                  )

# cocos2d_method_name : cocos2dx_method_name
STATIC_METHODS = {
                  'spriteWithSpriteFrameName' : 'createWithSpriteFrameName',
                  'standardUserDefaults' : 'sharedUserDefault',
                  'stringWithFormat' : 'createWithFormat',
                  'stringWithContentsOfFile' : 'createWithContentsOfFile',
                  'valueWithCGPoint' : '<CCPoint>valueWithValue',
                  }

IGNORED_HEADERS = (
                   'Foundation/Foundation.h',
                   )

def to2dx(some_id, prefix=False):
    """Returns correspondence name if possible."""
    ans = DICT2DX.get(some_id, some_id)
    if prefix and ans[0:2].upper() == 'CC' and ans not in CC_MACROS:
        ans = 'cocos2d::' + ans
    return ans

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
