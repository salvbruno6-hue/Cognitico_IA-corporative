# Hermes Bot Peer Messaging → ELO

## Reconciliation

The Hermes capability is adapted as a bounded message-envelope contract over the existing **ELO Agent Delegation** owner. No second messaging authority or transport is introduced.

## Contract

A peer message carries tenant scope, sender, recipient, stable message identity, content digest and provenance. Durability is required by the candidate contract. Self-delivery is rejected.

The assessment never authorizes or delivers a message: `delivery_permitted=False` even for a valid candidate.

## Boundaries

No Hermes modification, no network transport, no durable database writer, no new agent authority, no execution authorization, no business operation and no automatic promotion. This is candidate evidence only.
