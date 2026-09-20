# ELO implementation loop — evaluation evidence adapter

The implementation loop now has an explicit translation boundary between an existing Hermes candidate measurement and the immutable ImplementationEvidence contract.

The adapter:
- reuses the existing candidate owner and measured baseline/adapted values;
- preserves the existing evaluation result;
- requires explicit metric directions;
- requires caller-supplied provenance references;
- requires an explicit boundary-integrity result;
- rejects candidate/measurement identity mismatches.

It does not create provenance, infer gain, promote candidates, deploy anything, or mutate canonical ELO state.

Therefore an evaluation can be converted into loop evidence without creating a second evaluation authority. A missing provenance reference remains incomplete evidence and cannot satisfy the Start Gate.
