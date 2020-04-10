import pytest
from cronhelpers.telegram_wrapper import telegram_wrapper, telegram


def test_basic(mocker):
    mocker.patch('telegram.Bot')

    @telegram_wrapper("dummy_token", "dummy_id", name="smoketest", send_at_start=True, send_on_success=True)
    def simple_func(arg):
        return arg

    ret = simple_func("test value")
    assert ret == "test value"
    assert telegram.Bot.called is True
    assert telegram.Bot.call_args[1]["token"] == "dummy_token"
    assert telegram.Bot().send_message.call_count == 2
    start_call_dict = telegram.Bot().send_message.call_args_list[0][1]
    assert start_call_dict["chat_id"] == "dummy_id"
    assert "smoketest has started" in start_call_dict["text"]
    success_call_dict = telegram.Bot().send_message.call_args_list[1][1]
    assert "smoketest has completed" in success_call_dict["text"]
    assert "Main call returned value: test value" in success_call_dict["text"]


def test_only_on_error(mocker):
    mocker.patch('telegram.Bot')

    @telegram_wrapper("dummy_token", "dummy_id", name="onerror", send_at_start=False, send_on_success=False)
    def simple_func(arg):
        return arg

    ret = simple_func("test value")
    assert telegram.Bot().send_message.called is False

    @telegram_wrapper("dummy_token", "dummy_id", name="onerror", send_at_start=False, send_on_success=False)
    def failed_func(arg):
        raise ValueError("this is an error")
        return arg

    with pytest.raises(ValueError) as excinfo:
        ret = failed_func("test value")
    assert telegram.Bot().send_message.call_count == 1
    call_dict = telegram.Bot().send_message.call_args[1]
    assert "onerror has crashed" in call_dict["text"]
    assert "ValueError" in call_dict["text"]


def test_only_no_at_start(mocker):
    mocker.patch('telegram.Bot')

    @telegram_wrapper("dummy_token", "dummy_id", name="noAtStart", send_at_start=False, send_on_success=True)
    def simple_func(arg):
        return arg

    ret = simple_func("test value")
    assert telegram.Bot().send_message.call_count == 1
    call_dict = telegram.Bot().send_message.call_args[1]
    assert "noAtStart has completed" in call_dict["text"]
