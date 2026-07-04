#!/usr/bin/env python3
"""
Shared configuration module for HuggingFace scripts
Reads service and satellite names from config.yaml
"""

import yaml
from pathlib import Path


def _load_config():
    """Load config.yaml from the scripts directory"""
    config_path = Path(__file__).parent / "config.yaml"
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def get_services_names():
    """Read service list from config.yaml"""
    config = _load_config()
    return config.get('services', {}).get('names', [])


def get_satellites_names():
    """Read satellite list from config.yaml"""
    config = _load_config()
    return config.get('services', {}).get('satellites', [])
