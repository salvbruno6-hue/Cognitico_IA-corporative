# ELO Core Maturity — EVO-03

## Critical criterion

`immutable historical evidence → append-only follow-up → reconstruction/replay`

## Deficiency found

The existing persistent memory contract supported governed admission and retrieval, but did not explicitly protect records classified as historical from re-admission or expiration cleanup, nor provide a canonical reconstruction path for historical follow-ups.

## Correction

The canonical `PersistentMemoryStore` was extended without introducing a second memory authority:

- `kind="historical"` records are immutable;
- duplicate admission of the same historical identity is blocked;
- follow-up is appended as a new `historical_follow_up` record referencing the immutable parent through provenance;
- replay reconstructs the historical chain within tenant/domain scope;
- expiration cleanup cannot delete historical records.

## Operational evidence

A dedicated GitHub Actions test will execute against the exact commit and verify:

1. historical admission;
2. duplicate mutation rejection;
3. append-only follow-up;
4. exact replay order and provenance linkage;
5. tenant/domain isolation;
6. preservation of historical evidence after expiration cleanup.

Final `PASS` requires GitHub Actions evidence tied to the exact tested commit plus canonical regression, merge, `ON_MAIN`, and post-merge regression.

## Boundaries

This is a repository-local maturity test. It does not claim production database validation or external-provider evidence. Production persistence remains replaceable behind the existing memory contract.

## Status

`EXECUTION_REQUESTED`
