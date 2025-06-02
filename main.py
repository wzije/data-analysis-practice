import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np


# Fungsi 1: Melihat distribusi data Quantity (boxplot)
def praktikum1():
    df = pd.read_feather("./data/dataset.feather")
    print("Total data:", df.shape)
    print(df.head(5))
    print("Data sorted by Quantity desc:")
    print(df.sort_values(by="Quantity", ascending=False).head(10))

    # Boxplot hanya quantity positif, tanpa outlier (showfliers=False)
    bp = df[df["Quantity"] > 0]["Quantity"].plot.box(
        showfliers=False, legend=False, figsize=(10, 7), grid=True
    )
    bp.set_title("Distribution Quantity (Positive Values)")
    bp.set_ylabel("Quantity")
    plt.show()


# Fungsi 2: Menghitung jumlah invoice per bulan dan plot sampai 2011-12
def praktikum2():
    df = pd.read_feather("./data/dataset.feather")

    # Filter data sampai sebelum 2011-12-01
    new_df = df.loc[df["InvoiceDate"] < "2011-12-01"]
    print("Data sampai 2011-12-01:", new_df.shape)
    print(new_df.head())

    # Hitung jumlah invoice unik per bulan
    monthly_order = new_df.set_index("InvoiceDate")["InvoiceNo"].resample("M").nunique()
    print(monthly_order)

    # Plot
    ax = monthly_order.plot(legend=False, grid=True, figsize=(10, 7))
    ax.set_xlabel("Date")
    ax.set_ylabel("Number of Invoices")
    ax.set_title("Jumlah Penjualan per Bulan sampai 2011-12")
    ax.set_ylim(0, monthly_order.max() + 500)

    # Set label tanggal format MM.YYYY dengan rotasi 45 derajat
    ax.set_xticks(range(len(monthly_order.index)))
    ax.set_xticklabels([d.strftime("%m.%Y") for d in monthly_order.index], rotation=45)
    plt.show()


# Fungsi 3: Pendapatan per bulan dan plotnya
def praktikum3():
    df = pd.read_feather("./data/dataset.feather")
    df["Sales"] = df["Quantity"] * df["UnitPrice"]

    # Hitung pendapatan bulanan
    monthly_revenue = df.set_index("InvoiceDate")["Sales"].resample("M").sum()
    print("Total pendapatan:", monthly_revenue.sum())

    # Plot pendapatan per bulan
    ax = monthly_revenue.plot(legend=False, grid=True, figsize=(10, 7))
    ax.set_title("Pendapatan per Bulan")
    ax.set_ylabel("Pendapatan")
    ax.set_xlabel("Bulan")
    ax.set_ylim(0, monthly_revenue.max() + 500)

    ax.set_xticks(range(len(monthly_revenue.index)))
    ax.set_xticklabels(
        [d.strftime("%m.%Y") for d in monthly_revenue.index], rotation=45
    )
    plt.show()


# Fungsi 4: Informasi customer repeat order per bulan
def praktikum4():
    df = pd.read_feather("./data/dataset.feather")
    df["Sales"] = df["Quantity"] * df["UnitPrice"]

    # Group by InvoiceNo dan InvoiceDate: total Sales dan 1 CustomerID
    inv_customer = (
        df.groupby(["InvoiceNo", "InvoiceDate"])
        .agg({"Sales": "sum", "CustomerID": "max", "Country": "max"})
        .reset_index()
    )

    print("Data per invoice:")
    print(inv_customer.head())

    # Hitung customer yang repeat order per bulan (freq 'ME' = Month End)
    monthly_repeat_customer = (
        inv_customer.set_index("InvoiceDate")
        .groupby([pd.Grouper(freq="ME"), "CustomerID"])
        .filter(lambda x: len(x) > 1)  # customer dengan >1 transaksi per bulan
        .groupby(pd.Grouper(freq="ME"))["CustomerID"]
        .nunique()
    )

    # Total unique customer per bulan
    monthly_unique_customer = (
        df.set_index("InvoiceDate")["CustomerID"].resample("ME").nunique()
    )

    # Persentase customer repeat per bulan
    repeat_percentage = (monthly_repeat_customer / monthly_unique_customer) * 100

    # Tabel ringkasan
    summary = pd.DataFrame(
        {
            "Repeat Customers": monthly_repeat_customer,
            "Unique Customers": monthly_unique_customer,
            "Repeat %": repeat_percentage,
        }
    ).fillna(0)
    print(summary)

    # Plot (jika ingin diaktifkan, hapus tanda komentar)
    # ax = summary[["Repeat Customers", "Unique Customers"]].plot(grid=True, figsize=(10,7))
    # summary["Repeat %"].plot(ax=ax, secondary_y=True, color="green", alpha=0.3)
    # ax.set_xlabel("Bulan")
    # ax.set_ylabel("Jumlah Customer")
    # plt.title("Jumlah Customer Unik vs Repeat per Bulan")
    # plt.show()


