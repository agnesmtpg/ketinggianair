import os

def get_sidebar_bw(active_index=0):
    # active_index: 0=Dashboard, 1=Grafik, 2=Riwayat
    r1_circle = '<circle cx="16" cy="16" r="6" fill="#FFFFFF" stroke="#000000" stroke-width="2"/><circle cx="16" cy="16" r="3" fill="#000000"/>' if active_index == 0 else '<circle cx="16" cy="16" r="6" fill="#FFFFFF" stroke="#71717A" stroke-width="1.5"/>'
    r1_box = '<rect width="240" height="32" rx="6" fill="#F4F4F5" stroke="#000000" stroke-width="1.5"/>' if active_index == 0 else '<rect width="240" height="32" rx="6" fill="#FFFFFF" stroke="#A1A1AA" stroke-width="1"/>'
    r1_weight = '800' if active_index == 0 else '500'

    r2_circle = '<circle cx="16" cy="16" r="6" fill="#FFFFFF" stroke="#000000" stroke-width="2"/><circle cx="16" cy="16" r="3" fill="#000000"/>' if active_index == 1 else '<circle cx="16" cy="16" r="6" fill="#FFFFFF" stroke="#71717A" stroke-width="1.5"/>'
    r2_box = '<rect width="240" height="32" rx="6" fill="#F4F4F5" stroke="#000000" stroke-width="1.5"/>' if active_index == 1 else '<rect width="240" height="32" rx="6" fill="#FFFFFF" stroke="#A1A1AA" stroke-width="1"/>'
    r2_weight = '800' if active_index == 1 else '500'

    r3_circle = '<circle cx="16" cy="16" r="6" fill="#FFFFFF" stroke="#000000" stroke-width="2"/><circle cx="16" cy="16" r="3" fill="#000000"/>' if active_index == 2 else '<circle cx="16" cy="16" r="6" fill="#FFFFFF" stroke="#71717A" stroke-width="1.5"/>'
    r3_box = '<rect width="240" height="32" rx="6" fill="#F4F4F5" stroke="#000000" stroke-width="1.5"/>' if active_index == 2 else '<rect width="240" height="32" rx="6" fill="#FFFFFF" stroke="#A1A1AA" stroke-width="1"/>'
    r3_weight = '800' if active_index == 2 else '500'

    subpage_btn = ''
    if active_index != 0:
        subpage_btn = '''
      <!-- Tombol Kembali ke Dashboard (Sidebar) -->
      <g transform="translate(0, 144)">
        <rect width="240" height="32" rx="16" fill="#FFFFFF" stroke="#000000" stroke-width="1.5"/>
        <text x="120" y="20" font-size="11" font-weight="700" text-anchor="middle">← Kembali ke Dashboard</text>
      </g>'''

    return f'''
  <!-- SIDEBAR WIREFRAME (HITAM PUTIH) -->
  <g id="Sidebar_Wireframe">
    <rect width="280" height="900" fill="#FAFAFA" stroke="#000000" stroke-width="1.5"/>

    <!-- Tombol Back / Collapse Nav -->
    <g transform="translate(20, 20)">
      <rect width="96" height="32" rx="8" fill="#FFFFFF" stroke="#000000" stroke-width="1.5"/>
      <text x="14" y="21" font-size="14" font-weight="800">←</text>
      <text x="32" y="21" font-size="12" font-weight="700">Kembali</text>
    </g>

    <!-- Header / Brand -->
    <g transform="translate(20, 68)">
      <rect x="96" y="8" width="48" height="48" rx="8" fill="#FFFFFF" stroke="#000000" stroke-width="1.5"/>
      <line x1="96" y1="8" x2="144" y2="56" stroke="#D4D4D8" stroke-width="1"/>
      <line x1="144" y1="8" x2="96" y2="56" stroke="#D4D4D8" stroke-width="1"/>
      <text x="120" y="38" font-size="18" text-anchor="middle">💧</text>

      <text x="120" y="78" font-size="18" font-weight="800" text-anchor="middle">Water Monitoring</text>
      <text x="120" y="94" font-size="10" fill="#71717A" text-anchor="middle">[Wireframe Brand Header]</text>
    </g>

    <line x1="20" y1="175" x2="260" y2="175" stroke="#000000" stroke-width="1" stroke-dasharray="3 3"/>

    <!-- Radio Navigation Menu -->
    <g transform="translate(20, 190)">
      <text x="4" y="16" font-size="12" font-weight="800">MENU</text>
      
      <!-- Option 1: Dashboard -->
      <g transform="translate(0, 30)">
        {r1_box}
        {r1_circle}
        <text x="32" y="20" font-size="12" font-weight="{r1_weight}">Dashboard Utama</text>
      </g>

      <!-- Option 2: Grafik -->
      <g transform="translate(0, 68)">
        {r2_box}
        {r2_circle}
        <text x="32" y="20" font-size="12" font-weight="{r2_weight}">Grafik dan Historis</text>
      </g>

      <!-- Option 3: Riwayat -->
      <g transform="translate(0, 106)">
        {r3_box}
        {r3_circle}
        <text x="32" y="20" font-size="12" font-weight="{r3_weight}">Riwayat &amp; Notifikasi</text>
      </g>
      {subpage_btn}
    </g>

    <line x1="20" y1="375" x2="260" y2="375" stroke="#000000" stroke-width="1" stroke-dasharray="3 3"/>

    <!-- Status ESP32 -->
    <g transform="translate(20, 390)">
      <rect width="240" height="74" rx="10" fill="#FFFFFF" stroke="#000000" stroke-width="1.5"/>
      <circle cx="16" cy="20" r="4.5" fill="#000000"/>
      <text x="26" y="24" font-size="11" font-weight="800">STATUS HARDWARE (ESP32)</text>
      <text x="16" y="44" font-size="10.5">Waktu: <tspan font-weight="700">HH:MM:SS</tspan></text>
      <text x="16" y="60" font-size="10" fill="#52525B">IP: [10.207.82.29] Online</text>
    </g>

    <!-- Checkbox Auto-Refresh -->
    <g transform="translate(20, 476)">
      <rect width="18" height="18" rx="4" fill="#FFFFFF" stroke="#000000" stroke-width="1.5"/>
      <path d="M4 9L8 13L14 5" stroke="#000000" stroke-width="2" stroke-linecap="round"/>
      <text x="26" y="14" font-size="11.5" font-weight="700">[✓] Auto-Refresh Live Data</text>
    </g>

    <line x1="20" y1="506" x2="260" y2="506" stroke="#000000" stroke-width="1" stroke-dasharray="3 3"/>

    <!-- Telegram Bot Section -->
    <g transform="translate(20, 520)">
      <text x="0" y="16" font-size="12" font-weight="800">MODUL TELEGRAM BOT</text>
      
      <!-- Toggle -->
      <text x="0" y="44" font-size="11" font-weight="600">Notifikasi otomatis</text>
      <rect x="186" y="32" width="46" height="20" rx="10" fill="#E4E4E7" stroke="#000000" stroke-width="1.5"/>
      <circle cx="220" cy="42" r="7" fill="#000000"/>
      
      <text x="0" y="74" font-size="10" fill="#52525B">Perintah: /status /on /off /dashboard /menu</text>
      <text x="0" y="90" font-size="10" fill="#52525B">Penerima terdaftar: [1 Subscriber]</text>
      
      <!-- Button -->
      <rect x="0" y="104" width="130" height="34" rx="17" fill="#FFFFFF" stroke="#000000" stroke-width="1.5"/>
      <text x="65" y="125" font-size="11" font-weight="800" text-anchor="middle">[ Tes Telegram ]</text>
    </g>
  </g>'''


