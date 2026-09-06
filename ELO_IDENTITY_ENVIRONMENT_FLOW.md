# ELO — Identity, Environment and Governed Execution Flow

## Objective

Establish one coherent flow for ADM, SPECIALIST and VISITOR without treating a ChatGPT session, a GitHub connection, an email or a natural-language request as sufficient authority by itself.

## Security boundary

```text
ChatGPT/session
      |
      v
external authentication / identity assertion
      |
      v
ELO operator binding or governed external session
      |
      +-------------------+-------------------+
      |                   |                   |
     ADM             SPECIALIST           VISITOR
      |                   |                   |
 internal domain     company domain      company domain
      |                   |                   |
 GitHub scoped       contribution        consultation
 repository          + learning gate
      |                   |
 commit/PR              commit* 
      |                   |
 operational merge      Evolution Gate
      |                   |
 GitHub ruleset         PR / governed merge
```

`*` Specialist commit capability is limited to the repository and contribution area explicitly authorized by the external permission layer and ELO scope. It never grants direct Core promotion or merge authority.

## ADM establishment

ADM is established once through an explicit authentication ceremony and remains active as a governed operator binding until revoked or expired by policy.

### Same device

```text
ELO on phone
  -> Authorize as ADM
  -> direct authentication flow
  -> external identity provider authenticates the operator
  -> ELO validates the returned identity assertion
  -> ELO creates/activates the operator binding
```

No QR is required when the authentication and ELO session are on the same device.

### Different devices

```text
ELO on computer
  -> short-lived QR challenge
  -> phone opens the authorization flow
  -> external identity provider authenticates the operator
  -> ELO validates the returned identity assertion
  -> ELO creates/activates the operator binding
```

The QR/challenge is a bootstrap mechanism only. It is not a permanent credential and is not requested for every merge.

## Identity requirements

An ADM binding requires:

- authenticated external identity;
- stable provider subject;
- matching GitHub identity subject;
- explicit repository scope;
- explicit ELO capabilities;
- active binding state.

A challenge alone never grants ADM.

## Default external behavior

If an external identity cannot prove an authorized specialist or ADM binding, ELO fails closed to VISITOR.

```text
unproven identity -> VISITOR
proven specialist -> SPECIALIST
proven operator binding -> ADM
```

## Capabilities

### ADM standard binding

- consultation;
- specialist contribution support;
- commit;
- pull request creation;
- operational merge;
- internal architecture visibility within authorized scope.

Structural changes are not authorized by the standard ADM operational binding. They require a separate governed authorization path.

### SPECIALIST

- company/domain consultation;
- evidence and feedback;
- governed contribution;
- commit only where explicitly authorized.

The specialist cannot:

- merge;
- modify Core directly;
- modify canonical memory directly;
- change identity or security policy;
- manage permissions;
- access unrelated repositories;
- expose internal ELO architecture.

### VISITOR

- company/domain consultation only.

Visitor has no repository write, PR, merge or internal-architecture capability.

## Learning flow

```text
SPECIALIST
  -> feedback / evidence / proposal
  -> governed learning area
  -> provenance and validation
  -> learning candidate
  -> Evolution Gate
  -> PR
  -> ELO review
  -> governed merge
  -> consolidated knowledge
```

A specialist contribution is never treated as consolidated knowledge merely because it was committed.

## Repository boundary

ELO cannot revoke GitHub permissions already granted to a credential. Therefore repository isolation must also be enforced by GitHub permissions.

ELO must deny use of any repository outside the operator/specialist repository scope, even if the underlying credential happens to possess broader GitHub privileges.

## Structural protection

Changes to identity, security, governance, access policy, Evolution Gate or equivalent trust-boundary controls are structural. They must not be self-approved through the normal operational merge path.

## Required negative tests

1. Unauthenticated external session -> VISITOR.
2. Natural-language claim of ADM -> no privilege elevation.
3. Authenticated but unbound GitHub identity -> no ADM.
4. Specialist attempts merge -> DENY.
5. Specialist attempts internal architecture access -> DENY.
6. Any environment attempts unrelated repository -> DENY.
7. ADM operational merge in authorized repository -> allowed subject to GitHub gates.
8. ADM attempts structural merge through operational capability -> DENY.
9. Expired/invalid challenge -> DENY.
10. Challenge with mismatched identity -> DENY.

## Implementation boundary

The ELO module provides policy/enforcement state. It does not implement GitHub OAuth, GitHub 2FA, GitHub passkeys, or external identity-provider authentication. Those remain external trust anchors. The ELO must consume verifiable identity assertions rather than fabricate them.
