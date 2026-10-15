import os

def generate_bw_wireframe_svg():
    svg = '''<svg width="1440" height="900" viewBox="0 0 1440 900" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&amp;display=swap');
      text { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; fill: #000000; }
      .wf-title { font-size: 11px; font-weight: 700; fill: #000000; text-transform: uppercase; letter-spacing: 0.8px; }
      .wf-val { font-size: 22px; font-weight: 800; fill: #000000; }
      .wf-sub { font-size: 11.5px; fill: #52525B; }
      .wf-tag { font-size: 10px; font-family: monospace; font-weight: 600; fill: #71717A; }
    </style>
  </defs>

  <!-- Canvas Background (Pure Wireframe White & Subtle Border) -->
  <rect width="1440" height="900" fill="#FFFFFF"/>
  <rect width="1440" height="900" stroke="#000000" stroke-width="2"/>

  <!-- ==================== SIDEBAR WIREFRAME (HITAM PUTIH) ==================== -->
  <g id="Sidebar_Wireframe">
    <!-- Sidebar Base Frame -->
    <rect width="280" height="900" fill="#FAFAFA" stroke="#000000" stroke-width="1.5"/>

    <!-- Tombol Back / Collapse Nav -->
    <g transform="translate(20, 20)">
      <rect width="96" height="32" rx="8" fill="#FFFFFF" stroke="#000000" stroke-width="1.5"/>
      <text x="14" y="21" font-size="14" font-weight="800">←</text>
      <text x="32" y="21" font-size="12" font-weight="700">Kembali</text>
    </g>

    <!-- Header / Logo Placeholder -->
    <g transform="translate(20, 68)">
      <!-- Placeholder Box for Icon -->
      <rect x="96" y="8" width="48" height="48" rx="8" fill="#FFFFFF" stroke="#000000" stroke-width="1.5"/>
      <line x1="96" y1="8" x2="144" y2="56" stroke="#D4D4D8" stroke-width="1"/>
      <line x1="144" y1="8" x2="96" y2="56" stroke="#D4D4D8" stroke-width="1"/>
      <text x="120" y="38" font-size="18" text-anchor="middle">💧</text>

      <text x="120" y="78" font-size="18" font-weight="800" text-anchor="middle">Water Monitoring</text>
      <text x="120" y="94" font-size="10" fill="#71717A" text-anchor="middle">[Wireframe Brand Header]</text>
    </g>

    <line x1="20" y1="175" x2="260" y2="175" stroke="#000000" stroke-width="1" stroke-dasharray="3 3"/>

    <!-- Radio Navigation Menu (3 Items) -->
    <g transform="translate(20, 190)">
      <text x="4" y="16" font-size="12" font-weight="800">MENU NAVIGASI</text>
      
      <!-- Option 1: Selected -->
      <g transform="translate(0, 30)">
        <rect width="240" height="32" rx="6" fill="#F4F4F5" stroke="#000000" stroke-width="1.5"/>
        <circle cx="16" cy="16" r="6" fill="#FFFFFF" stroke="#000000" stroke-width="2"/>
        <circle cx="16" cy="16" r="3" fill="#000000"/>
        <text x="32" y="20" font-size="12" font-weight="800">Dashboard Utama</text>
        <text x="228" y="20" font-size="9" fill="#71717A" text-anchor="end">&lt;Aktif&gt;</text>
      </g>

      <!-- Option 2: Default -->
      <g transform="translate(0, 68)">
        <rect width="240" height="32" rx="6" fill="#FFFFFF" stroke="#A1A1AA" stroke-width="1"/>
        <circle cx="16" cy="16" r="6" fill="#FFFFFF" stroke="#71717A" stroke-width="1.5"/>
        <text x="32" y="20" font-size="12" font-weight="500">Grafik dan Historis</text>
      </g>

      <!-- Option 3: Default -->
      <g transform="translate(0, 106)">
        <rect width="240" height="32" rx="6" fill="#FFFFFF" stroke="#A1A1AA" stroke-width="1"/>
        <circle cx="16" cy="16" r="6" fill="#FFFFFF" stroke="#71717A" stroke-width="1.5"/>
        <text x="32" y="20" font-size="12" font-weight="500">Riwayat &amp; Notifikasi</text>
      </g>
    </g>

    <line x1="20" y1="345" x2="260" y2="345" stroke="#000000" stroke-width="1" stroke-dasharray="3 3"/>

    <!-- Hardware Status Box Placeholder -->
    <g transform="translate(20, 360)">
      <rect width="240" height="74" rx="10" fill="#FFFFFF" stroke="#000000" stroke-width="1.5"/>
      <circle cx="16" cy="20" r="4.5" fill="#000000"/>
      <text x="26" y="24" font-size="11" font-weight="800">STATUS HARDWARE (ESP32)</text>
      <text x="16" y="44" font-size="10.5" fill="#000000">Waktu: <tspan font-weight="700">HH:MM:SS (Live)</tspan></text>
      <text x="16" y="60" font-size="10" fill="#52525B">IP: [10.207.82.29] Online</text>
    </g>

    <!-- Checkbox Auto-Refresh -->
    <g transform="translate(20, 448)">
      <rect width="18" height="18" rx="4" fill="#FFFFFF" stroke="#000000" stroke-width="1.5"/>
      <path d="M4 9L8 13L14 5" stroke="#000000" stroke-width="2" stroke-linecap="round"/>
      <text x="26" y="14" font-size="11.5" font-weight="700">[✓] Auto-Refresh Live Data</text>
    </g>

    <line x1="20" y1="480" x2="260" y2="480" stroke="#000000" stroke-width="1" stroke-dasharray="3 3"/>

    <!-- Telegram Bot Section -->
    <g transform="translate(20, 495)">
      <text x="0" y="16" font-size="12" font-weight="800">MODUL TELEGRAM BOT</text>
      
      <!-- Toggle Switch Wireframe -->
      <text x="0" y="44" font-size="11" font-weight="600">Notifikasi otomatis</text>
      <rect x="186" y="32" width="46" height="20" rx="10" fill="#E4E4E7" stroke="#000000" stroke-width="1.5"/>
      <circle cx="220" cy="42" r="7" fill="#000000"/>
      
      <!-- Captions -->
      <text x="0" y="74" font-size="10" fill="#52525B">Perintah: /status /on /off /dashboard /menu</text>
      <text x="0" y="90" font-size="10" fill="#52525B">Penerima terdaftar: [N Subscriber]</text>
      
      <!-- Button Wireframe -->
      <rect x="0" y="104" width="130" height="34" rx="17" fill="#FFFFFF" stroke="#000000" stroke-width="1.5"/>
      <text x="65" y="125" font-size="11" font-weight="800" text-anchor="middle">[ Tes Telegram ]</text>
    </g>
  </g>

  <!-- ==================== MAIN CONTENT WIREFRAME (HITAM PUTIH) ==================== -->
  <g id="Main_Content_Wireframe" transform="translate(310, 32)">
    
    <!-- Title Wireframe -->
    <text x="0" y="28" font-size="26" font-weight="800">Dashboard Monitoring Air</text>
    <text x="360" y="28" font-size="11" class="wf-tag">&lt;Halaman Utama / Viewport Desktop&gt;</text>

    <!-- ==================== BARIS 1: 5 METRIC CARDS WIREFRAME ==================== -->
    <g id="Metric_Grid_Wireframe" transform="translate(0, 56)">
      
      <!-- CARD 1: STATUS PWM -->
      <g transform="translate(0, 0)">
        <rect width="210" height="125" rx="14" fill="#FFFFFF" stroke="#000000" stroke-width="1.5"/>
        <text x="16" y="26" class="wf-title">STATUS PWM</text>
        <text x="16" y="66" class="wf-val">PWM [0-255]</text>
        <text x="16" y="92" class="wf-sub">Duty: <b>[%]</b> ([V] DC)</text>
        <text x="16" y="112" class="wf-tag">[Modulasi Driver MOSFET]</text>
      </g>

      <!-- CARD 2: STATUS KECEPATAN -->
      <g transform="translate(225, 0)">
        <rect width="210" height="125" rx="14" fill="#FFFFFF" stroke="#000000" stroke-width="1.5"/>
        <text x="16" y="26" class="wf-title">STATUS KECEPATAN</text>
        <text x="16" y="66" class="wf-val">[STATUS]</text>
        <text x="16" y="92" class="wf-sub">Mode: <b>Otonom Cerdas</b></text>
        <text x="16" y="112" class="wf-tag">[Inferensi Fuzzy Mamdani]</text>
      </g>

      <!-- CARD 3: KUALITAS AIR -->
      <g transform="translate(450, 0)">
        <rect width="210" height="125" rx="14" fill="#FFFFFF" stroke="#000000" stroke-width="1.5"/>
        <text x="16" y="26" class="wf-title">KUALITAS AIR</text>
        <text x="16" y="66" class="wf-val">[Nilai] <tspan font-size="13">NTU</tspan></text>
        <text x="16" y="92" class="wf-sub">Status: <b>[Jernih / Keruh]</b></text>
        <text x="16" y="112" class="wf-tag">[Sensor Turbidity]</text>
      </g>

      <!-- CARD 4: DEBIT AIR MASUK -->
      <g transform="translate(675, 0)">
        <rect width="210" height="125" rx="14" fill="#FFFFFF" stroke="#000000" stroke-width="1.5"/>
        <text x="16" y="26" class="wf-title">DEBIT AIR MASUK</text>
        <text x="16" y="66" class="wf-val">[Nilai] <tspan font-size="13">L/min</tspan></text>
        <text x="16" y="92" class="wf-sub">Sensor Aliran Masuk</text>
        <text x="16" y="112" class="wf-tag">[Sensor YF-S201]</text>
      </g>

      <!-- CARD 5: TOTAL AIR TERPAKAI -->
      <g transform="translate(900, 0)">
        <rect width="210" height="125" rx="14" fill="#FFFFFF" stroke="#000000" stroke-width="1.5"/>
        <text x="16" y="26" class="wf-title">TOTAL AIR TERPAKAI</text>
        <text x="16" y="66" class="wf-val">[Nilai] <tspan font-size="13">Liter</tspan></text>
        <text x="16" y="92" class="wf-sub">Akumulasi Pengisian</text>
        <text x="16" y="112" class="wf-tag">[Integrasi Volume]</text>
      </g>
    </g>

    <!-- ==================== BARIS 2: LEVEL BAK MANDI WIREFRAME ==================== -->
    <g id="Row_2_Tank_Wireframe" transform="translate(0, 205)">
      <rect width="1110" height="280" rx="18" fill="#FFFFFF" stroke="#000000" stroke-width="1.5"/>
      
      <!-- Title -->
      <text x="555" y="42" font-size="18" font-weight="800" text-anchor="middle">Ketinggian Bak Mandi</text>
      <text x="555" y="60" font-size="11" fill="#71717A" text-anchor="middle">[Komponen Hero Visualizer Utama]</text>
      
      <!-- Percentage Placeholder -->
      <text x="555" y="132" font-size="64" font-weight="800" text-anchor="middle">[ 0% - 100% ]</text>
      
      <!-- Progress Bar Wireframe Track -->
      <g transform="translate(155, 160)">
        <rect width="800" height="18" rx="9" fill="#F4F4F5" stroke="#000000" stroke-width="1.5"/>
        <!-- Fill indicator wireframe -->
        <rect width="320" height="18" rx="9" fill="#71717A"/>
        <line x1="320" y1="0" x2="320" y2="18" stroke="#000000" stroke-width="2"/>
        <text x="320" y="-6" font-size="9" font-family="monospace" font-weight="700" text-anchor="middle">Level Bar</text>
      </g>
      
      <!-- Distance info placeholder -->
      <text x="555" y="218" font-size="13.5" text-anchor="middle">
        Jarak Permukaan ke Sensor: <tspan font-weight="700">[Jarak] cm</tspan> (Tinggi Bak Acuan: 72 cm)
      </text>
      
      <text x="555" y="244" font-size="11" fill="#71717A" font-style="italic" text-anchor="middle">
        Diperbarui dari ESP32: [HH:MM:SS] (Sinkronisasi Firebase Realtime Database)
      </text>
    </g>

    <!-- ==================== BARIS 3: ANOTASI UX WIREFRAME ==================== -->
    <g id="Row_3_Annotations" transform="translate(0, 510)">
      <rect width="1110" height="140" rx="14" fill="#FAFAFA" stroke="#000000" stroke-width="1" stroke-dasharray="4 4"/>
      <text x="24" y="28" font-size="12" font-weight="800">KETERANGAN KERANGKA UX (WIREFRAME SPECIFICATION):</text>
      
      <g transform="translate(24, 46)">
        <text x="0" y="14" font-size="11" fill="#27272A">• <b>Grid System:</b> Menggunakan 5-Column Responsive Flex/Grid Layout dengan rasio lebar kartu metrik 210px dan tinggi konsisten 125px.</text>
        <text x="0" y="34" font-size="11" fill="#27272A">• <b>Hierarki Informasi:</b> Informasi kritis (Status Motor &amp; Kekeruhan Air) ditempatkan di baris atas untuk deteksi status seketika (Immediate Cognition).</text>
        <text x="0" y="54" font-size="11" fill="#27272A">• <b>Navigasi Konsisten:</b> Sidebar kiri bersifat persisten (selalu tersedia) dengan navigasi 3 opsi radio tanpa ikon emoji guna menjaga formalitas ilmiah.</text>
        <text x="0" y="74" font-size="11" fill="#27272A">• <b>Feedback Realtime:</b> Slot Waktu, IP ESP32, dan Switch Telegram memberikan umpan balik status operasional sistem secara transparan.</text>
      </g>
    </g>

  </g>
</svg>'''

    out_path = r"D:\proyek 3 & proposal ta\web\figma\kerangka_ux_wireframe_bw.svg"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print("Berhasil membuat kerangka_ux_wireframe_bw.svg di:", out_path)

if __name__ == "__main__":
    generate_bw_wireframe_svg()
