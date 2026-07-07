from app.core.utils import stable_hash


def test_same_input_same_hash():
    assert stable_hash("hello") == stable_hash("hello")


def test_different_inputs_different_hash():
    assert stable_hash("hello") != stable_hash("world")


def test_hash_length_is_16():
    assert len(stable_hash("hello")) == 16


def test_empty_string():
    assert stable_hash("") == stable_hash("")