import pandas as pd
import matplotlib.pylab as plt

df = pd.read_feather("./data/dataset.feather")
# filter product bulanan

filtered_product_df = pd.DataFrame(
    df.set_index("InvoiceDate")
    .groupby([pd.Grouper(freq="ME"), "StockCode"])["Quantity"]
    .sum()
)

last_filtered_product_df = (
    filtered_product_df.loc["2011-11-30"]
    .sort_values(by="Quantity", ascending=False)
    .reset_index()
)

print(df.head())
