"""Logic helpers for matching agents to content.

Provides `compute_base_match_df` which computes absolute differences between
each agent and a given content instance for the following attributes:
`economic_status`, `ethics`, `politics`, `cultural`, `age`, and `sex`.

Differences are absolute values. For `cultural` the difference is 0 when
equal and 1 when different. The `base_score` is the mean of available
attribute differences for each agent (attributes with missing values are
ignored when computing the mean).
"""
from typing import Iterable, Mapping, Optional, Union

import numpy as np
import pandas as pd


def _as_dict(obj: Union[Mapping, object]) -> dict:
    """Return a dict from an object that may implement `to_dict()`.

    If `obj` is already a Mapping it is returned as a dict copy. If `obj`
    has a `to_dict()` method that result is returned. Otherwise an empty
    dict is returned.
    """
    if obj is None:
        return {}
    if isinstance(obj, Mapping):
        return dict(obj)
    if hasattr(obj, "to_dict") and callable(getattr(obj, "to_dict")):
        return obj.to_dict()
    return {}


def compute_base_match_df(agents_df: pd.DataFrame, content: Union[Mapping, object]) -> pd.DataFrame:
    """Compute base match score between agents and a single content instance.

    Args:
        agents_df: DataFrame of agents (columns expected: `economic_status`,
            `ethics`, `politics`, `cultural`, `age`, `sex`). Additional columns
            are preserved.
        content: Content instance or mapping with the same keys as above. Can
            be an object with `to_dict()`.

    Returns:
        A new DataFrame with appended columns for per-attribute absolute
        differences named `diff_<attribute>` and a `base_score` column which
        is the mean of available diffs for that agent.
    """
    content_dict = _as_dict(content)

    # Prefer normalized income column if available (note: follows existing
    # misspelling used in notebook: 'normallized_income'). If either the
    # agents dataframe or the content mapping contains this key, use it for


    attrs = [
        "tiered_income",
        "ethics",
        "politics",
        "cultural",
        "age",
        "sex",
    ]

    df = agents_df.copy()

    # Compute diff_tiered_income directly: the simulation guarantees
    # `tiered_income` exists on the agents DataFrame and `df_content`.
    content_tier = content_dict.get("tiered_income", None)
    try:
        content_tier = float(pd.to_numeric(content_tier, errors="coerce"))
    except Exception:
        content_tier = np.nan

    if "tiered_income" in df.columns and not pd.isna(content_tier):
        df["diff_tiered_income"] = (pd.to_numeric(df["tiered_income"], errors="coerce") - content_tier).abs()
    else:
        df["diff_tiered_income"] = np.nan

    # Helper to extract content value (or None)
    def cval(attr: str):
        return content_dict.get(attr, None)

    # Now compute other numeric diffs: ethics, politics, age, sex
    for attr in ["ethics", "politics", "age", "sex"]:
        c = cval(attr)
        try:
            c_num = pd.to_numeric(c, errors="coerce")
        except Exception:
            c_num = np.nan

        def _diff_numeric(x):
            try:
                x_num = pd.to_numeric(x, errors="coerce")
            except Exception:
                x_num = np.nan
            if pd.isna(x_num) or pd.isna(c_num):
                return np.nan
            return float(abs(x_num - c_num))

        if attr in df.columns:
            df[f"diff_{attr}"] = df[attr].apply(_diff_numeric)
        else:
            df[f"diff_{attr}"] = np.nan

    # cultural: 0 if equal (including same string), 1 if different, NaN if missing
    c_cultural = cval("cultural")

    def _normalize_cultural(val):
        if val is None or pd.isna(val):
            return None
        # If enum-like object with .value, use that
        try:
            if hasattr(val, "value"):
                base = val.value
            else:
                base = val
            return str(base).strip().lower()
        except Exception:
            return None

    norm_c = _normalize_cultural(c_cultural)

    def _diff_cultural(x):
        nx = _normalize_cultural(x)
        if nx is None or norm_c is None:
            return np.nan
        return 0.0 if nx == norm_c else 1.0

    df["diff_cultural"] = df["cultural"].apply(_diff_cultural)

    # Compute base score as mean of available diffs per row
    diff_cols = [f"diff_{a}" for a in attrs]
    df["base_score"] = 1 - df[diff_cols].mean(axis=1, skipna=True)

    return df


__all__ = ["compute_base_match_df"]
