from tempfile import NamedTemporaryFile

from bot import exts
from bot.utils.extensions import unqualify, walk_extensions


def test_unqualify() -> None:
    """Test the `unqualify` function."""
    assert unqualify("bot.exts.test") == "test"
    assert unqualify("bot.exts.core.ping") == "ping"


def test_walk_extensions() -> None:
    """Test the `walk_extensions` function."""
    for ext in walk_extensions():
        assert ext.startswith(f"{exts.__name__}.")


def test_walk_extensions_skip_ignored() -> None:
    """Extensions starting with _ should be ignored."""
    with NamedTemporaryFile(dir=exts.__path__[0], prefix="_", suffix=".py", mode="w") as f:
        ext = f"{exts.__name__}.{f.name.rsplit('/')[-1].removesuffix('.py')}"
        assert ext not in walk_extensions()
