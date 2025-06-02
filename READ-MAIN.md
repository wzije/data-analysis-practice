# Materi Praktikum Analisis Data dengan Python dan Pandas

---

## Praktikum 1: Distribusi Quantity dengan Boxplot

```python
def praktikum1():
    # Membaca data dari file feather yang sudah disiapkan
    df = pd.read_feather("./assets/data.feather")

    # Memilih data Quantity yang nilainya lebih dari 0 (mengabaikan quantity negatif atau 0)
    # lalu membuat boxplot tanpa menampilkan outlier (showfliers=False)
    bp = df[df["Quantity"] > 0]["Quantity"].plot.box(showfliers=False, figsize=(10,7))

    # Memberi judul grafik
    bp.set_title("Distribution Quantity (Positive Values)")
    bp.set_ylabel("Quantity")

    # Menampilkan plot
    plt.show()
```

**Penjelasan:**
Kode ini menampilkan distribusi kuantitas barang yang terjual menggunakan boxplot, membantu melihat rentang, median, dan penyebaran data quantity positif.

---

## Praktikum 2: Jumlah Invoice Per Bulan

```python
def praktikum2():
    # Membaca data
    df = pd.read_feather("./assets/data.feather")

    # Filter data hanya sampai tanggal 1 Desember 2011 (exclude data sesudah itu)
    new_df = df.loc[df["InvoiceDate"] < "2011-12-01"]

    # Mengelompokkan data berdasarkan tanggal invoice dan menghitung jumlah invoice unik per bulan
    monthly_order = new_df.set_index("InvoiceDate")["InvoiceNo"].resample("M").nunique()

    # Membuat plot garis jumlah invoice per bulan
    monthly_order.plot(figsize=(10,7), grid=True)
    plt.title("Jumlah Penjualan per Bulan sampai 2011-12")
    plt.show()
```

**Penjelasan:**
Menampilkan tren jumlah transaksi (invoice) unik tiap bulan hingga November 2011, membantu melihat pola aktivitas penjualan bulanan.

---

## Praktikum 3: Pendapatan Per Bulan

```python
def praktikum3():
    df = pd.read_feather("./assets/data.feather")

    # Membuat kolom baru "Sales" sebagai hasil perkalian Quantity dan UnitPrice
    df["Sales"] = df["Quantity"] * df["UnitPrice"]

    # Menghitung total pendapatan per bulan dengan resampling data berdasarkan tanggal invoice
    monthly_revenue = df.set_index("InvoiceDate")["Sales"].resample("M").sum()

    # Membuat plot garis total pendapatan per bulan
    monthly_revenue.plot(figsize=(10,7), grid=True)
    plt.title("Pendapatan per Bulan")
    plt.show()
```

**Penjelasan:**
Menghitung dan menampilkan total pendapatan bulanan sebagai indikator performa bisnis dari waktu ke waktu.

---

## Praktikum 4: Analisis Customer Repeat Order

```python
def praktikum4():
    df = pd.read_feather("./assets/data.feather")
    df["Sales"] = df["Quantity"] * df["UnitPrice"]

    # Data invoice per customer per tanggal
    inv_customer = df.groupby(["InvoiceNo", "InvoiceDate"]).agg({"Sales":"sum","CustomerID":"max"}).reset_index()

    # Total customer unik per bulan
    monthly_total_customer = (
        inv_customer.set_index("InvoiceDate")
        .groupby(pd.Grouper(freq="ME"))["CustomerID"]
        .nunique()
    )

    # Customer repeat (lebih dari 1 invoice per bulan)
    monthly_repeat_customer = (
        inv_customer.set_index("InvoiceDate")
        .groupby([pd.Grouper(freq="ME"), "CustomerID"])
        .filter(lambda x: len(x) > 1)
        .groupby(pd.Grouper(freq="ME"))["CustomerID"]
        .nunique()
    )

    # Hitung persentase repeat customer per bulan
    repeat_customer_pct = (monthly_repeat_customer / monthly_total_customer) * 100

    print("Jumlah Repeat Customer per bulan:")
    print(monthly_repeat_customer)
    print("\nPersentase Repeat Customer per bulan:")
    print(repeat_customer_pct)

    # Plot jumlah repeat customer
    plt.figure(figsize=(14,6))
    monthly_total_customer.plot(kind="bar", color="lightgray", label="Total Customer")
    monthly_repeat_customer.plot(kind="bar", color="skyblue", label="Repeat Customer")
    plt.title("Jumlah Total dan Repeat Customer per Bulan")
    plt.xlabel("Bulan")
    plt.ylabel("Jumlah Customer")
    plt.legend()
    plt.grid(axis="y")
    plt.show()

    # Plot persentase repeat customer
    plt.figure(figsize=(14,4))
    repeat_customer_pct.plot(kind="line", marker="o", color="blue")
    plt.title("Persentase Repeat Customer per Bulan (%)")
    plt.xlabel("Bulan")
    plt.ylabel("Persentase (%)")
    plt.grid(True)
    plt.show()

```

