from __future__ import annotations

from typing import Iterable, Tuple

import pandas as pd


def export_readings_to_csv(rows: Iterable[Tuple[int, str, str, str]], file_path: str) -> None:
    data = list(rows)
    df = pd.DataFrame(data, columns=["id", "tag_name", "value", "timestamp"])
    df.to_csv(file_path, index=False)
