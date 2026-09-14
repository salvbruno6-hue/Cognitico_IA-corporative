"""Regression tests for native media governance."""
import pytest
from src.elo.cognitive.media_boundary import GovernedMediaBoundary, MediaBoundaryError, MediaObservation


def valid():
    return MediaObservation("m-1", "tenant-1", "image", "source:camera", ("ev-1",), {"source": "camera"}, "resize")


def test_media_observation_is_accepted():
    assert GovernedMediaBoundary().accept(valid()).media_id == "m-1"


def test_media_requires_evidence():
    with pytest.raises(MediaBoundaryError):
        GovernedMediaBoundary().accept(MediaObservation("m-1", "tenant-1", "image", "source", (), {"source": "x"}))


def test_media_rejects_secrets():
    item = valid()
    object.__setattr__(item, "provenance", {"api_key": "x"})
    with pytest.raises(MediaBoundaryError):
        GovernedMediaBoundary().accept(item)