**Penjelasan:**
Mengidentifikasi dan menghitung jumlah pelanggan yang melakukan repeat order dalam satu bulan, berguna untuk analisis loyalitas pelanggan.

---

## Praktikum 5: Revenue dari Repeat Customer

```python
def praktikum4():
    df = pd.read_feather("./assets/data.feather")
    df["Sales"] = df["Quantity"] * df["UnitPrice"]

    # Data invoice per customer per tanggal
    inv_customer = df.groupby(["InvoiceNo", "InvoiceDate"]).agg({"Sales":"sum","CustomerID":"max"}).reset_index()

    # Total customer unik per bulan
    monthly_total_customer = (
        inv_customer.set_index("InvoiceDate")
        .groupby(pd.Grouper(freq="ME"))["CustomerID"]
        .nunique()
    )

    # Customer repeat (lebih dari 1 invoice per bulan)
    monthly_repeat_customer = (
        inv_customer.set_index("InvoiceDate")
        .groupby([pd.Grouper(freq="ME"), "CustomerID"])
        .filter(lambda x: len(x) > 1)
        .groupby(pd.Grouper(freq="ME"))["CustomerID"]
        .nunique()
    )

    # Hitung persentase repeat customer per bulan
    repeat_customer_pct = (monthly_repeat_customer / monthly_total_customer) * 100

    print("Jumlah Repeat Customer per bulan:")
    print(monthly_repeat_customer)
    print("\nPersentase Repeat Customer per bulan:")
    print(repeat_customer_pct)

    # Plot jumlah repeat customer
    plt.figure(figsize=(14,6))
    monthly_total_customer.plot(kind="bar", color="lightgray", label="Total Customer")
    monthly_repeat_customer.plot(kind="bar", color="skyblue", label="Repeat Customer")
    plt.title("Jumlah Total dan Repeat Customer per Bulan")
    plt.xlabel("Bulan")
    plt.ylabel("Jumlah Customer")
    plt.legend()
    plt.grid(axis="y")
    plt.show()

    # Plot persentase repeat customer
    plt.figure(figsize=(14,4))
    repeat_customer_pct.plot(kind="line", marker="o", color="blue")
    plt.title("Persentase Repeat Customer per Bulan (%)")
    plt.xlabel("Bulan")
    plt.ylabel("Persentase (%)")
    plt.grid(True)
    plt.show()

```

**Penjelasan:**
Menghitung pendapatan yang berasal dari pelanggan yang melakukan repeat order per bulan, berguna untuk analisis kontribusi pelanggan setia terhadap revenue.

---

## Praktikum 6: Prediksi Pendapatan 6 Bulan ke Depan dengan Linear Regression

```python
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt

def praktikum6():
    df = pd.read_feather("./assets/data.feather")
    df["Sales"] = df["Quantity"] * df["UnitPrice"]

    # Hitung pendapatan bulanan
    monthly_revenue = df.set_index("InvoiceDate")["Sales"].resample("M").sum()

    # Membuat variabel X sebagai indeks waktu bulan (0,1,2,...)
    X = np.arange(len(monthly_revenue)).reshape(-1, 1)
    y = monthly_revenue.values

    # Membuat model regresi linear dan melatih model
    model = LinearRegression()
    model.fit(X, y)

    # Prediksi 6 bulan ke depan
    future_months = 6
    X_future = np.arange(len(monthly_revenue), len(monthly_revenue) + future_months).reshape(-1, 1)
    y_pred = model.predict(X_future)

    # Plot hasil pendapatan aktual dan prediksi
    plt.plot(np.arange(len(monthly_revenue)), y, label="Pendapatan Aktual")
    plt.plot(np.arange(len(monthly_revenue), len(monthly_revenue) + future_months), y_pred, "--", label="Prediksi")
    plt.title("Prediksi Pendapatan Penjualan 6 Bulan ke Depan")
    plt.legend()
    plt.show()
```

**Penjelasan:**
Menggunakan regresi linear sederhana untuk memprediksi pendapatan penjualan 6 bulan ke depan berdasarkan tren pendapatan bulanan historis.

# Kesimpulan

- Praktikum dasar memulai dengan membaca dan memahami data.
- Praktikum lanjutan memperdalam analisis statistik, grouping, pivot, dan visualisasi.
- Analisis repeat order dan revenue membantu memahami loyalitas pelanggan.
- Prediksi menggunakan regresi linier sederhana untuk estimasi pendapatan masa depan.
