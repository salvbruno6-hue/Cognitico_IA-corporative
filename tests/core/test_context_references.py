from src.elo.core.context_references import parse_context_references


def test_parses_file_with_line_range_without_io():
    refs = parse_context_references("inspect @file:src/elo/core/context_resolution.py:10-25")
    assert len(refs) == 1
    ref = refs[0]
    assert ref.kind == "file"
    assert ref.target == "src/elo/core/context_resolution.py"
    assert ref.line_start == 10
    assert ref.line_end == 25
    assert ref.owner == "artifact_resolver"
    assert ref.required_capability is None


def test_parses_folder_and_git_references():
    refs = parse_context_references("@folder:src/elo @git:3")
    assert [(ref.kind, ref.target) for ref in refs] == [("folder", "src/elo"), ("git", "3")]
    assert refs[0].owner == "artifact_resolver"
    assert refs[1].owner == "source_discovery"
    assert refs[1].required_capability == "source.github.read"


def test_parses_diff_staged_and_url_references():
    refs = parse_context_references("@diff @staged @url:https://example.com/docs")
    assert [ref.kind for ref in refs] == ["diff", "staged", "url"]
    assert refs[0].required_capability == "source.github.read"
    assert refs[1].required_capability == "source.github.read"
    assert refs[2].required_capability == "source.web.read"


def test_quoted_targets_preserve_spaces():
    refs = parse_context_references('@file:"docs/project plan.md" @url:`https://example.com/a path`')
    assert refs[0].target == "docs/project plan.md"
    assert refs[1].target == "https://example.com/a path"


def test_trailing_sentence_punctuation_is_not_part_of_target():
    refs = parse_context_references("See @file:README.md, then @url:https://example.com/page.")
    assert refs[0].target == "README.md"
    assert refs[1].target == "https://example.com/page"


def test_no_reference_means_no_work():
    assert parse_context_references("normal message with no attachment") == ()


def test_parser_is_non_operational_and_preserves_order():
    refs = parse_context_references("@file:a.py @diff @file:b.py:4")
    assert [ref.raw for ref in refs] == ["@file:a.py", "@diff", "@file:b.py:4"]
    assert all(ref.target for ref in refs)
