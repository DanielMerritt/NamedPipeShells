A script that can be used to gain a pty from a web shell without a reverse connection.

Forked from IPPsec: https://www.youtube.com/watch?v=k6ri-LFWEj4

To use, upload the web shell and then run:

linux_named_pipe_shell.py &lt;url of web shell&gt;

Then run /usr/bin/script -qc /bin/bash /dev/null or python3 -c 'import pty; pty.spawn("/bin/bash")' to gain pty.
