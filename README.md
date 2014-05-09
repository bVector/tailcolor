###### Requirements:
Requires fabulous, sarge, and blessings:

```
pip install fabulous
pip install blessings
pip install sarge
```

###### Usage

Usage: tail -F [file to follow] | tailcolor
(works with most stdin pipes)

###### Known issues
- Lines do not wrap
- Issues with buffered output: If you're writing to a file, 'stdbuf -oL -eL [command]' works well if the command you're piping through doesnt have line buffered output (e.g. tcpdump has -l) http://sarge.readthedocs.org/en/latest/tutorial.html#buffering-issues
