"""
Modul Praktikum Analisis Data Penjualan dengan Python

Berisi:
- Praktikum Dasar (membaca data, filter, agregasi, visualisasi dasar)
- Praktikum Lanjutan (repeat order, revenue repeat, prediksi)

Gunakan modul ini untuk latihan bertahap dari dasar ke lanjutan.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression


# -----------------------
# PRAKTIKUM DASAR
# -----------------------


def praktikum_dasar_1():
    """
    Praktikum 1:
    Membaca data feather, melihat 5 data pertama dan info tipe data
    """
    df = pd.read_feather("./assets/data.feather")
    print("5 data pertama:")
    print(df.head())
    print("\nInfo data:")
    print(df.info())


def praktikum_dasar_2():
    """
    Praktikum 2:
    Filter quantity > 0, deskriptif statistik quantity, boxplot distribusi quantity positif
    """
    df = pd.read_feather("./assets/data.feather")
    df_pos = df[df["Quantity"] > 0]

    print("Statistik Quantity (positif):")
    print(df_pos["Quantity"].describe())

    df_pos["Quantity"].plot.box(showfliers=False, figsize=(8, 6))
    plt.title("Distribusi Quantity Positif (tanpa outlier)")
    plt.ylabel("Quantity")
    plt.show()


def praktikum_dasar_3():
    """
    Praktikum 3:
    Konversi kolom InvoiceDate ke datetime, set sebagai index,
    hitung jumlah invoice unik per bulan, dan plot tren jumlah invoice.
    """
    df = pd.read_feather("./assets/data.feather")
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    df.set_index("InvoiceDate", inplace=True)

    monthly_invoice_count = df["InvoiceNo"].resample("M").nunique()
    print("Jumlah Invoice unik per bulan:")
    print(monthly_invoice_count.head())

    monthly_invoice_count.plot(figsize=(10, 6), grid=True)
    plt.title("Jumlah Invoice per Bulan")
    plt.ylabel("Jumlah Invoice")
    plt.show()


def praktikum_dasar_4():
    """
    Praktikum 4:
    Membuat kolom Sales, hitung total pendapatan penjualan per bulan, plot grafik pendapatan bulanan.
    """
    df = pd.read_feather("./assets/data.feather")
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    df["Sales"] = df["Quantity"] * df["UnitPrice"]
    df.set_index("InvoiceDate", inplace=True)

    monthly_revenue = df["Sales"].resample("M").sum()
    print("Pendapatan per bulan:")
    print(monthly_revenue.head())

    monthly_revenue.plot(figsize=(10, 6), grid=True)
    plt.title("Pendapatan Penjualan per Bulan")
    plt.ylabel("Total Pendapatan")
    plt.show()


def praktikum_dasar_5():
    """
    Praktikum 5:
    Gabungkan data per invoice dengan total Sales dan CustomerID,
    tampilkan contoh data gabungan untuk analisis customer.
    """
    df = pd.read_feather("./assets/data.feather")
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    df["Sales"] = df["Quantity"] * df["UnitPrice"]

    inv_customer = (
        df.groupby(["InvoiceNo", "InvoiceDate", "CustomerID"])["Sales"]
        .sum()
        .reset_index()
    )
    print("Data gabungan Invoice, Tanggal, Customer dan Sales:")
    print(inv_customer.head())


def praktikum_dasar_6():
    """
    Praktikum 6:
    Hitung jumlah pelanggan unik per bulan dan visualisasikan grafik pelanggan per bulan,
    sebagai persiapan analisis repeat order.
    """
    df = pd.read_feather("./assets/data.feather")
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    df["Sales"] = df["Quantity"] * df["UnitPrice"]

    inv_customer = (
        df.groupby(["InvoiceNo", "InvoiceDate", "CustomerID"])["Sales"]
        .sum()
        .reset_index()
    )
    inv_customer.set_index("InvoiceDate", inplace=True)

    monthly_customers = inv_customer.groupby(pd.Grouper(freq="M"))[
        "CustomerID"
    ].nunique()
    print("Jumlah pelanggan unik per bulan:")
    print(monthly_customers.head())

    monthly_customers.plot(figsize=(10, 6), grid=True)
    plt.title("Jumlah Pelanggan Unik per Bulan")
    plt.ylabel("Jumlah Pelanggan")
    plt.show()


# -----------------------
# PRAKTIKUM LANJUTAN
# -----------------------


def praktikum_lanjutan_1():
    """
    Praktikum 1 Lanjutan:
    Distribusi Quantity (positif) dengan boxplot tanpa outlier.
    """
    df = pd.read_feather("./assets/data.feather")
    bp = df[df["Quantity"] > 0]["Quantity"].plot.box(showfliers=False, figsize=(10, 7))
    bp.set_title("Distribution Quantity (Positive Values)")
    bp.set_ylabel("Quantity")
    plt.show()


def praktikum_lanjutan_2():
    """
    Praktikum 2 Lanjutan:
    Jumlah Invoice per Bulan sampai 2011-12.
    """
    df = pd.read_feather("./assets/data.feather")
    new_df = df.loc[df["InvoiceDate"] < "2011-12-01"]
    monthly_order = new_df.set_index("InvoiceDate")["InvoiceNo"].resample("M").nunique()
    monthly_order.plot(figsize=(10, 7), grid=True)
    plt.title("Jumlah Penjualan per Bulan sampai 2011-12")
    plt.show()


def praktikum_lanjutan_3():
    """
    Praktikum 3 Lanjutan:
    Pendapatan per Bulan.
    """
    df = pd.read_feather("./assets/data.feather")
    df["Sales"] = df["Quantity"] * df["UnitPrice"]
    monthly_revenue = df.set_index("InvoiceDate")["Sales"].resample("M").sum()
    monthly_revenue.plot(figsize=(10, 7), grid=True)
    plt.title("Pendapatan per Bulan")
    plt.show()


def praktikum_lanjutan_4():
    """
    Praktikum 4 Lanjutan:
    Analisis Customer Repeat Order: jumlah customer yang order lebih dari sekali per bulan.
    Termasuk visualisasi grafik.
    """
    df = pd.read_feather("./assets/data.feather")
    df["Sales"] = df["Quantity"] * df["UnitPrice"]
    inv_customer = (
        df.groupby(["InvoiceNo", "InvoiceDate"])
        .agg({"Sales": "sum", "CustomerID": "max"})
        .reset_index()
    )

    monthly_repeat_customer = (
        inv_customer.set_index("InvoiceDate")
        .groupby([pd.Grouper(freq="ME"), "CustomerID"])
        .filter(lambda x: len(x) > 1)
        .groupby(pd.Grouper(freq="ME"))["CustomerID"]
        .nunique()
    )

    print("Jumlah Customer Repeat Order per Bulan:")
    print(monthly_repeat_customer)

    monthly_repeat_customer.plot(figsize=(10, 6), grid=True)
    plt.title("Jumlah Customer Repeat Order per Bulan")
    plt.ylabel("Jumlah Customer")
    plt.show()


def praktikum_lanjutan_5():
    """
    Praktikum 5 Lanjutan:
    Revenue dari Repeat Customer per bulan.
    Termasuk visualisasi grafik.
    """
    df = pd.read_feather("./assets/data.feather")
    df["Sales"] = df["Quantity"] * df["UnitPrice"]
    inv_customer = (
        df.groupby(["InvoiceNo", "InvoiceDate"])
        .agg({"CustomerID": "max", "Sales": "sum"})
        .reset_index()
    )

    repeat_filter = (
        inv_customer.set_index("InvoiceDate")
        .groupby([pd.Grouper(freq="ME"), "CustomerID"])
        .filter(lambda x: len(x) > 1)
    )

    monthly_repeat_revenue = repeat_filter.groupby(
        [pd.Grouper(freq="ME"), "CustomerID"]
    )["Sales"].sum()
    monthly_revenue = (
        inv_customer.set_index("InvoiceDate").resample("ME")["Sales"].sum()
    )

    print("Revenue Repeat Customer per Bulan:")
    print(monthly_repeat_revenue)

    # Plot total repeat revenue per month (aggregate per month)
    monthly_repeat_revenue.groupby(level=0).sum().plot(figsize=(10, 6), grid=True)
    plt.title("Revenue dari Repeat Customer per Bulan")
    plt.ylabel("Total Revenue")
    plt.show()


def praktikum_lanjutan_6():
    """
    Praktikum 6 Lanjutan:
    Prediksi Pendapatan 6 Bulan ke Depan menggunakan Linear Regression.
    """
    df = pd.read_feather("./assets/data.feather")
    df["Sales"] = df["Quantity"] * df["UnitPrice"]
    monthly_revenue = df.set_index("InvoiceDate")["Sales"].resample("M").sum()

    X = np.arange(len(monthly_revenue)).reshape(-1, 1)
    y = monthly_revenue.values

    model = LinearRegression()
    model.fit(X, y)

    future_months = 6
    X_future = np.arange(
        len(monthly_revenue), len(monthly_revenue) + future_months
    ).reshape(-1, 1)
    y_pred = model.predict(X_future)

    plt.plot(np.arange(len(monthly_revenue)), y, label="Pendapatan Aktual")
    plt.plot(
        np.arange(len(monthly_revenue), len(monthly_revenue) + future_months),
        y_pred,
        "--",
        label="Prediksi",
    )
    plt.title("Prediksi Pendapatan Penjualan 6 Bulan ke Depan")
    plt.legend()
    plt.show()
