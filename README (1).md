# Verifikasi Ijazah: OCR Nomor Ijazah dan Deteksi Tanda Tangan

## Deskripsi

Proyek ini merupakan prototype pengolahan citra untuk membantu verifikasi ijazah melalui dua proses:

1. **OCR:** membaca nomor ijazah menggunakan Tesseract.
2. **Deteksi tanda tangan:** memeriksa keberadaan tanda tangan Rektor dan Dekan menggunakan pengolahan citra.

Contoh hasil:

```text
Input        : 01_HighQuality_Enhanced.jpg
Nomor Ijazah : 571012022000056
Tanda Tangan : PRESENT
- Rektor     : PRESENT
- Dekan      : PRESENT
- Pemilik    : PRESENT (informasi tambahan)
```

## 1. Struktur File

| File | Fungsi |
|---|---|
| `TUGAS7_VerifIjazah.ipynb` | Notebook utama untuk pemrosesan citra dan verifikasi |
| `eval_cer.py` | Menguji dan membandingkan metode enhancement menggunakan CER |
| `01_HighQuality_Enhanced.jpg` | Contoh gambar ijazah |
| `README.md` | Dokumentasi proyek |

## 2. Metode yang Digunakan

### A. Grayscale

Mengubah gambar berwarna menjadi keabuan menggunakan OpenCV. Tahap ini menyederhanakan gambar agar lebih mudah diproses.

### B. Image Enhancement

Menggunakan Gaussian Blur untuk mengurangi noise dan CLAHE untuk meningkatkan kontras agar teks lebih jelas, terutama pada gambar dengan kontras rendah.

### C. Region of Interest (ROI)

Memotong bagian gambar yang diperlukan, yaitu nomor ijazah dan area tanda tangan. Cara ini membantu program berfokus pada informasi yang ingin diperiksa.

### D. OCR Nomor Ijazah

Area nomor diperbesar 2× menggunakan interpolasi bikubik, kemudian diproses dengan metode Otsu untuk memisahkan teks dari latar belakang. Tesseract OCR digunakan untuk membaca nomor, sedangkan parsing digunakan untuk mengambil nomor ijazah dari hasil teks.

### E. Deteksi Tanda Tangan

Deteksi dilakukan melalui tiga tahap:

1. **Thresholding:** memisahkan goresan tanda tangan dari latar belakang berdasarkan perbedaan intensitas.
2. **Morphological Closing:** menyambungkan goresan yang terputus atau memiliki celah kecil.
3. **Analisis komponen terhubung:** memeriksa luas, lebar, dan jumlah piksel goresan untuk menentukan apakah tanda tangan terdeteksi.

Status `PRESENT` diberikan jika area memenuhi kriteria deteksi. Hasil akhir dinyatakan `PRESENT` apabila tanda tangan Rektor dan Dekan sama-sama terdeteksi. Tanda tangan pemilik merupakan informasi tambahan.

## 3. Analisis Hasil Output

Pada gambar `01_HighQuality_Enhanced.jpg`, OCR berhasil membaca nomor ijazah `571012022000056`. Ketiga area tanda tangan juga terdeteksi sebagai `PRESENT`.

Hasil visual menunjukkan bahwa thresholding dapat memperjelas goresan tanda tangan, sedangkan morphological closing membantu menyambungkan goresan yang terputus. Namun, beberapa teks cetak di sekitar tanda tangan Dekan masih ikut terdeteksi.

Hasil ini menunjukkan bahwa program berhasil memproses gambar pengujian, tetapi status `PRESENT` hanya menunjukkan keberadaan pola yang menyerupai tanda tangan, bukan membuktikan keaslian tanda tangan atau ijazah.

## 4. Evaluasi Enhancement Berdasarkan CER

### A. Pengertian CER

Character Error Rate (CER) digunakan untuk mengukur kesalahan karakter pada hasil OCR dibandingkan dengan teks acuan (*ground truth*).

Rumus:

\[
CER = \frac{S+D+I}{N}
\]

Keterangan:
- `S`: jumlah karakter yang salah.
- `D`: jumlah karakter yang terhapus.
- `I`: jumlah karakter tambahan.
- `N`: jumlah karakter pada teks acuan.

**Semakin rendah nilai CER, semakin baik hasil OCR.** Nilai CER 0 berarti hasil OCR sama persis dengan teks acuan.

### B. Hasil Pengujian

Pengujian dilakukan menggunakan delapan metode enhancement pada gambar asli dan lima kondisi degradasi, yaitu penurunan resolusi, noise, blur, kontras rendah, dan kompresi JPEG.

Hasil CER rata-rata untuk nomor ijazah:

| Metode | Rata-rata CER |
|---|---:|
| Tanpa enhancement (grayscale) | 0,167 |
| Upscale 2× | 0,167 |
| CLAHE | **0,000** |
| Otsu | 0,044 |
| Adaptive Threshold | 0,167 |
| CLAHE + Otsu | **0,000** |
| Sharpen + Otsu | 0,167 |
| Median Blur + Otsu | **0,000** |

