import socket
import sys
from abc import ABC, abstractmethod
from datetime import datetime


class BaseScanner(ABC):
    """Kerangka abstraksi untuk pemindaian jaringan."""

    def __init__(self, target_host, start_port, end_port, timeout=0.5):
        self._target_host = target_host
        self._target_ip = self._resolve_host(target_host)
        self._start_port = start_port
        self._end_port = end_port
        self._timeout = timeout
        self._open_ports = []

    def _resolve_host(self, target_host):
        """Menyelesaikan nama host menjadi alamat IP (atribut terenkapsulasi)."""
        try:
            return socket.gethostbyname(target_host)
        except socket.gaierror:
            print("\n[!] Host tidak dapat diselesaikan. Periksa kembali nama/IP target.")
            sys.exit(1)

    @abstractmethod
    def scan(self):
        """Metode pemindaian yang harus diimplementasikan oleh kelas turunan."""
        pass

    def get_target_host(self):
        """Antarmuka publik untuk mengakses host target."""
        return self._target_host

    def get_target_ip(self):
        """Antarmuka publik untuk mengakses IP target."""
        return self._target_ip

    def get_start_port(self):
        """Antarmuka publik untuk mengakses port awal."""
        return self._start_port

    def get_end_port(self):
        """Antarmuka publik untuk mengakses port akhir."""
        return self._end_port

    def get_open_ports(self):
        """Antarmuka publik untuk mengakses daftar port terbuka."""
        return list(self._open_ports)


class TCPPortScanner(BaseScanner):
    """Kelas konkret untuk pemindaian port TCP (mewarisi BaseScanner)."""

    def __init__(self, target_host, start_port, end_port, timeout=0.5):
        super().__init__(target_host, start_port, end_port, timeout)

    def scan(self):
        """Melakukan pemindaian port TCP secara polimorfis."""
        self._open_ports.clear()

        print("-" * 50)
        print(f" Memindai Target IP: {self._target_ip}")
        print(f" Rentang Port      : {self._start_port} - {self._end_port}")
        print(f" Waktu Mulai       : {str(datetime.now())}")
        print("-" * 50)

        try:
            for port in range(self._start_port, self._end_port + 1):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(self._timeout)
                result = s.connect_ex((self._target_ip, port))
                s.close()

                if result == 0:
                    print(f"[+] Port {port} : TERBUKA")
                    self._open_ports.append(port)

        except KeyboardInterrupt:
            print("\n[!] Pemindaian dibatalkan oleh pengguna (Ctrl+C).")

        print("-" * 50)
        print(f" Pemindaian Selesai. Total port terbuka ditemukan: {len(self._open_ports)}")
        print("-" * 50)

        return self.get_open_ports()
