# Linux Command Practice — November 2, 2026

## Day 101: Linux by Task, Not by Memory

Initial recall score: 5/18

## Commands Reviewed

| Task | Command |
|---|---|
| List hidden files | `ls -la` |
| Find Python files | `find . -type f -name '*.py'` |
| Search text | `grep -in "error" app.log` |
| Check permissions | `stat -c '%a %n' file` |
| Change permissions | `chmod 700 script.sh` |
| List processes | `ps aux` |
| Check listening ports | `sudo ss -tulnp` |
| Check SSH service | `systemctl status ssh` |
| View service logs | `journalctl -u ssh -n 50` |
| Check disk usage | `du -h --max-depth=1 /var` |

## Job Control

- `command &` — run a command in the background.
- `fg` — bring a background job into the foreground.

## What I Struggled With

I remembered some command names but struggled to
recall their flags and complete syntax independently.

My weakest areas were:
- File management
- Permissions
- Process and port inspection
- Service management
- Disk usage

## November Learning Goal

Improve Linux command recall by practicing real tasks
instead of memorizing commands individually.
