#!/usr/bin/env python3

import re
import datetime

class Tag(object):
    def __init__(self, name, start, end):
        self.name = name
        self.start = start
        self.end = end
    
    @classmethod
    def from_match(cls, re_match):
        return cls(re_match[1], re_match.start(), re_match.end())

class ProjectTag(Tag):
    def __str__(self):
        return "+" + self.name

class ContextTag(Tag):
    def __str__(self):
        return "@" + self.name

class KeyValueTag(Tag):
    def __init__(self, key, value, start, end):
        super().__init__(key, start, end)
        self.value = value
    
    @property
    def key(self):
        return self.name

    def __str__(self):
        return self.key + ":" + self.value
    
    @classmethod
    def from_match(cls, re_match):
        return cls(re_match[1], re_match[2], re_match.start(), re_match.end())

completion_re = r"(?P<completion>x\s)?"
priority_re = r"(?P<priority>\([A-Z]\)\s)?"
date_re = r"[0-9]{4}-[0-9]{2}-[0-9]{2}"
completion_date_re = r"(?P<completion_date>"+date_re+r"\s)"
creation_date_re = r"(?P<creation_date>"+date_re+r"\s)"
dates_re = r"("+completion_date_re+r"?"+creation_date_re+r")?"
content_re = r"(?P<description>.+)"
task_regex = r"^"+completion_re+priority_re+dates_re+content_re+r"$"
project_tag_re = r"\s\+(\S+)"
context_tag_re = r"\s@(\S+)"
keyvalue_tag_re = r"\s(\S+):(\S+)"

def split_date_string(date_string):
    return [ int(x) for x in date_string.split("-") ]

class Task(object):
    def __init__(self, content_string):
        self.content = content_string
    
    @property
    def regex_match(self):
        return re.match(task_regex, self.content)
    
    def regex_group(self, group_name):
        return self.regex_match.group(group_name)
    
    @property
    def is_completed(self):
        return self.regex_group("completion") is not None
    
    def __raw_priority(self):
        return self.regex_group("priority")
    
    def has_priority(self):
        return self.__raw_priority() is not None

    @property
    def priority(self):
        raw_priority = self.__raw_priority()
        if raw_priority is None:
            return None
        return raw_priority[1:2]
    
    def __raw_completion_date(self):
        return self.regex_group("completion_date")

    def has_completion_date(self):
        return self.__raw_completion_date() is not None

    @property
    def completion_date(self):
        raw_date = self.__raw_completion_date()
        if raw_date == None:
            return None
        return datetime.date(*split_date_string(raw_date))
    
    def __raw_creation_date(self):
        return self.regex_group("creation_date")
    
    def has_creation_date(self):
        return self.__raw_creation_date() is not None

    @property
    def creation_date(self):
        raw_date = self.__raw_creation_date()
        if raw_date == None:
            return None
        return datetime.date(*split_date_string(raw_date))
    
    def __raw_description(self):
        return self.regex_group("description")

    @property
    def description(self):
        return self.__raw_description()
    
    @property
    def project_tags_iter(self):
        return map(ProjectTag.from_match, re.finditer(project_tag_re, self.description))
    
    @property
    def project_tags(self):
        return list(map(lambda t: t.name, self.project_tags_iter))
    
    @property
    def context_tags_iter(self):
        return map(ContextTag.from_match, re.finditer(context_tag_re, self.description))

    @property
    def context_tags(self):
        return list(map(lambda t: t.name, self.context_tags_iter))
    
    @property
    def keyvalue_tags_iter(self):
        return map(KeyValueTag.from_match, re.finditer(keyvalue_tag_re, self.description))

    @property
    def keyvalue_tags(self):
        return list(map(lambda t: t.key, self.keyvalue_tags_iter))

    def value_for_key(self, key):
        try:
            tag = next(t for t in self.keyvalue_tags_iter if t.key == key)
            return tag.value
        except StopIteration:
            raise KeyError("No key value tag with %s key is present." % key)
    
    def __getitem__(self, key):
        return self.value_for_key(key)
    
    def format(self, format_string):
        return format_string.format(task=self)

class TodoList(object):
    def __init__(self, stream):
        self.stream = stream
    
    def __iter__(self):
        # Set the stream back to the beginning
        self.stream.seek(0, 0)
        for line in self.stream:
            yield Task(line)