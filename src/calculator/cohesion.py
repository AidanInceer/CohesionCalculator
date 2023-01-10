from dataclasses import dataclass

import pandas as pd


@dataclass
class Calculate:
    directory_df: pd.Dataframe

    def thing(self):
        pass