def get_menu1_body():
    return '''
  <!-- MAIN CONTENT: MENU 1 DASHBOARD UTAMA -->
  <g id="Main_Content" transform="translate(310, 32)">
    <text x="0" y="28" font-size="26" font-weight="800">Dashboard Monitoring Air</text>
    <text x="360" y="28" font-size="11" font-family="monospace" fill="#71717A">&lt;Menu 1: Dashboard Utama&gt;</text>

    <!-- 5 METRIC CARDS -->
    <g transform="translate(0, 56)">
      <!-- Card 1 -->
      <g transform="translate(0, 0)">
        <rect width="210" height="125" rx="14" fill="#FFFFFF" stroke="#000000" stroke-width="1.5"/>
        <text x="16" y="26" font-size="11" font-weight="700">STATUS PWM</text>
        <text x="16" y="66" font-size="22" font-weight="800">PWM [0-255]</text>
        <text x="16" y="92" font-size="11.5" fill="#52525B">Duty: <b>[%]</b> ([V] DC)</text>
        <text x="16" y="112" font-size="9.5" font-family="monospace" fill="#71717A">[Driver MOSFET D4184]</text>
      </g>
      <!-- Card 2 -->
      <g transform="translate(225, 0)">
        <rect width="210" height="125" rx="14" fill="#FFFFFF" stroke="#000000" stroke-width="1.5"/>
        <text x="16" y="26" font-size="11" font-weight="700">STATUS KECEPATAN</text>
        <text x="16" y="66" font-size="20" font-weight="800">[CEPAT / SEDANG / PELAN]</text>
        <text x="16" y="92" font-size="11.5" fill="#52525B">Mode: <b>Otonom Cerdas</b></text>
        <text x="16" y="112" font-size="9.5" font-family="monospace" fill="#71717A">[Fuzzy Mamdani Engine]</text>
      </g>
      <!-- Card 3 -->
      <g transform="translate(450, 0)">
        <rect width="210" height="125" rx="14" fill="#FFFFFF" stroke="#000000" stroke-width="1.5"/>
        <text x="16" y="26" font-size="11" font-weight="700">KUALITAS AIR</text>
        <text x="16" y="66" font-size="22" font-weight="800">[Nilai] <tspan font-size="13">NTU</tspan></text>
        <text x="16" y="92" font-size="11.5" fill="#52525B">Status: <b>[Jernih / Keruh]</b></text>
        <text x="16" y="112" font-size="9.5" font-family="monospace" fill="#71717A">[Sensor Turbidity]</text>
      </g>
      <!-- Card 4 -->
      <g transform="translate(675, 0)">
        <rect width="210" height="125" rx="14" fill="#FFFFFF" stroke="#000000" stroke-width="1.5"/>
        <text x="16" y="26" font-size="11" font-weight="700">DEBIT AIR MASUK</text>
        <text x="16" y="66" font-size="22" font-weight="800">[Nilai] <tspan font-size="13">L/min</tspan></text>
        <text x="16" y="92" font-size="11.5" fill="#52525B">Sensor Aliran Air</text>
        <text x="16" y="112" font-size="9.5" font-family="monospace" fill="#71717A">[Sensor YF-S201]</text>
      </g>
      <!-- Card 5 -->
      <g transform="translate(900, 0)">
        <rect width="210" height="125" rx="14" fill="#FFFFFF" stroke="#000000" stroke-width="1.5"/>
        <text x="16" y="26" font-size="11" font-weight="700">TOTAL AIR TERPAKAI</text>
        <text x="16" y="66" font-size="22" font-weight="800">[Nilai] <tspan font-size="13">Liter</tspan></text>
        <text x="16" y="92" font-size="11.5" fill="#52525B">Akumulasi Volume</text>
        <text x="16" y="112" font-size="9.5" font-family="monospace" fill="#71717A">[Integrasi Pulsa]</text>
      </g>
    </g>

    <!-- TANK HERO CONTAINER -->
    <g transform="translate(0, 205)">
      <rect width="1110" height="280" rx="18" fill="#FFFFFF" stroke="#000000" stroke-width="1.5"/>
      <text x="555" y="42" font-size="18" font-weight="800" text-anchor="middle">Ketinggian Bak Mandi</text>
      <text x="555" y="60" font-size="11" fill="#71717A" text-anchor="middle">[Komponen Hero Visualizer]</text>
      
      <text x="555" y="132" font-size="64" font-weight="800" text-anchor="middle">[ 0% - 100% ]</text>
      
      <g transform="translate(155, 160)">
        <rect width="800" height="18" rx="9" fill="#F4F4F5" stroke="#000000" stroke-width="1.5"/>
        <rect width="320" height="18" rx="9" fill="#71717A"/>
        <line x1="320" y1="0" x2="320" y2="18" stroke="#000000" stroke-width="2"/>
        <text x="320" y="-6" font-size="9" font-family="monospace" font-weight="700" text-anchor="middle">Level Bar</text>
      </g>
      
      <text x="555" y="218" font-size="13.5" text-anchor="middle">
        Jarak Permukaan ke Sensor: <tspan font-weight="700">[Jarak] cm</tspan> (Tinggi Bak Acuan: 72 cm)
      </text>
      
      <text x="555" y="244" font-size="11" fill="#71717A" font-style="italic" text-anchor="middle">
        Diperbarui dari ESP32: [HH:MM:SS] (Sinkronisasi Firebase Realtime Database)
      </text>
    </g>

    <!-- FOOTER WIREFRAME ANNOTATION -->
    <g transform="translate(0, 510)">
      <rect width="1110" height="120" rx="12" fill="#FAFAFA" stroke="#000000" stroke-width="1" stroke-dasharray="4 4"/>
      <text x="20" y="26" font-size="11.5" font-weight="800">SPESIFIKASI WIREFRAME MENU 1 (DASHBOARD):</text>
      <text x="20" y="48" font-size="10.5" fill="#3F3F46">• 5 Kotak Metrik memiliki tinggi seragam 125px menggunakan CSS Grid auto-fit minmax(185px, 1fr).</text>
      <text x="20" y="68" font-size="10.5" fill="#3F3F46">• Nilai persentase besar di tengah bak memberi kejelasan visual instan (Zero Cognitive Load).</text>
      <text x="20" y="88" font-size="10.5" fill="#3F3F46">• Header menampilkan brand dan status real-time tanpa elemen visual dekoratif yang mengganggu.</text>
    </g>
  </g>'''


