"""Legacy module alias.

The default agent module was renamed ``agent_code_puppy`` ->
``agent_spruce_grove`` during the Spruce Grove OS rebrand. External plugins
or user customizations that import the old dotted path keep working via this
re-export module (and via the global ``code_puppy`` import shim).
"""

from spruce_grove.agents.agent_spruce_grove import SpruceGroveAgent

# Historic class name, kept for third-party imports.
CodePuppyAgent = SpruceGroveAgent

__all__ = ["SpruceGroveAgent", "CodePuppyAgent"]
