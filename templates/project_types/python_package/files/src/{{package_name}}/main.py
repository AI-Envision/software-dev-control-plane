from __future__ import annotations


def describe_project() -> str:
    """Return a deterministic scaffold description.

    Time complexity: O(1)
    Space complexity: O(1)
    """
    return "{{project_name}}: minimal deterministic {{language}} scaffold"
