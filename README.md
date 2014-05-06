###### Requirements:
Requires fabulous and blessings:

```
pip install fabulous
pip install blessings
```

###### Usage

Usage: tailcolor.py [file to follow]

###### Known issues
- Lines do not wrap
- Hangs with some non-line-buffered output: If you're writing to a file, 'stdbuf -oL -eL [command]' works well if the command doesnt have line buffered output (tcpdump has -l)
