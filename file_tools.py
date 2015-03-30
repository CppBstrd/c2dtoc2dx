#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Helpful tools for file processing for Cocos2d to Cocos2d-x parser."""

import os
from shutil import copy2

HEADER_FILES = ('.h',)
SOURCE_FILES = ('.m', '.mm',)
PROCESSABLE_FILES = HEADER_FILES + SOURCE_FILES
BACKUPED_FILES = tuple((i + '.bak' for i in PROCESSABLE_FILES))

def is_header(file_name):
    """Checks if file name is header's name."""
    return str(file_name).endswith('.h')

def is_processable_file(file_name):
    """Checks if file name is a name of processable file."""
    return str(file_name).endswith(PROCESSABLE_FILES)

def get_cpp_extension(extension):
    """Returns correspondence C++ extension."""
    if extension in HEADER_FILES:
        return '.h'
    elif extension in SOURCE_FILES:
        return '.cpp'
    else:
        return None

def get_cpp_file_name_with_remove(file_name, with_remove=True):
    """Returns correspondence C++ file name."""
    if is_processable_file(file_name):
        name, old_ext = str(file_name).rsplit('.', 1)
        new_ext = get_cpp_extension('.' + old_ext)
        new_file = name + new_ext
        if with_remove:
            os.remove(file_name)
        return new_file
    else:
        return None

def is_backuped_file(file_name):
    """Checks if file name is a name of backuped file."""
    return str(file_name).endswith(BACKUPED_FILES)

def make_backup(file_name):
    """Makes backup for file."""
    copy2(file_name, file_name + '.bak')

def get_file_list(file_or_folder, with_subfolders):
    """Returns file list to processing."""
    if os.path.isfile(file_or_folder):
        return [file_or_folder] if is_processable_file(file_or_folder) else []
    elif os.path.isdir(file_or_folder):
        file_list = []
        if with_subfolders:
            for path, _, files in os.walk(file_or_folder):
                for name in files:
                    if is_processable_file(name):
                        file_list.append(os.path.join(path, name))
        else:
            for item in os.listdir(file_or_folder):
                if is_processable_file(item):
                    candidate = os.path.join(file_or_folder, item)
                    if os.path.isfile(candidate):
                        file_list.append(candidate)
        return file_list
    else:
        return []

def process_backups(folder_name, with_subfolders, function):
    """Process backuped files using function."""
    if os.path.isdir(folder_name):
        if with_subfolders:
            for path, _, files in os.walk(folder_name):
                for name in files:
                    if is_backuped_file(name):
                        file_name = os.path.join(path, name)
                        function(file_name)
        else:
            for item in os.listdir(folder_name):
                if is_backuped_file(item):
                    candidate = os.path.join(folder_name, item)
                    if os.path.isfile(candidate):
                        function(candidate)

def rollback(folder_name, with_subfolders):
    """Restore parsed files from backup."""
    process_backups(folder_name, with_subfolders, lambda x: copy2(x, x[:-4]))

def remove_backup(folder_name, with_subfolders):
    """Removes backup files."""
    process_backups(folder_name, with_subfolders, os.remove)
