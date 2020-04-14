# cronhelpers

[![CircleCI](https://circleci.com/gh/ceshine/what-i-did-today-telegram-bot/tree/master.svg?style=svg)](https://circleci.com/gh/ceshine/what-i-did-today-telegram-bot/tree/master)

Cron smarter with these small tools. (WIP)

## List of Tools

### telegram_wrapper

Send a message to you via a Telegram bot when a cron job has started, and/or a cron job has crashed, and/or a cron job has finished successfully. Suitable for a small set of cron jobs. **You need to wrap your cron job inside a Python function.**

Example usage:

```python
from cronhelpers import telegram_wraooer

# This one only sends a message when the cron job failed
@telegram_wrapper(
    "your_token", "your_chat_id", name="jobName",
    send_at_start=False, send_on_success=False)
def simple_func(arg):
    return arg
```

(This is a modified version of telegram_sender from [huggingface/knockknock](https://github.com/huggingface/knockknock/blob/master/knockknock/telegram_sender.py). The knockknock is targeted at the machine learning training scenario. I simply made it more relevant to cron jobs and added a few parameters.)
