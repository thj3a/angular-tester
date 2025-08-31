"""
Angular Tester - A tool to generate and run Angular unit tests using LLMs
"""

from .main import AngularTester
from .config import ConfigManager

__all__ = ['AngularTester', 'ConfigManager']