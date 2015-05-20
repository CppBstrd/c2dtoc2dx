#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Dictionaries and sets with identifiers for the conversion."""

OBJC_TO_CPP = {
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
        
V2_TO_V3 = {
        'CCArray' : 'Vector',
        'CCDictionary' : 'Map',
        'CCObject *' : 'Ref *',
        'CCPointZero' : 'Point::ZERO',
}

DEPRECATED_V3 = (
        'CCPointEqualToPoint', 'CCRectContainsPoint', 'CCRectMake', 'CCSizeMake', 'CCString',
)

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
