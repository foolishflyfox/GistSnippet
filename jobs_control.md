Commands:

- `./tst.py &`: run in background
- `nohup ./tst.py &`: don't print output in stdout, and set the parent process as #0 process.`nohup` means **No hangup signal**.
- `setsid ./tst.py &`: print output in stdout, set the parent process as #1 process.
- `disown %1`: change the parent process of a background process
- hot key `ctrl+z`: suspend foreground process
- `bg %1`: trun foreground job #1 to background
- `bg`: trun all foreground job to background
- `fg %1`: trun background job to foreground
- `fg`: trun all background job to foreground
- `kill -9 %1`: kill job #1
- `ps -ef`: this command will show the ppid




For example, we have a python script named tst.py like following:

```python
#!/usr/bin/env python
  
import time

for i in range(1000):
    with open('info.log', 'a') as f:
        f.write(str(i))
        print(i)
        time.sleep(1.5)
```

Note: All the following experiments are tested with ssh remote connection:

## Normal running

The process tree of this script: 
*python ./tst.py* -> *-zsh* -> *sshd: linux_fhb@pts/1* -> *sshd: linux_fhb[priv]* -> */usr/sbin/sshd -D* -> */sbin/init splash* -> 0

## Questions & Answers

**Q1: How to run a background program?**

A1: Just add an ampersand at the end of command. e.g. `./tst.py &`. 

**Q2: How to turn the foreground process into a background process?**

A2: You shoud take two steps.
1. Suspend foreground process with hot key `ctrl + z`, and the terminal will print like **[1]  + 13158 suspended  ./tst.py**,
the first number **1** means the job number, and the second number **13158** is the process pid.
2. Run `bg` command : `bg %1`, the **1** is the job number you want run at background, if you want run all the jobs, run `bg`.

**Q3: How to turn the background process into a foreground process?**

A3: Run `fg` command : `fg %1`, if you want turn all jobs to foreground, run command `fg`.

## Set process to the son of #0 process

- with nohup command: `nohup ./tst.py &`

- with setsid command: `setsid ./tst.py &`

- set system process as parent process of a background process: `disown %1`

Note: change the parent process with `disown` won't change the workspace directory.

