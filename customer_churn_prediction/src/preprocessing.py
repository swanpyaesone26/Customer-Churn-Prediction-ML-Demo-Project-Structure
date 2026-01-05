from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import joblib
from pathlib import Path
from typing import Optional


def build_encoder(save_path: Optional[str] = None):
    """Return a OneHotEncoder fitted to the training categorical scheme.

    If 'save_path' is provided the fitted encoder will be persisted via
    joblib for later reuse (recommended for production).
    """
    encoder = OneHotEncoder(
        drop="if_binary", sparse_output=False, handle_unknown="ignore"
    )
    encoder.fit(
        pd.DataFrame(
            {
                "Geography": ["France", "Germany", "Spain"],
                "Gender": ["Male", "Female", "Male"],
            }
        )[["Geography", "Gender"]]
    )

    if save_path:
        save_encoder(encoder, save_path)

    return encoder


def save_encoder(encoder: OneHotEncoder, path: str) -> None:
    """Persist a fitted encoder to 'path' using joblib."""
    dest = Path(path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(encoder, str(dest))


def load_encoder(path: str) -> Optional[OneHotEncoder]:
    """Load a persisted encoder from 'path' or return None if not found."""
    p = Path(path)
    if not p.exists():
        return None
    return joblib.load(str(p))
