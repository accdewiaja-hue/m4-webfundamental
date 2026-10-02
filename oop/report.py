import json
from abc import ABC, abstractmethod
from datetime import datetime


class BaseReportExporter(ABC):
    """Abstraksi antarmuka untuk ekspor hasil pemindaian."""

    def __init__(self, filename):
        self._filename = filename

    @abstractmethod
    def export(self, scan_data):
        """Metode export yang harus diimplementasikan kelas turunan."""
        pass

    def get_filename(self):
        """Antarmuka publik untuk mengakses nama berkas."""
        return self._filename


class PDFReportExporter(BaseReportExporter):
    """Ekspor hasil pemindaian ke PDF (mewarisi BaseReportExporter)."""

    def __init__(self, filename="laporan_scan.pdf"):
        super().__init__(filename)

    def export(self, scan_data):
        """Implementasi polimorfis ekspor ke PDF."""
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors

        target_host = scan_data.get("target_host")
        target_ip = scan_data.get("target_ip")
        start_port = scan_data.get("start_port")
        end_port = scan_data.get("end_port")
        open_ports = scan_data.get("open_ports", [])

        doc = SimpleDocTemplate(self._filename, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            'TitleStyle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#1a365d'),
            spaceAfter=12,
            alignment=1
        )
        normal_style = styles['Normal']

        story.append(Paragraph("Laporan Hasil Pemindaian Port (Port Scanner)", title_style))
        story.append(Spacer(1, 12))

        summary_data = [
            [Paragraph("<b>Target Host:</b>", normal_style), Paragraph(str(target_host), normal_style)],
            [Paragraph("<b>Target IP:</b>", normal_style), Paragraph(str(target_ip), normal_style)],
            [Paragraph("<b>Rentang Port:</b>", normal_style), Paragraph(f"{start_port} - {end_port}", normal_style)],
            [Paragraph("<b>Waktu Eksekusi:</b>", normal_style), Paragraph(str(datetime.now()), normal_style)],
        ]

        summary_table = Table(summary_data, colWidths=[120, 380])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f7fafc')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e0')),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 15))

        story.append(Paragraph("<b>Daftar Port Terbuka</b>", styles['Heading2']))
        story.append(Spacer(1, 6))

        if open_ports:
            port_table_data = [["Port", "Status", "Layanan Umum (Estimasi)"]]
            for p in open_ports:
                if p in [80, 443]:
                    service = "HTTP/HTTPS"
                elif p == 22:
                    service = "SSH"
                elif p == 21:
                    service = "FTP"
                else:
                    service = "Lainnya/Custom"
                port_table_data.append([str(p), "TERBUKA", service])

            p_table = Table(port_table_data, colWidths=[100, 150, 250])
            p_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2b6cb0')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ffffff')),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
                ('PADDING', (0, 0), (-1, -1), 6),
            ]))
            story.append(p_table)
        else:
            story.append(Paragraph("Tidak ada port terbuka yang ditemukan pada rentang tersebut.", normal_style))

        doc.build(story)
        print(f"[+] Laporan berhasil dieksport ke PDF: {self._filename}")


class JSONReportExporter(BaseReportExporter):
    """Ekspor hasil pemindaian ke JSON (mewarisi BaseReportExporter)."""

    def __init__(self, filename="laporan_scan.json"):
        super().__init__(filename)

    def export(self, scan_data):
        """Implementasi polimorfis ekspor ke JSON."""
        target_host = scan_data.get("target_host")
        target_ip = scan_data.get("target_ip")
        start_port = scan_data.get("start_port")
        end_port = scan_data.get("end_port")
        open_ports = scan_data.get("open_ports", [])

        data = {
            "target_host": target_host,
            "target_ip": target_ip,
            "port_range": {
                "start": start_port,
                "end": end_port
            },
            "scan_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_open_ports": len(open_ports),
            "open_ports": [
                {
                    "port": p,
                    "status": "OPEN",
                    "estimated_service": self._get_service(p)
                }
                for p in open_ports
            ]
        }

        with open(self._filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        print(f"[+] Laporan berhasil dieksport ke JSON: {self._filename}")

    @staticmethod
    def _get_service(port):
        if port in [80, 443]:
            return "HTTP/HTTPS"
        elif port == 22:
            return "SSH"
        elif port == 21:
            return "FTP"
        else:
            return "Lainnya/Custom"
