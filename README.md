## Installation:

```
pip install tailcolor
```


## Requirements:
Requires fabulous, sarge, and blessings:

```
pip install fabulous
pip install blessings
pip install sarge
```

## Usage

```
Usage patterns: 
  tail -F [file to follow] | tailcolor
  tail -F [file to follow] | tailflash
  tail -F [file to follow] | tailrain
  
tail -F  can be replaced with any command that provides stdout
  
```

## Known issues
- Issues with buffered output: If you're writing to a file, 'stdbuf -oL -eL [command]' works well if the command you're piping through doesnt have line buffered output (e.g. tcpdump has -l) http://sarge.readthedocs.org/en/latest/tutorial.html#buffering-issues
- Minor graphical glitches when exiting or when the piped process prints to stdout ( pipe stdout to /dev/null fixes )
