# First implementation-loop candidate: checkpoint

The checkpoint candidate is now composed end-to-end from existing ELO components:

1. bounded Hermes candidate;
2. controlled checkpoint measurement;
3. immutable ImplementationEvidence;
4. Start Gate evidence contract;
5. governed implementation loop;
6. ELO Review as the final result of the probe.

Expected controlled result:
- baseline recovery_success = 0.0;
- adapted recovery_success = 1.0;
- direction = maximize;
- repeatable = true;
- regressions = none;
- boundary integrity = true;
- loop decision = READY_FOR_ELO_REVIEW.

The probe deliberately does not set ELO approval. Therefore it cannot return IMPLEMENTATION_AUTHORIZED and cannot mutate canonical state.
