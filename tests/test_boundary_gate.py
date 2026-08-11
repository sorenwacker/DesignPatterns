"""Tests for the Boundary Gate pattern."""

import pytest

from design_patterns.gates.boundary import BoundaryGate

CLEAN_MODULE = '''
"""Generic import machinery. The profile is supplied by the caller."""

from collections.abc import Mapping


def build(records: Mapping[str, str], profile) -> list[str]:
    return profile.order(records)
'''

DIRECT_IMPORT = """
from profiles.miappe import Profile


def default_profile():
    return Profile()
"""

SUBMODULE_IMPORT = """
import profiles.miappe.fields
"""

VOCABULARY_LEAK = '''
"""Ordering rules for the MIAPPE programme."""

DEFAULT_ORDER = ("investigation", "study")
'''

COMPOSITION_MODULE = """
from profiles.miappe import Profile


def build_application():
    return Importer(profile=Profile())
"""


@pytest.fixture
def gate():
    """A gate keeping the generic library free of any specific profile."""
    return BoundaryGate(
        forbidden_prefix="profiles",
        forbidden_vocabulary=frozenset({"miappe"}),
        composition=frozenset({"cli/__init__.py"}),
    )


class TestImportViolations:
    """Tests for the import half of the gate."""

    def test_a_clean_module_passes(self, gate):
        """A module that receives its collaborator passes."""
        assert gate.import_violations({"library/importer.py": CLEAN_MODULE}) == []

    def test_a_direct_import_is_a_violation(self, gate):
        """Reaching for the implementation is the hidden dependency."""
        (message,) = gate.import_violations({"library/defaults.py": DIRECT_IMPORT})
        assert "library/defaults.py" in message

    def test_a_submodule_import_is_a_violation(self, gate):
        """Matching the prefix catches imports below the forbidden package."""
        (message,) = gate.import_violations({"library/fields.py": SUBMODULE_IMPORT})
        assert "profiles.miappe.fields" in message

    def test_a_package_with_a_similar_name_is_not_a_violation(self, gate):
        """Prefix matching must respect module boundaries."""
        source = "import profileshelper\n"
        assert gate.import_violations({"library/helper.py": source}) == []

    def test_the_composition_point_is_exempt(self, gate):
        """Naming the implementation is the composition point's whole job."""
        assert gate.import_violations({"cli/__init__.py": COMPOSITION_MODULE}) == []

    def test_the_message_states_the_rule(self, gate):
        """The failure explains the principle, not only the fact."""
        (message,) = gate.import_violations({"library/defaults.py": DIRECT_IMPORT})
        assert "never reached for" in message


class TestVocabularyViolations:
    """Tests for the vocabulary half of the gate."""

    def test_a_docstring_naming_the_forbidden_thing_is_a_violation(self, gate):
        """A layer free of the import can still be coupled by its vocabulary."""
        (message,) = gate.vocabulary_violations({"library/order.py": VOCABULARY_LEAK})
        assert "library/order.py" in message

    def test_the_match_is_case_insensitive(self, gate):
        """MIAPPE, Miappe, and miappe are the same leak."""
        assert gate.vocabulary_violations({"library/a.py": "# miappe\n"}) != []
        assert gate.vocabulary_violations({"library/b.py": "# MIAPPE\n"}) != []

    def test_a_clean_module_has_no_vocabulary_violation(self, gate):
        """Generic wording produces no message."""
        assert gate.vocabulary_violations({"library/importer.py": CLEAN_MODULE}) == []

    def test_the_composition_point_may_use_the_vocabulary(self, gate):
        """The exemption covers naming as well as importing."""
        assert gate.vocabulary_violations({"cli/__init__.py": COMPOSITION_MODULE}) == []


class TestExemptions:
    """Tests separating principled exemptions from tolerated debt."""

    def test_a_grandfathered_module_is_exempt(self):
        """Debt is tolerated so the rule can be adopted before the cleanup."""
        gate = BoundaryGate(
            forbidden_prefix="profiles",
            forbidden_vocabulary=frozenset({"miappe"}),
            composition=frozenset({"cli/__init__.py"}),
            grandfathered=frozenset({"library/legacy.py"}),
        )
        assert gate.violations({"library/legacy.py": DIRECT_IMPORT}) == []

    def test_debt_and_principle_are_separate_lists(self, gate):
        """A module exempt on principle is not recorded as debt."""
        assert gate.grandfathered == frozenset()
        assert gate.composition == frozenset({"cli/__init__.py"})


class TestCombinedViolations:
    """Both halves of the gate together."""

    def test_import_and_vocabulary_violations_are_both_reported(self, gate):
        """A module can fail both checks and should report both."""
        source = DIRECT_IMPORT + VOCABULARY_LEAK
        assert len(gate.violations({"library/defaults.py": source})) == 2

    def test_check_raises_on_any_violation(self, gate):
        """check is the assertion form of violations."""
        with pytest.raises(AssertionError, match="library/defaults.py"):
            gate.check({"library/defaults.py": DIRECT_IMPORT})

    def test_check_passes_on_a_clean_package(self, gate):
        """A package that honours the boundary passes quietly."""
        gate.check({"library/importer.py": CLEAN_MODULE})
