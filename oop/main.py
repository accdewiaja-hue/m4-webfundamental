import sys
from scanner import TCPPortScanner
from report import PDFReportExporter, JSONReportExporter


def main():
    print("=== APLIKASI PORT SCANNER & EXPORTER (OOP) ===")
    target = input("Masukkan IP atau Domain target (contoh: 127.0.0.1): ").strip()

    try:
        start = int(input("Masukkan port awal (contoh: 1): "))
        end = int(input("Masukkan port akhir (contoh: 1024): "))
    except ValueError:
        print("[!] Masukkan angka port yang valid.")
        sys.exit(1)

    # Membuat objek scanner (menggunakan abstraksi BaseScanner melalui kelas konkret)
    scanner = TCPPortScanner(target_host=target, start_port=start, end_port=end, timeout=0.4)

    # Melakukan pemindaian (polimorfisme: pemanggilan metode scan() secara seragam)
    open_ports = scanner.scan()

    # Menyiapkan data hasil pemindaian (enkapsulasi via antarmuka publik)
    scan_data = {
        "target_host": scanner.get_target_host(),
        "target_ip": scanner.get_target_ip(),
        "start_port": scanner.get_start_port(),
        "end_port": scanner.get_end_port(),
        "open_ports": open_ports,
    }

    # Membentuk nama berkas yang aman
    safe_target = str(scanner.get_target_host()).replace('.', '_').replace(':', '_')

    # Membuat exporter (polimorfisme: menggunakan antarmuka BaseReportExporter)
    pdf_exporter = PDFReportExporter(filename=f"scan_report_{safe_target}.pdf")
    json_exporter = JSONReportExporter(filename=f"scan_report_{safe_target}.json")

    # Mengekspor hasil secara seragam melalui metode export()
    pdf_exporter.export(scan_data)
    json_exporter.export(scan_data)


if __name__ == "__main__":
    main()
