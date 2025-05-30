"""Pytest configuration and fixtures for Virtual Power Plant (VPP) tests."""

import os
import sys

import pytest

# Set up import path before importing project modules
root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, root)

import src.vpp.main as vpp  # noqa: E402


@pytest.fixture(autouse=True)
def reset_vpp_state():
    """Reset the global state of the VPP before each test."""
    vpp.plants.clear()
    vpp.next_id = 1
    yield
