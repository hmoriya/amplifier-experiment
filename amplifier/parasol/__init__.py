"""
Parasol DDD Framework for Amplifier

A domain-driven development framework that expands from central information design
like an umbrella opening from a single point.
"""

from .core import ParasolEngine
from .knowledge import KnowledgeBase
from .knowledge import KnowledgeCollector
from .memory import ParasolMemory
from .patterns import PatternLibrary
from .patterns import PatternMatcher
from .phases import CapabilityDesignPhase
from .phases import DomainModelingPhase
from .phases import ImplementationGenerationPhase
from .phases import OperationDesignPhase
from .phases import ValidationOptimizationPhase
from .phases import ValueAnalysisPhase

__all__ = [
    "ParasolEngine",
    "ValueAnalysisPhase",
    "CapabilityDesignPhase",
    "DomainModelingPhase",
    "OperationDesignPhase",
    "ImplementationGenerationPhase",
    "ValidationOptimizationPhase",
    "PatternLibrary",
    "PatternMatcher",
    "KnowledgeBase",
    "KnowledgeCollector",
    "ParasolMemory",
]

__version__ = "1.0.0"
