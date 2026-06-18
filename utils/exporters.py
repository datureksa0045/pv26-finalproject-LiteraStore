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


def export_to_pdf(file_path, data_rows):
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

        doc = SimpleDocTemplate(
            file_path,
            pagesize=landscape(A4),
            rightMargin=24,
            leftMargin=24,
            topMargin=24,
            bottomMargin=24,
        )
        styles = getSampleStyleSheet()
        elements = [
            Paragraph("Laporan Penjualan LiteraStore", styles["Title"]),
            Spacer(1, 12),
        ]

        table_data = [
            [
                "ID Transaksi",
                "Judul Buku Terjual",
                "Jumlah Qty",
                "Total Pendapatan (Rp)",
                "Tanggal Penjualan",
            ]
        ]
        table_data.extend([[str(value) for value in row] for row in data_rows])

        table = Table(table_data, repeatRows=1)
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#A67C52")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("ALIGN", (0, 1), (0, -1), "RIGHT"),
                    ("ALIGN", (2, 1), (3, -1), "RIGHT"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 9),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
                ]
            )
        )
        elements.append(table)
        doc.build(elements)
        return True, "Sukses"
    except Exception as e:
        return False, str(e)
