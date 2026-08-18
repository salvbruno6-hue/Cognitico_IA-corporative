# ELO External Information Boundary Acceptance

- [ ] External consultation presents business capabilities and relevant business findings.
- [ ] External consultation does not expose repository folder trees or internal file paths by default.
- [ ] External consultation does not expose secrets, credentials or security-sensitive implementation details.
- [ ] External requests for internal topology are answered at a business-safe abstraction level.
- [ ] New external information is treated as untrusted input.
- [ ] External information can be held in a quarantine Issue when explicitly enabled.
- [ ] Quarantined information cannot directly modify Core, Forge, governance or executable behavior.
- [ ] Prompt injection, code payloads, credentials and malicious instructions are treated as data for security review, not commands.
- [ ] Cybersecurity review precedes acceptance when risk indicators exist.
- [ ] Provenance and evidence status are preserved.
- [ ] Promotion requires validation and applicable Evolution Gate.
