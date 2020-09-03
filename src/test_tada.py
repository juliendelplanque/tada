#!/usr/bin/env python3

import datetime
import pytest

import tada

def test_is_completed_task():
    task = tada.Task("x this is a completed task")

    assert task.is_completed

def test_not_is_completed_task():
    task = tada.Task("this is incomplete task")

    assert not task.is_completed

def test_priority():
    task = tada.Task("(A) this is prioritary task")

    assert task.has_priority()
    assert task.priority == 'A'

def test_no_priority():
    task = tada.Task("this is non-prioritary task")

    assert not task.has_priority()
    assert task.priority is None

def test_completion_date():
    task = tada.Task("2020-09-02 2020-09-01 this is non-prioritary task")

    assert task.has_completion_date()
    assert task.completion_date == datetime.date(2020, 9, 2)

def test_no_completion_date():
    task = tada.Task("2020-09-01 this is non-prioritary task")

    assert not task.has_completion_date()
    assert task.completion_date is None

def test_creation_date():
    task = tada.Task("2020-09-01 this is non-prioritary task")

    assert task.has_creation_date()
    assert task.creation_date == datetime.date(2020, 9, 1)

def test_no_creation_date():
    task = tada.Task("this is non-prioritary task")

    assert not task.has_creation_date()
    assert task.creation_date is None

def test_description():
    task = tada.Task("a simple description")

    assert task.description == "a simple description"

def test_description_with_creation_date():
    task = tada.Task("2020-09-01 a simple description")

    assert task.description == "a simple description"
    assert task.creation_date == datetime.date(2020, 9, 1)

def test_description_with_dates():
    task = tada.Task("2020-09-02 2020-09-01 a simple description")

    assert task.description == "a simple description"
    assert task.completion_date == datetime.date(2020, 9, 2)
    assert task.creation_date == datetime.date(2020, 9, 1)

def test_description_with_completion():
    task = tada.Task("x a simple description")

    assert task.description == "a simple description"
    assert task.is_completed

def test_project_tag_str():
    tag = tada.ProjectTag("foo", 0, 2)

    assert str(tag) == "+foo"

def test_context_tag_str():
    tag = tada.ContextTag("foo", 0, 2)

    assert str(tag) == "@foo"

def test_keyvalue_tag_str():
    tag = tada.KeyValueTag("due", "2020-10-02", 0, 2)

    assert str(tag) == "due:2020-10-02"

def test_project_tags_iter():
    task = tada.Task("a simple description with +project +tags")

    for t in task.project_tags_iter:
        assert type(t) == tada.ProjectTag

def test_project_tags():
    task = tada.Task("a simple description with +project +tags")

    assert task.project_tags == ["project", "tags"]

def test_no_project_tags():
    task = tada.Task("a simple description")

    assert task.project_tags == []

def test_context_tags_iter():
    task = tada.Task("a simple description with @context @tags")
    
    for t in task.context_tags_iter:
        assert type(t) == tada.ContextTag

def test_context_tags():
    task = tada.Task("a simple description with @context @tags")

    assert task.context_tags == ["context", "tags"]

def test_no_context_tags():
    task = tada.Task("a simple description")

    assert task.context_tags == []

def test_keyvalue_tags_iter():
    task = tada.Task("a simple description with due:2020-01-01 foo:bar")
    
    for t in task.keyvalue_tags_iter:
        assert type(t) == tada.KeyValueTag

def test_keyvalue_tags():
    task = tada.Task("a simple description with due:2020-01-01 foo:bar")

    assert task.keyvalue_tags == ["due", "foo"]

def test_no_keyvalue_tags():
    task = tada.Task("a simple description")

    assert task.keyvalue_tags == []

def test_value_for_key():
    task = tada.Task("a simple description with due:2020-01-01 foo:bar")

    assert task.value_for_key("due") == "2020-01-01"
    assert task.value_for_key("foo") == "bar"

def test_value_for_not_found_key():
    task = tada.Task("a simple description")
    with pytest.raises(KeyError):
        task.value_for_key("due")

def test_empty_task():
    task = tada.Task()

    assert not task.is_completed
    assert not task.has_priority()
    assert task.priority is None
    assert not task.has_completion_date()
    assert task.completion_date is None
    assert not task.has_creation_date()
    assert task.creation_date is None
    assert not task.project_tags
    assert not task.context_tags
    assert not task.keyvalue_tags
    assert task.description == ""

def test_change_task_completion():
    task = tada.Task("Cool task.")

    assert not task.is_completed

    task.is_completed = True

    assert task.is_completed
    assert task.content == "x Cool task."

    task.is_completed = False

    assert not task.is_completed
    assert task.content == "Cool task."