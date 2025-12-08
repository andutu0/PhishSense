import pickle
from pathlib import Path
from typing import Any, Tuple

_model = None
_vectorizer = None


def _load_pickle(path: Path) -> Any:
    with path.open("rb") as f:
        return pickle.load(f)


def get_model_and_vectorizer(model_dir: str | None = None) -> Tuple[Any, Any]:
    global _model, _vectorizer

    if _model is not None and _vectorizer is not None:
        return _model, _vectorizer

    if model_dir is None:
        base_dir = Path(__file__).resolve().parents[2] / "model"
    else:
        base_dir = Path(model_dir)

    model_path = base_dir / "model.pkl"
    vec_path = base_dir / "vectorizer.pkl"

    if not model_path.exists() or not vec_path.exists():
        raise RuntimeError(f"Model files not found in {base_dir}")

    _model = _load_pickle(model_path)
    _vectorizer = _load_pickle(vec_path)

    return _model, _vectorizer
