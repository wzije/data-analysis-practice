# Modul Praktikum Dasar Analisis Data Penjualan dengan Python

---

## Tujuan Praktikum

Memahami teknik dasar membaca, membersihkan, mengolah, dan memvisualisasikan data transaksi penjualan agar siap mengikuti praktikum lanjutan yang lebih kompleks.

---

## Persiapan

- Pastikan Python terinstall dengan library: `pandas`, `matplotlib`
- Data sudah tersedia di file `./data/dataset.feather` (format feather)

---

## Praktikum 1: Membaca dan Memahami Struktur Data

### Tujuan

Memahami format dan isi data penjualan.

### Langkah

1. Import library dan baca data.
2. Lihat 5 baris pertama data.
3. Periksa tipe data tiap kolom.

### Kode:

```python
import pandas as pd

def praktikum1():
    df = pd.read_feather("./data/dataset.feather")
    print("5 data pertama:")
    print(df.head())
    print("\nInfo data:")
    print(df.info())
```

---

## Praktikum 2: Filter Data Kuantitas Positif dan Statistik Deskriptif

### Tujuan

Memahami cara filtering data dan analisis statistik dasar kuantitas.

### Langkah

1. Filter data agar hanya quantity > 0 (mengabaikan return atau koreksi).
2. Hitung statistik deskriptif quantity.
3. Visualisasikan distribusi quantity dengan boxplot.

### Kode:

```python
import matplotlib.pyplot as plt

def praktikum2():
    df = pd.read_feather("./data/dataset.feather")
    df_pos = df[df["Quantity"] > 0]
    print("Statistik Quantity (positif):")
    print(df_pos["Quantity"].describe())

    df_pos["Quantity"].plot.box(showfliers=False, figsize=(8,6))
    plt.title("Distribusi Quantity Positif (tanpa outlier)")
    plt.ylabel("Quantity")
    plt.show()
```

---

## Praktikum 3: Konversi Kolom Tanggal dan Resampling Data

### Tujuan

Mempelajari cara mengubah kolom tanggal ke tipe waktu dan melakukan agregasi data berdasarkan waktu.

### Langkah

1. Konversi kolom `InvoiceDate` ke tipe datetime.
2. Set kolom `InvoiceDate` sebagai index.
3. Hitung jumlah invoice unik per bulan.
4. Visualisasikan tren jumlah invoice per bulan.

### Kode:

```python
def praktikum3():
    df = pd.read_feather("./data/dataset.feather")
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    df.set_index("InvoiceDate", inplace=True)

    monthly_invoice_count = df["InvoiceNo"].resample("M").nunique()
    print("Jumlah Invoice unik per bulan:")
    print(monthly_invoice_count.head())

    monthly_invoice_count.plot(figsize=(10,6), grid=True)
    plt.title("Jumlah Invoice per Bulan")
    plt.ylabel("Jumlah Invoice")
    plt.show()
```

---

## Praktikum 4: Menghitung Total Penjualan dan Pendapatan Per Bulan

### Tujuan

Menghitung total pendapatan penjualan bulanan.

### Langkah

1. Hitung kolom baru `Sales` = `Quantity * UnitPrice`.
2. Agregasi total sales per bulan.
3. Visualisasi pendapatan bulanan.

### Kode:

```python
def praktikum4():
    df = pd.read_feather("./data/dataset.feather")
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    df["Sales"] = df["Quantity"] * df["UnitPrice"]
    df.set_index("InvoiceDate", inplace=True)

    monthly_revenue = df["Sales"].resample("M").sum()
    print("Pendapatan per bulan:")
    print(monthly_revenue.head())

    monthly_revenue.plot(figsize=(10,6), grid=True)
    plt.title("Pendapatan Penjualan per Bulan")
    plt.ylabel("Total Pendapatan")
    plt.show()
```

---

## Praktikum 5: Analisis Pelanggan dan Repeat Order Dasar

### Tujuan

Memahami struktur data customer dan invoice serta mempersiapkan data untuk analisis repeat order.

### Langkah

1. Group data per invoice (gabungkan `InvoiceNo`, `InvoiceDate`, `CustomerID`, dan total `Sales`).
2. Lihat contoh data group tersebut.

### Kode:

```python
def praktikum5():
    df = pd.read_feather("./data/dataset.feather")
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    df["Sales"] = df["Quantity"] * df["UnitPrice"]

    inv_customer = df.groupby(["InvoiceNo", "InvoiceDate", "CustomerID"])["Sales"].sum().reset_index()
    print("Data gabungan Invoice, Tanggal, Customer dan Sales:")
    print(inv_customer.head())
```

---

## Praktikum 6: Visualisasi Distribusi Pelanggan per Bulan (Persiapan Repeat Order)

### Tujuan

Melihat jumlah pelanggan unik per bulan sebagai dasar analisis repeat order.

### Langkah

1. Set index pada data gabungan invoice.
2. Hitung pelanggan unik per bulan.
3. Visualisasi grafik jumlah pelanggan unik per bulan.

### Kode:

```python
def praktikum6():
    df = pd.read_feather("./data/dataset.feather")
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    df["Sales"] = df["Quantity"] * df["UnitPrice"]

    inv_customer = df.groupby(["InvoiceNo", "InvoiceDate", "CustomerID"])["Sales"].sum().reset_index()
    inv_customer.set_index("InvoiceDate", inplace=True)

    monthly_customers = inv_customer.groupby(pd.Grouper(freq="M"))["CustomerID"].nunique()
    print("Jumlah pelanggan unik per bulan:")
    print(monthly_customers.head())

    monthly_customers.plot(figsize=(10,6), grid=True)
    plt.title("Jumlah Pelanggan Unik per Bulan")
    plt.ylabel("Jumlah Pelanggan")
    plt.show()
```

---

## Penutup Modul Dasar

Praktikum di atas akan membangun pondasi yang kuat untuk memahami data penjualan dan pola dasar dalam dataset transaksi. Setelah praktikum ini, mahasiswa sudah memahami bagaimana:

- Mengelola data transaksi dalam bentuk tabel,
- Melakukan pembersihan dan filter data,
- Memahami waktu dan resampling,
- Membuat visualisasi tren sederhana,
- Mempersiapkan data untuk analisis customer dan penjualan yang lebih kompleks.
