from lamd.compute import Compute


def test_compute_initialization():
    """Test that Compute class can be initialized."""
    compute = Compute()
    assert compute is not None


def test_compute_functions_list():
    """Test that _compute_functions_list returns an empty list."""
    compute = Compute()
    functions = compute._compute_functions_list()
    assert isinstance(functions, list)
    assert len(functions) == 0
