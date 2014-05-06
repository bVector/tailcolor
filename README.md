Requires fabulous and blessings:

pip install fabulous

pip install blessings



Usage: tailcolor.py [file to follow]


Works best with line-buffered output.




If you're writing to a file, 'stdbuf -oL -eL [command]' works well if the command doesnt have line buffered output (tcpdump has -l)
