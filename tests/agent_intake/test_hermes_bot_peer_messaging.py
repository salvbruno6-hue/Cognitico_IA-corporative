from elo.agent_intake.hermes_bot_peer_messaging import build_peer_message, assess_peer_message

def test_valid_peer_message_is_candidate_only():
    m=build_peer_message("msg-1","multiteiner","bot-a","bot-b","hello","prov-1")
    r=assess_peer_message(m)
    assert r.valid is True
    assert r.delivery_permitted is False
    assert len(m.body_digest)==64

def test_self_delivery_is_rejected():
    m=build_peer_message("msg-2","multiteiner","bot-a","bot-a","hello","prov-2")
    assert assess_peer_message(m).reason=="self_delivery_not_peer_message"

def test_non_durable_message_is_rejected():
    m=build_peer_message("msg-3","multiteiner","bot-a","bot-b","hello","prov-3")
    m=type(m)(*m.__class__.__match_args__) if False else m
    from dataclasses import replace
    assert assess_peer_message(replace(m,durable=False)).reason=="durability_required"

def test_missing_provenance_is_rejected():
    try:
        build_peer_message("msg-4","multiteiner","bot-a","bot-b","hello","")
    except ValueError as exc:
        assert "provenance" in str(exc)
    else:
        raise AssertionError("missing provenance must be rejected")