def get_menu2_body():
    return '''
  <!-- MAIN CONTENT: MENU 2 GRAFIK DAN HISTORIS -->
  <g id="Main_Content" transform="translate(310, 24)">
    
    <!-- Tombol Back ke Dashboard Utama -->
    <g transform="translate(0, 0)">
      <rect width="240" height="36" rx="18" fill="#FFFFFF" stroke="#000000" stroke-width="1.5"/>
      <text x="120" y="23" font-size="12" font-weight="700" text-anchor="middle">← Kembali ke Dashboard Utama</text>
    </g>

    <text x="0" y="74" font-size="26" font-weight="800">Grafik dan Historis</text>
    <text x="0" y="98" font-size="13" fill="#52525B">Visualisasi tren ketinggian air, fluktuasi kekeruhan (NTU), dan debit aliran air secara berkala.</text>

    <!-- 2 TABEL SIDE BY SIDE -->
    <g transform="translate(0, 125)">
      <!-- Tabel 1: Tren Level Air -->
      <g transform="translate(0, 0)">
        <rect width="540" height="260" rx="16" fill="#FFFFFF" stroke="#000000" stroke-width="1.5"/>
        <text x="24" y="32" font-size="16" font-weight="800">Tren Level Air (%)</text>
        <text x="24" y="50" font-size="11" fill="#71717A">[Data Historis Status Ketinggian Air]</text>
        
        <rect x="24" y="65" width="492" height="30" rx="6" fill="#F4F4F5" stroke="#000000" stroke-width="1"/>
        <text x="36" y="84" font-size="11" font-weight="800">WAKTU</text>
        <text x="260" y="84" font-size="11" font-weight="800">STATUS AIR / LEVEL</text>

        <text x="36" y="116" font-size="11.5">[HH:MM:SS]</text>
        <text x="260" y="116" font-size="11.5" font-weight="700">Normal (Level [X]%)</text>
        <line x1="24" y1="126" x2="516" y2="126" stroke="#E4E4E7"/>

        <text x="36" y="148" font-size="11.5">[HH:MM:SS]</text>
        <text x="260" y="148" font-size="11.5" font-weight="700">Normal (Level [X]%)</text>
        <line x1="24" y1="158" x2="516" y2="158" stroke="#E4E4E7"/>

        <text x="36" y="180" font-size="11.5">[HH:MM:SS]</text>
        <text x="260" y="180" font-size="11.5" font-weight="700">Mengisi (Level [X]%)</text>
        <line x1="24" y1="190" x2="516" y2="190" stroke="#E4E4E7"/>

        <text x="36" y="212" font-size="11.5">[HH:MM:SS]</text>
        <text x="260" y="212" font-size="11.5" font-weight="700">Mengisi (Level [X]%)</text>
      </g>

      <!-- Tabel 2: Riwayat Sensor -->
      <g transform="translate(570, 0)">
        <rect width="540" height="260" rx="16" fill="#FFFFFF" stroke="#000000" stroke-width="1.5"/>
        <text x="24" y="32" font-size="16" font-weight="800">Riwayat Sensor</text>
        <text x="24" y="50" font-size="11" fill="#71717A">[Pencatatan Sinkronisasi Payload RTDB]</text>
        
        <rect x="24" y="65" width="492" height="30" rx="6" fill="#F4F4F5" stroke="#000000" stroke-width="1"/>
        <text x="36" y="84" font-size="11" font-weight="800">WAKTU</text>
        <text x="260" y="84" font-size="11" font-weight="800">AKTIVITAS PENGIRIMAN</text>

        <text x="36" y="116" font-size="11.5">[HH:MM:SS]</text>
        <text x="260" y="116" font-size="11.5">Sync Firebase Payload (HTTP 200)</text>
        <line x1="24" y1="126" x2="516" y2="126" stroke="#E4E4E7"/>

        <text x="36" y="148" font-size="11.5">[HH:MM:SS]</text>
        <text x="260" y="148" font-size="11.5">Ultrasonik: [X]cm, NTU: [X]</text>
        <line x1="24" y1="158" x2="516" y2="158" stroke="#E4E4E7"/>

        <text x="36" y="180" font-size="11.5">[HH:MM:SS]</text>
        <text x="260" y="180" font-size="11.5">Inferensi Mamdani: PWM [X]</text>
        <line x1="24" y1="190" x2="516" y2="190" stroke="#E4E4E7"/>

        <text x="36" y="212" font-size="11.5">[HH:MM:SS]</text>
        <text x="260" y="212" font-size="11.5">Debit Flow Sensor: [X] L/m</text>
      </g>
    </g>

    <!-- BOX KURVA SIMULASI KEKERUHAN -->
    <g transform="translate(0, 410)">
      <rect width="1110" height="290" rx="18" fill="#FFFFFF" stroke="#000000" stroke-width="1.5"/>
      <text x="28" y="36" font-size="18" font-weight="800">Simulasi respon terhadap kekeruhan</text>
      <text x="28" y="56" font-size="11" fill="#71717A">[Kurva Respon Keamanan Inferensi Logika Fuzzy terhadap Kenaikan Turbidity]</text>
      
      <!-- Coordinate Graph -->
      <g transform="translate(50, 80)">
        <line x1="0" y1="150" x2="1000" y2="150" stroke="#000000" stroke-width="1.5"/>
        <line x1="0" y1="0" x2="0" y2="150" stroke="#000000" stroke-width="1.5"/>
        
        <!-- Y-grid lines -->
        <line x1="0" y1="35" x2="1000" y2="35" stroke="#E4E4E7" stroke-dasharray="3 3"/>
        <text x="-10" y="38" font-size="10" text-anchor="end">75%</text>

        <line x1="0" y1="75" x2="1000" y2="75" stroke="#E4E4E7" stroke-dasharray="3 3"/>
        <text x="-10" y="78" font-size="10" text-anchor="end">50%</text>

        <line x1="0" y1="115" x2="1000" y2="115" stroke="#E4E4E7" stroke-dasharray="3 3"/>
        <text x="-10" y="118" font-size="10" text-anchor="end">25%</text>

        <!-- Response Curve in B&W -->
        <path d="M0 10 L150 15 L300 25 L450 50 L600 75 L750 105 L880 150 L1000 150" fill="none" stroke="#000000" stroke-width="3"/>
        <circle cx="0" cy="10" r="4.5" fill="#000000"/>
        <circle cx="300" cy="25" r="4.5" fill="#000000"/>
        <circle cx="600" cy="75" r="4.5" fill="#000000"/>
        <circle cx="750" cy="105" r="4.5" fill="#000000"/>
        <circle cx="880" cy="150" r="4.5" fill="#000000"/>

        <!-- Critical Threshold Line -->
        <line x1="750" y1="0" x2="750" y2="150" stroke="#000000" stroke-width="1.5" stroke-dasharray="4 4"/>
        <text x="760" y="24" font-size="10.5" font-weight="800">[Ambang Batas Kritis: 100 NTU]</text>
        <text x="760" y="40" font-size="9.5" fill="#52525B">Pompa Mati Otomatis (PWM 0)</text>

        <!-- X Labels -->
        <text x="0" y="170" font-size="10" text-anchor="middle">5 NTU</text>
        <text x="300" y="170" font-size="10" text-anchor="middle">25 NTU (Jernih)</text>
        <text x="600" y="170" font-size="10" text-anchor="middle">70 NTU (Waspada)</text>
        <text x="750" y="170" font-size="10" font-weight="700" text-anchor="middle">100 NTU (Kritis)</text>
        <text x="940" y="170" font-size="10" text-anchor="middle">150 NTU (Bahaya)</text>
      </g>
    </g>

    <!-- FOOTER ANNOTATION -->
    <g transform="translate(0, 720)">
      <rect width="1110" height="90" rx="12" fill="#FAFAFA" stroke="#000000" stroke-width="1" stroke-dasharray="4 4"/>
      <text x="20" y="26" font-size="11.5" font-weight="800">SPESIFIKASI WIREFRAME MENU 2 (GRAFIK &amp; HISTORIS):</text>
      <text x="20" y="48" font-size="10.5" fill="#3F3F46">• Menyajikan data auditabilitas sistem secara berkala dengan 2 tabel perbandingan sinkronisasi.</text>
      <text x="20" y="68" font-size="10.5" fill="#3F3F46">• Visualisasi kurva inferensi Mamdani membuktikan logika penurunan daya pompa seiring naiknya kekeruhan air.</text>
    </g>
  </g>'''


