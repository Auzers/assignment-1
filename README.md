# 11-768 Assignment 1: Build an Agent Harness

This repository contains the starter code and instructions for Assignment 1 for 11-768, the Carnegie Mellon University course on AI Agents. You can find the problem statement, along with instructions for setup and notes on grading in [ASSIGNMENT.md](ASSIGNMENT.md)

Authors: Weiwei Sun and Saujas Vaduguru, with feedback from 11-768 course staff (instructors Daniel Fried and Graham Neubig, and TAs Aditya Soni, Andy Liu, Apurva Gandhi, Demi Wang, Jiarui Liu, and Yueqi Song).

## Part 2 local experiment record

The two Django trajectories use the vendored `django__django-15368` SWE-bench
instance. The baseline retained the full history; the compacted run used a
6,000-token compaction threshold.

| Metric | Baseline | Compacted run |
| --- | ---: | ---: |
| Agent action calls | 26 | 3 |
| Compaction calls | 0 | 1 |
| Prompt tokens, all model calls | 274,081 | 15,278 |
| Completion tokens, all model calls | 6,972 | 909 |
| Total tokens, all model calls | 281,053 | 16,187 |

The compacted run triggered after action 3. The active-context estimate fell
from 6,781 to 2,708 tokens (a reduction of 4,073 tokens, about 60%). The
compaction request itself used 4,123 prompt tokens and 172 completion tokens.

These totals are not a controlled cost comparison: the two stochastic runs
took different numbers of agent actions. In particular, the available patch
artifact predates the compacted trajectory, and the compacted run did not
produce a new patch. It therefore does not yet establish that a compacted run
can finish the SWE-bench repair. The evaluation command did apply the earlier
candidate patch and the SWE-bench test patch in a fresh Modal sandbox.
