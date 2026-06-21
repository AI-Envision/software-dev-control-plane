from {{package_name}} import describe_project


def test_describe_project_is_deterministic() -> None:
    assert describe_project() == "{{project_name}}: minimal deterministic {{language}} scaffold"