def get_menu3_body():
    return '''
  <!-- MAIN CONTENT: MENU 3 RIWAYAT DAN NOTIFIKASI -->
  <g id="Main_Content" transform="translate(310, 24)">
    
    <!-- Tombol Back ke Dashboard Utama -->
    <g transform="translate(0, 0)">
      <rect width="240" height="36" rx="18" fill="#FFFFFF" stroke="#000000" stroke-width="1.5"/>
      <text x="120" y="23" font-size="12" font-weight="700" text-anchor="middle">← Kembali ke Dashboard Utama</text>
    </g>

    <text x="0" y="74" font-size="26" font-weight="800">Riwayat Aktivitas &amp; Log Notifikasi</text>
    <text x="0" y="98" font-size="13" fill="#52525B">Catatan peristiwa otomatis pengisian air, peringatan Telegram, dan status bak mandi.</text>

    <!-- CONTAINER TABEL LOGS -->
    <g transform="translate(0, 125)">
      <rect width="1110" height="660" rx="18" fill="#FFFFFF" stroke="#000000" stroke-width="1.5"/>

      <!-- Filter Dropdown Bar -->
      <g transform="translate(32, 24)">
        <text x="0" y="22" font-size="12" font-weight="700">Filter berdasarkan status:</text>
        <rect x="180" y="0" width="220" height="34" rx="6" fill="#F4F4F5" stroke="#000000" stroke-width="1"/>
        <text x="196" y="22" font-size="12" font-weight="600">[Semua Status ▼]</text>
      </g>

      <!-- Table Header -->
      <g transform="translate(32, 78)">
        <rect width="1046" height="38" rx="6" fill="#F4F4F5" stroke="#000000" stroke-width="1"/>
        <text x="24" y="24" font-size="11" font-weight="800">WAKTU TRANSMISI</text>
        <text x="280" y="24" font-size="11" font-weight="800">RINCIAN AKTIVITAS</text>
        <text x="820" y="24" font-size="11" font-weight="800">STATUS BAK</text>

        <!-- Row 1 -->
        <g transform="translate(0, 38)">
          <text x="24" y="30" font-size="11.5">[HH:MM:SS]</text>
          <text x="280" y="30" font-size="11.5">Penyelarasan Telemetri Sensor ESP32 via Firebase RTDB</text>
          <rect x="820" y="14" width="120" height="24" rx="12" fill="#FFFFFF" stroke="#000000" stroke-width="1.5"/>
          <text x="880" y="30" font-size="10.5" font-weight="700" text-anchor="middle">[ Normal ]</text>
          <line x1="16" y1="50" x2="1030" y2="50" stroke="#E4E4E7"/>
        </g>

        <!-- Row 2 -->
        <g transform="translate(0, 90)">
          <text x="24" y="30" font-size="11.5">[HH:MM:SS]</text>
          <text x="280" y="30" font-size="11.5">Pengisian Pompa Dimulai: Level &le; 20% memicu PWM 255</text>
          <rect x="820" y="14" width="120" height="24" rx="12" fill="#FFFFFF" stroke="#000000" stroke-width="1.5"/>
          <text x="880" y="30" font-size="10.5" font-weight="700" text-anchor="middle">[ Mengisi ]</text>
          <line x1="16" y1="50" x2="1030" y2="50" stroke="#E4E4E7"/>
        </g>

        <!-- Row 3 -->
        <g transform="translate(0, 142)">
          <text x="24" y="30" font-size="11.5">[HH:MM:SS]</text>
          <text x="280" y="30" font-size="11.5">Notifikasi Telegram Terkirim: "Air bak mandi telah mencapai 75%"</text>
          <rect x="820" y="14" width="120" height="24" rx="12" fill="#FFFFFF" stroke="#000000" stroke-width="1.5"/>
          <text x="880" y="30" font-size="10.5" font-weight="700" text-anchor="middle">[ Notifikasi ]</text>
          <line x1="16" y1="50" x2="1030" y2="50" stroke="#E4E4E7"/>
        </g>

        <!-- Row 4 -->
        <g transform="translate(0, 194)">
          <text x="24" y="30" font-size="11.5">[HH:MM:SS]</text>
          <text x="280" y="30" font-size="11.5">Pengujian Sensor Turbidity: Kekeruhan 8.5 NTU (Standar Bersih)</text>
          <rect x="820" y="14" width="120" height="24" rx="12" fill="#FFFFFF" stroke="#000000" stroke-width="1.5"/>
          <text x="880" y="30" font-size="10.5" font-weight="700" text-anchor="middle">[ Jernih ]</text>
          <line x1="16" y1="50" x2="1030" y2="50" stroke="#E4E4E7"/>
        </g>

        <!-- Row 5 -->
        <g transform="translate(0, 246)">
          <text x="24" y="30" font-size="11.5">[HH:MM:SS]</text>
          <text x="280" y="30" font-size="11.5">Proteksi Darurat: Sensor Turbidity &gt; 100 NTU, Pompa Otomatis Mati</text>
          <rect x="820" y="14" width="120" height="24" rx="12" fill="#000000"/>
          <text x="880" y="30" font-size="10.5" font-weight="700" fill="#FFFFFF" text-anchor="middle">[ Bahaya ]</text>
          <line x1="16" y1="50" x2="1030" y2="50" stroke="#E4E4E7"/>
        </g>
      </g>

      <!-- Tombol Segarkan Log di Bawah -->
      <g transform="translate(32, 570)">
        <rect width="210" height="42" rx="21" fill="#FFFFFF" stroke="#000000" stroke-width="1.5"/>
        <text x="105" y="26" font-size="12" font-weight="800" text-anchor="middle">[ 🔄 Segarkan Data Log ]</text>
      </g>
    </g>
  </g>'''


