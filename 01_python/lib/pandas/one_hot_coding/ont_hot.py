import pandas as pd
import numpy as np

df = pd.DataFrame({
    "city":["北京","上海","广州"]
})

df = pd.get_dummies(
    df,
    columns=["city"]
)

print(df)