#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Simple Cocos2d-to-Cocos2d-x converter."""

# Entry point
if __name__ == '__main__':
    import argparse
    import file_tools
    from v2.to2dx import CocosLexer
#     import sys
    # pylint: disable=line-too-long
    parser = argparse.ArgumentParser(description='Cocos2d to Cocos2d-x-2 code converter.', usage='%(prog)s <path> [arguments]')
    parser.add_argument('path', metavar='FILE_OR_FOLDER', type=str, nargs=1, help='Path to file or folder.')
    parser.add_argument('--rollback', '-r', action='store_true', default=False,
                        help='Rollback backuped files in pointed folder (ignore other flags except subfolders).')
    parser.add_argument('--remove-backup', '-m', action='store_true', default=False,
                        help='Remove backuped files (ignore other flags except rollback and subfolders).')
    parser.add_argument('--debug', '-d', action='store_true', default=False,
                        help='Prints interpreter result in console for the 1st file only and interrupts.')
    parser.add_argument('--backup', '-b', action='store_true', default=False, help='Store old code in *.bak files.')
    parser.add_argument('--subfolders', '-s', action='store_true', default=False, help='Do options in subfolders.')
    args = parser.parse_args()
    if args.rollback:
        file_tools.rollback(args.path[0], args.subfolders)
        quit()
    elif args.remove_backup:
        file_tools.remove_backup(args.path[0], args.subfolders)
        quit()
    file_list = file_tools.get_file_list(args.path[0], args.subfolders)
    if not file_list:
        quit()
    cocos_lexer = CocosLexer()
    cocos_lexer.build()
    cocos_lexer.set_is_header_func(file_tools.is_header)
    for fname in file_list:
        cocos_lexer.feed_from_file(fname)
        if args.debug:
            cocos_lexer.console_output2()
            break
        if args.backup:
            file_tools.make_backup(fname)
        cocos_lexer.file_output(file_tools.get_cpp_file_name_with_remove(fname))
        cocos_lexer.refresh()
        