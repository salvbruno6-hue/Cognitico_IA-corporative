# Checkpoint implementation-loop measurement

The checkpoint candidate now has a deterministic controlled measurement harness.

Baseline:
- no checkpoint/restore path;
- interrupted state is unavailable;
- recovery success is measured as 0.0.

Adapted:
- uses the existing ELO state-recovery capability;
- checkpoint and restore are performed in memory;
- tenant continuity and integrity are verified;
- recovery success is measured as 1.0.

Metric: recovery_success. Direction: maximize.

The harness repeats both probes and reports repeatability. It does not promote the candidate or mutate canonical state.

A measured improvement is evidence for the implementation loop, not permission to deploy or promote the capability.
