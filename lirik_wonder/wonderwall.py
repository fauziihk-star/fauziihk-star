# Menampilkan dan memutar bagian reff pertama "Wonderwall".
import sys
import time
import subprocess
import os
from pathlib import Path


NAMA_AUDIO = "Wonderwall - Oasis Lirik Terjemahan Indonesia.mp3"
# Posisi "Because maybe" pada versi audio yang ada di folder project.
WAKTU_MULAI_REFF = 87.0
DURASI_REFF = 26.0


def siapkan_pemutar(folder_project):
    """Kompilasi pemutar macOS bila belum ada atau source-nya berubah."""
    sumber = folder_project / "pemutar_reff.swift"
    pemutar = folder_project / ".pemutar_reff"

    if not pemutar.exists() or sumber.stat().st_mtime > pemutar.stat().st_mtime:
        print("Menyiapkan pemutar audio...")
        lingkungan = os.environ.copy()
        # Menghindari masalah izin cache compiler pada lingkungan yang dibatasi.
        lingkungan["CLANG_MODULE_CACHE_PATH"] = "/private/tmp/lirik_wonder_swift_cache"
        subprocess.run(
            ["swiftc", str(sumber), "-o", str(pemutar)],
            check=True,
            env=lingkungan,
        )
    return pemutar


def putar_audio_reff(folder_project):
    """Memutar MP3 langsung dari awal reff dan berhenti setelah reff selesai."""
    audio = folder_project / NAMA_AUDIO
    if not audio.exists():
        raise FileNotFoundError(f"File audio tidak ditemukan: {audio.name}")

    pemutar = siapkan_pemutar(folder_project)
    return subprocess.Popen(
        [str(pemutar), str(audio), str(WAKTU_MULAI_REFF), str(DURASI_REFF)]
    )


def putar_lirik(data_lirik):
    """Tampilkan tiap baris tepat pada waktu reff yang sesuai."""
    awal_reff = time.monotonic()

    for teks, waktu_baris, jeda_huruf in data_lirik:
        sisa_waktu = awal_reff + waktu_baris - time.monotonic()
        if sisa_waktu > 0:
            time.sleep(sisa_waktu)

        for huruf in teks:
            sys.stdout.write(huruf)
            sys.stdout.flush()
            time.sleep(jeda_huruf)
        print()


def main():
    folder_project = Path(__file__).resolve().parent

    # Tuple: (lirik, detik sejak reff dimulai, jeda ketik per huruf).
    # Waktunya disesuaikan dengan "Because maybe" pada detik 01:27 di MP3.
    lirik_wonderwall = [
        ("Because maybeeeeeeeeeeeeeee........................................", 1.0, 0.050),
        ("You're gonna be the one that saves meeeeeeeeeeeeeeeeeeeeeeee....................", 5.0, 0.060),
        ("And after all......................................................", 11.0, 0.055),
        ("You're my wonderwallllllllllllllllll..........................................", 16.0, 0.050),
    ]

    print("\n--- Memutar reff Wonderwall (01:27 - 01:53) ---\n")
    proses_audio = putar_audio_reff(folder_project)
    awal_putar = time.monotonic()

    try:
        putar_lirik(lirik_wonderwall)
        waktu_sisa = DURASI_REFF - (time.monotonic() - awal_putar)
        if waktu_sisa > 0:
            time.sleep(waktu_sisa)
    except KeyboardInterrupt:
        print("\nPemutaran dihentikan.")
    finally:
        if proses_audio.poll() is None:
            proses_audio.terminate()
            proses_audio.wait()

    print("\n--- Reff selesai ---")

# Menjalankan program
if __name__ == "__main__":
    main()