Untuk teks satu baris secara keseluruhan, hasil CER rata-ratanya adalah:

| Metode | Rata-rata CER |
|---|---:|
| CLAHE + Otsu | **0,029** |
| CLAHE | 0,034 |
| Median Blur + Otsu | 0,046 |
| Otsu | 0,052 |
| Upscale 2× | 0,075 |
| Tanpa enhancement (grayscale) | 0,172 |
| Adaptive Threshold | 0,213 |
| Sharpen + Otsu | 0,218 |

### C. Kesimpulan CER

Berdasarkan hasil pengujian, **CLAHE + Otsu merupakan metode paling efektif secara keseluruhan** karena menghasilkan CER rata-rata terendah untuk teks satu baris, yaitu 0,029. Pada pembacaan nomor ijazah setelah parsing, metode ini memperoleh CER 0,000 pada seluruh kondisi pengujian.

CLAHE membantu meningkatkan kontras, sedangkan Otsu memisahkan teks dari latar belakang. Kombinasi keduanya menghasilkan pembacaan yang lebih konsisten dibandingkan metode lainnya.

CLAHE dan Median Blur + Otsu juga memperoleh CER nomor rata-rata 0,000. Namun, CLAHE + Otsu tetap unggul dalam pengujian teks satu baris secara keseluruhan.

Kesalahan pembacaan pada kata *Nomor ijazah* masih dapat terjadi karena bentuk atau titik huruf kurang jelas. Kesalahan tersebut tidak memengaruhi hasil nomor setelah parsing karena sistem mengambil bagian nomor saja.

## 5. Cara Menjalankan Kode

### A. Google Colab

1. Buka [Google Colab](https://colab.research.google.com/).
2. Unggah `TUGAS7_VerifIjazah.ipynb`.
3. Unggah gambar ijazah melalui panel **Files**.
4. Sesuaikan nama file pada konfigurasi:

   ```python
   IMAGE_PATH = "01_HighQuality_Enhanced.jpg"
   ```

5. Jalankan semua sel melalui menu **Runtime → Run all**.
6. Periksa hasil OCR, visualisasi pemrosesan citra, dan status tanda tangan.

Notebook dapat memasang kebutuhan sistem dan library melalui sel instalasi yang tersedia.

### B. Komputer Lokal

Pastikan Python dan Tesseract OCR sudah terpasang.

- **Windows:** instal Tesseract melalui [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki).
- **Ubuntu/Debian:**

  ```bash
  sudo apt install tesseract-ocr
  ```

- **macOS:**

  ```bash
  brew install tesseract
  ```

Instal library Python:

```bash
python -m pip install opencv-python-headless pytesseract matplotlib numpy jupyter
```

Jika menggunakan Windows, sesuaikan lokasi Tesseract pada notebook:

```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

Letakkan notebook dan gambar ijazah di folder proyek, kemudian jalankan:

```bash
jupyter notebook TUGAS7_VerifIjazah.ipynb
```

Sesuaikan `IMAGE_PATH`, lalu pilih **Run All**.

> Catatan: perintah `!apt-get` pada notebook ditujukan untuk lingkungan seperti Google Colab atau Ubuntu. Pada Windows dan macOS, instal Tesseract melalui langkah di atas.

### C. Menjalankan Evaluasi CER

Sesuaikan `GT_NUM` dan `GT_LINE` di `eval_cer.py` berdasarkan nomor dan teks yang benar pada gambar ijazah.

Jalankan perintah:

```bash
python eval_cer.py
```

Skrip akan membandingkan hasil OCR dari berbagai metode enhancement. Pastikan teks acuan diketik dengan benar agar nilai CER akurat.

### D. Menyesuaikan Area ROI

Jika posisi nomor atau tanda tangan berbeda, sesuaikan koordinat ROI pada notebook. Contohnya:

```python
ROI_NOMOR = (0.04, 0.90, 0.32, 0.97)

ROI_TTD = {
    "Rektor": (0.12, 0.72, 0.40, 0.83),
    "Dekan": (0.62, 0.66, 0.88, 0.84)
}
```

Koordinat menggunakan format `(x1, y1, x2, y2)` dengan nilai relatif 0–1. Sesuaikan nilainya hingga kotak tepat mencakup area yang diperlukan.

## 6. Masalah yang Sering Muncul

| Masalah | Solusi |
|---|---|
| `TesseractNotFoundError` | Instal Tesseract atau perbaiki lokasi executable |
| Gambar tidak terbaca | Periksa nama dan lokasi file pada `IMAGE_PATH` |
| Nomor salah atau `None` | Periksa ROI nomor dan kualitas gambar |
| Tanda tangan tidak terdeteksi | Periksa ROI, kualitas citra, dan parameter thresholding |

## 7. Batasan Sistem

- Hasil deteksi tanda tangan tidak membuktikan keaslian tanda tangan atau ijazah.
- Hasil OCR dipengaruhi kualitas gambar dan posisi ROI.
- Nilai CER bergantung pada ketepatan teks acuan.
- Pengujian tambahan pada lebih banyak gambar diperlukan untuk menilai kinerja sistem secara lebih luas.