# Fungsi 5: Pendapatan dari repeat customer dan persentasenya
def praktikum5():
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_colwidth", None)

    df = pd.read_feather("./data/dataset.feather")
    df["Sales"] = df["Quantity"] * df["UnitPrice"]

    inv_customer = (
        df.groupby(["InvoiceNo", "InvoiceDate"])
        .agg({"CustomerID": "max", "Country": "max", "Sales": "sum"})
        .reset_index()
    )

    # Filter repeat customer: customer dengan >1 transaksi per bulan
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

    # Persentase pendapatan dari repeat customer tiap bulan
    repeat_rev_percentage = (
        monthly_repeat_revenue.groupby(level=0).sum() / monthly_revenue
    ) * 100

    print("Minimum persentase pendapatan repeat customer:", repeat_rev_percentage.min())

    # Plot pendapatan total dan repeat customer
    ax = monthly_revenue.plot(figsize=(12, 9), label="Total Revenue")
    monthly_repeat_revenue.groupby(level=0).sum().plot(
        ax=ax, grid=True, label="Repeat Customer Revenue"
    )

    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Pendapatan")
    ax.set_title("Pendapatan Total vs Pendapatan Repeat Customer")
    ax.legend()
    ax.set_ylim(0, monthly_revenue.max() + 100000)

    # Plot persentase pendapatan repeat customer (bar plot dengan y axis kanan)
    ax2 = ax.twinx()
    repeat_rev_percentage.plot(
        kind="bar", color="green", alpha=0.3, ax=ax2, label="Repeat Revenue %"
    )
    ax2.set_ylabel("Persentase (%)")
    ax2.set_ylim(0, repeat_rev_percentage.max() + 10)
    ax2.legend(loc="upper right")
    plt.show()


# Fungsi 6: Prediksi pendapatan penjualan 6 bulan ke depan dengan regresi linier
def praktikum6():
    df = pd.read_feather("./data/dataset.feather")
    df["Sales"] = df["Quantity"] * df["UnitPrice"]

    # Pendapatan bulanan
    monthly_revenue = df.set_index("InvoiceDate")["Sales"].resample("M").sum()

    # Index numerik (bulan ke-n)
    X = np.arange(len(monthly_revenue)).reshape(-1, 1)
    y = monthly_revenue.values

    # Training model regresi linier
    model = LinearRegression()
    model.fit(X, y)

    # Prediksi 6 bulan ke depan
    future_months = 6
    X_future = np.arange(
        len(monthly_revenue), len(monthly_revenue) + future_months
    ).reshape(-1, 1)
    y_pred = model.predict(X_future)

    # Gabungkan data asli dan prediksi
    all_months = np.arange(len(monthly_revenue) + future_months)
    all_sales = np.concatenate([y, y_pred])

    # Plot hasil aktual dan prediksi
    plt.figure(figsize=(10, 7))
    plt.plot(all_months[: len(X)], y, label="Pendapatan Aktual")
    plt.plot(all_months[len(X) :], y_pred, "--", label="Prediksi", color="red")
    plt.title("Prediksi Pendapatan Penjualan 6 Bulan ke Depan")
    plt.xlabel("Bulan ke-n")
    plt.ylabel("Pendapatan")
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    while True:
        print("\nPilih praktikum yang ingin dijalankan:")
        print("1. Distribusi data Quantity")
        print("2. Jumlah invoice / penjualan per bulan")
        print("3. Informasi pendapatan per bulan")
        print("4. Informasi customer yang repeat order")
        print("5. Informasi revenue dari repeat customer")
        print("6. Prediksi penjualan 6 bulan ke depan")
        print("0. Keluar")

        pilihan = input("Masukkan nomor pilihan: ")

        if pilihan == "1":
            praktikum1()
        elif pilihan == "2":
            praktikum2()
        elif pilihan == "3":
            praktikum3()
        elif pilihan == "4":
            praktikum4()
        elif pilihan == "5":
            praktikum5()
        elif pilihan == "6":
            praktikum6()
        elif pilihan == "0":
            print("Terima kasih, program selesai.")
            break
        else:
            print("Pilihan tidak valid, silakan coba lagi.")


if __name__ == "__main__":
    main()
