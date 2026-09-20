"""Candidate-only boundary for Hermes profiles."""
from dataclasses import dataclass
from enum import Enum
from typing import Tuple
CAPABILITY_ID="EXT-PROFILE-HERMES"
class ProfileDisposition(str,Enum): OBSERVATION="OBSERVATION"; CANDIDATE="CANDIDATE"; REJECTED="REJECTED"
@dataclass(frozen=True)
class ProfileSignal:
 profile_id:str;tenant_scope:str;source_refs:Tuple[str,...];identity_digest:str;isolated_state:bool;explicit_activation:bool;shared_canonical_memory:bool;authority_transfer:bool
@dataclass(frozen=True)
class ProfileAssessment:
 profile_id:str;disposition:ProfileDisposition;evidence_refs:Tuple[str,...];canonical_authority:bool=False;execution_permitted:bool=False;promotion_permitted:bool=False
def assess_profile(s:ProfileSignal)->ProfileAssessment:
 if not s.profile_id or not s.tenant_scope or not s.identity_digest or not s.source_refs or s.authority_transfer:return ProfileAssessment(s.profile_id,ProfileDisposition.REJECTED,s.source_refs)
 if s.shared_canonical_memory or not s.isolated_state or not s.explicit_activation:return ProfileAssessment(s.profile_id,ProfileDisposition.OBSERVATION,s.source_refs)
 return ProfileAssessment(s.profile_id,ProfileDisposition.CANDIDATE,s.source_refs)
