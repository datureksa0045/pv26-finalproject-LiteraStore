import csv

def export_to_csv(file_path, data_rows):
    try:
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Header Laporan Penjualan
            writer.writerow(["ID Transaksi", "Judul Buku Terjual", "Jumlah Qty", "Total Pendapatan (Rp)", "Tanggal Penjualan"])
            writer.writerows(data_rows)
        return True, "Sukses"
    except Exception as e:
        return False, str(e)