def wrap_svg(content, width=1440, height=900):
    return f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&amp;display=swap');
      text {{ font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; fill: #000000; }}
    </style>
  </defs>
  <rect width="{width}" height="{height}" fill="#FFFFFF"/>
  <rect width="{width}" height="{height}" stroke="#000000" stroke-width="2"/>
{content}
</svg>'''


def main():
    out_dir = r"D:\proyek 3 & proposal ta\web\figma"
    os.makedirs(out_dir, exist_ok=True)

    # 1. Wireframe Menu 1: Dashboard
    m1_content = get_sidebar_bw(0) + get_menu1_body()
    with open(os.path.join(out_dir, "wireframe_1_dashboard.svg"), "w", encoding="utf-8") as f:
        f.write(wrap_svg(m1_content, 1440, 900))

    # 2. Wireframe Menu 2: Grafik dan Historis
    m2_content = get_sidebar_bw(1) + get_menu2_body()
    with open(os.path.join(out_dir, "wireframe_2_telemetri.svg"), "w", encoding="utf-8") as f:
        f.write(wrap_svg(m2_content, 1440, 900))

    # 3. Wireframe Menu 3: Riwayat & Notifikasi
    m3_content = get_sidebar_bw(2) + get_menu3_body()
    with open(os.path.join(out_dir, "wireframe_3_riwayat.svg"), "w", encoding="utf-8") as f:
        f.write(wrap_svg(m3_content, 1440, 900))

    # 4. Giant Board: All 3 Menus Side-by-Side (Width 4560 x Height 1040)
    board = f'''<svg width="4560" height="1060" viewBox="0 0 4560 1060" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&amp;display=swap');
      text {{ font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; fill: #000000; }}
    </style>
  </defs>
  <rect width="4560" height="1060" fill="#F4F4F5"/>

  <!-- BOARD TOP HEADER -->
  <g transform="translate(40, 30)">
    <text x="0" y="28" font-size="28" font-weight="800">KERANGKA UX (LOW-FIDELITY WIREFRAME) — SELURUH MENU SISTEM</text>
    <text x="0" y="50" font-size="14" fill="#52525B">Arsitektur Tata Letak Hitam-Putih Lengkap: Menu 1 (Dashboard Utama), Menu 2 (Grafik &amp; Historis), dan Menu 3 (Riwayat &amp; Notifikasi)</text>
  </g>

  <!-- FRAME 1: DASHBOARD UTAMA -->
  <g id="Frame_1_Dashboard_Wireframe" transform="translate(40, 100)">
    <text x="0" y="-12" font-size="14" font-weight="800">[1] WIREFRAME: DASHBOARD UTAMA</text>
    <rect width="1440" height="900" fill="#FFFFFF" stroke="#000000" stroke-width="2"/>
    {m1_content}
  </g>

  <!-- FRAME 2: GRAFIK & HISTORIS -->
  <g id="Frame_2_Grafik_Wireframe" transform="translate(1540, 100)">
    <text x="0" y="-12" font-size="14" font-weight="800">[2] WIREFRAME: GRAFIK DAN HISTORIS</text>
    <rect width="1440" height="900" fill="#FFFFFF" stroke="#000000" stroke-width="2"/>
    {m2_content}
  </g>

  <!-- FRAME 3: RIWAYAT & NOTIFIKASI -->
  <g id="Frame_3_Riwayat_Wireframe" transform="translate(3040, 100)">
    <text x="0" y="-12" font-size="14" font-weight="800">[3] WIREFRAME: RIWAYAT &amp; NOTIFIKASI</text>
    <rect width="1440" height="900" fill="#FFFFFF" stroke="#000000" stroke-width="2"/>
    {m3_content}
  </g>
</svg>'''

    board_path = os.path.join(out_dir, "wireframe_all_menus_board.svg")
    with open(board_path, "w", encoding="utf-8") as f:
        f.write(board)

    print("Berhasil membuat seluruh wireframe hitam putih di:", out_dir)

if __name__ == "__main__":
    main()
