# ECEA-5316 Assignment 2: Sequencer Generic

Emulates the Example 0 timing diagram (`sched-example-0-feasible-above-LUB-disharmonic`) with three `SCHED_FIFO` service threads and Fibonacci fake workloads. Compare RM, EDF, and LLF traces from the course spreadsheet in Cheddar.

## Example 0 schedule (time unit = 10 ms)

| Service | Period T | Execution C | Deadline | Sequencer rate |
| --- | --- | --- | --- | --- |
| Sequencer | 1 | — | — | 100 Hz |
| S1 / Thread 1 | 2 (20 ms) | 1 (10 ms) | T | every 2nd tick (50 Hz) |
| S2 / Thread 2 | 5 (50 ms) | 1 (10 ms) | T | every 5th tick (20 Hz) |
| S3 / Thread 3 | 15 (150 ms) | 2 (20 ms) | T | every 15th tick (6.67 Hz) |

Hyperperiod LCM(2, 5, 15) = 30 time units (300 ms).

Utilization: `U = 1/2 + 1/5 + 2/15 ≈ 0.833`, which is **above** the n=3 RM LUB (~0.780) but still feasible (U ≤ 1). Assignment 1 used T2=10 (U ≈ 0.733, below LUB); this chart raises S2’s rate so RM no longer has a LUB guarantee.

## Build

```bash
make seqgenex0
```

## Run

Needs `SCHED_FIFO` privileges. All four threads are pinned to one CPU core.

```bash
sudo ./seqgenex0
./capture-syslog.sh assignment2-syslog.txt
```

The default run is 2400 sequencer periods at 100 Hz (about 24 seconds).

## Required syslog format

Every program log is tagged `[COURSE:1][ASSIGNMENT:2]`. Service lines look like:

```text
[COURSE:1][ASSIGNMENT:2]: Thread 1 start 3 @ 0.040000 sec on core 3
```

`capture-syslog.sh` writes `uname -a` as the first line of the submission file, then the tagged events.

To remove build artifacts:

```bash
make clean
```
