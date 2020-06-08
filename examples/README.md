## Testing how the algorithm scales


## Objectifs 
The script "checker" should works on verry large dataset . I created a script that create a dataset with 500 subjects and 1 sessions in each subject and see how long it takes to run

# Table of Contents
0. [Objectifs](#Objectifs)
1. [Time benchmark](#Time-benchmark)


## ## Time benchmark
-   **real** - (wall clock time) is the time from start to finish of the call. It is the time from the moment you hit the `Enter` key until the moment the command is completed.
-   **user** - amount of CPU time spent in user mode.
-   **system** - amount of CPU time spent in kernel mode


number of subject |user time| system time |total
:---|:---|:---|:---|:---|
1| 0,03s |0,00s  |0,020s
10| 0,04s| 0.00  | 0,037s
50| 0,050s |0,00s  |0,051s
100|  0,070s |  0,00s  |  0,072s
150| 0,090s | 0,01s |0,099s
200| 0,10s | 0,02s  |0,130s
500|0,46s| 0,02s  |0,488s

![Plot](https://ibb.co/7vgm7Zb)
we can see that the script is running well in despite the number of subject that increase
