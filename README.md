# cronhelpers

[![CircleCI](https://circleci.com/gh/ceshine/what-i-did-today-telegram-bot/tree/master.svg?style=svg)](https://circleci.com/gh/ceshine/what-i-did-today-telegram-bot/tree/master)

Cron smarter with these small tools and tips. (WIP)

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

## Tips

### Organizing the Logs

We want to save the outputs of the Cron Jobs on disk in an organized way, so we can review them later if things go wrong.

One of the solutions is to wrap your cron jobs in a shell script that set up the logging for you. Example (it organizes log files in such format: `/tmp/cron_logs/%Y%m/%Y%m%d_%H%M.log`):

```bash
#!/bin/sh
set -e # Exit immediately if a command exits with a non-zero status.
log_dir=/tmp/cron_logs/$(date +'%Y%m')
mkdir -p "$log_dir" || { echo "Can't create log directory '$log_dir'"; exit 1; }
log_file=$log_dir/$(date +'%Y%m%d_%H%M').log
# From now on stderr and stdout steams will be redirected to the log file
exec 2>&1 1>>"$log_file"
# The actual cron job starts here
python myjob.py
cp something_here something_there
echo "It can be whatever that runs in shell."
```

And of course you can choose to run this shell script inside python using [subprocess](https://docs.python.org/3/library/subprocess.html) and use [telegram_wrapper](https://github.com/ceshine/cronhelpers#telegram_wrapper) to monitor its execution. Or you can just monitor the most error-prone part of your job.

This tip comes from this [StackOverflow thread](https://stackoverflow.com/questions/41755437/managing-log-files-created-by-cron-jobs).
