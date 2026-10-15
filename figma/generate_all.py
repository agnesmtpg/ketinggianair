import os
import sys

def get_sidebar_svg(active_menu=1):
    # active_menu: 1 for Dashboard, 2 for Telemetri, 3 for Riwayat
    opt1_circle = '<circle cx="12" cy="14" r="7" fill="#FFFFFF" stroke="#0D47A1" stroke-width="2"/><circle cx="12" cy="14" r="3.5" fill="#0D47A1"/>' if active_menu == 1 else '<circle cx="12" cy="14" r="7" fill="#FFFFFF" stroke="#90A4AE" stroke-width="1.5"/>'
    opt1_weight = '700' if active_menu == 1 else '500'

    opt2_circle = '<circle cx="12" cy="14" r="7" fill="#FFFFFF" stroke="#0D47A1" stroke-width="2"/><circle cx="12" cy="14" r="3.5" fill="#0D47A1"/>' if active_menu == 2 else '<circle cx="12" cy="14" r="7" fill="#FFFFFF" stroke="#90A4AE" stroke-width="1.5"/>'
    opt2_weight = '700' if active_menu == 2 else '500'

    opt3_circle = '<circle cx="12" cy="14" r="7" fill="#FFFFFF" stroke="#0D47A1" stroke-width="2"/><circle cx="12" cy="14" r="3.5" fill="#0D47A1"/>' if active_menu == 3 else '<circle cx="12" cy="14" r="7" fill="#FFFFFF" stroke="#90A4AE" stroke-width="1.5"/>'
    opt3_weight = '700' if active_menu == 3 else '500'

    return f'''
  <!-- SIDEBAR (STREAMLIT AQUATIC EXACT) -->
  <g id="Streamlit_Sidebar">
    <rect width="280" height="900" fill="#BBDEFB"/>
    <line x1="280" y1="0" x2="280" y2="900" stroke="#90CAF9" stroke-width="1.5"/>

    <!-- Tombol Back / Collapse Sidebar (Menggantikan keyboard_double) -->
    <g id="Sidebar_Back_Btn" transform="translate(20, 18)">
      <rect width="94" height="32" rx="10" fill="#FFFFFF" stroke="#90CAF9" stroke-width="1"/>
      <text x="14" y="21" fill="#0D47A1" font-size="14" font-weight="800">←</text>
      <text x="32" y="21" fill="#0D47A1" font-size="12" font-weight="700">Kembali</text>
    </g>

    <!-- Logo & Header -->
    <g id="Sidebar_Header" transform="translate(20, 68)">
      <text x="120" y="32" font-size="36" text-anchor="middle">💧</text>
      <text x="120" y="66" fill="#000000" font-size="22" font-weight="800" text-anchor="middle">Water Monitoring</text>
    </g>

    <line x1="20" y1="148" x2="260" y2="148" stroke="#90CAF9" stroke-width="1"/>

    <!-- Radio Menu (3 Items) -->
    <g id="Sidebar_Nav" transform="translate(20, 162)">
      <text x="4" y="16" fill="#000000" font-size="13" font-weight="700">Menu</text>
      
      <!-- Option 1: Dashboard Utama -->
      <g id="Nav_Dashboard" transform="translate(0, 30)">
        {opt1_circle}
        <text x="28" y="18" fill="#000000" font-size="13" font-weight="{opt1_weight}">Dashboard Utama</text>
      </g>

      <!-- Option 2: Grafik dan Historis -->
      <g id="Nav_Telemetri" transform="translate(0, 64)">
        {opt2_circle}
        <text x="28" y="18" fill="#000000" font-size="13" font-weight="{opt2_weight}">Grafik dan Historis</text>
      </g>

      <!-- Option 3: Riwayat & Notifikasi -->
      <g id="Nav_Logs" transform="translate(0, 98)">
        {opt3_circle}
        <text x="28" y="18" fill="#000000" font-size="13" font-weight="{opt3_weight}">Riwayat &amp; Notifikasi</text>
      </g>
    </g>

    <line x1="20" y1="295" x2="260" y2="295" stroke="#90CAF9" stroke-width="1"/>

    <!-- ESP32 Status Box (Exact Live State) -->
    <g id="Sidebar_ESP32_Status" transform="translate(20, 310)">
      <rect width="240" height="74" rx="14" fill="#FFFFFF" fill-opacity="0.9" stroke="#E2E8F0"/>
      <rect width="4.5" height="74" rx="2" fill="#2E7D32"/>
      <circle cx="18" cy="22" r="5" fill="#2E7D32"/>
      <text x="28" y="25" fill="#2E7D32" font-size="11.5" font-weight="700">ESP32 TERHUBUNG</text>
      <text x="16" y="44" fill="#000000" font-size="11">Waktu: <tspan font-weight="700">00:00:00</tspan></text>
      <text x="16" y="60" fill="#000000" font-size="10">IP: 10.207.82.29 (WiFi Online)</text>
    </g>

    <!-- Checkbox Auto-Refresh -->
    <g id="Sidebar_Auto_Refresh" transform="translate(20, 400)">
      <rect width="18" height="18" rx="4" fill="#1976D2"/>
      <path d="M4 9L8 13L14 5" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      <text x="26" y="14" fill="#000000" font-size="12" font-weight="700">Auto-Refresh Live Data</text>
    </g>

    <line x1="20" y1="432" x2="260" y2="432" stroke="#90CAF9" stroke-width="1"/>

    <!-- Telegram Bot Section (Exact Live State) -->
    <g id="Sidebar_Telegram" transform="translate(20, 448)">
      <text x="0" y="16" fill="#000000" font-size="13" font-weight="700">📱 Telegram Bot</text>
      
      <!-- Toggle Notifikasi Otomatis -->
      <text x="0" y="44" fill="#000000" font-size="11.5" font-weight="600">Notifikasi otomatis</text>
      <rect x="190" y="32" width="44" height="20" rx="10" fill="#1976D2"/>
      <circle cx="224" cy="42" r="8" fill="#FFFFFF"/>
      
      <!-- Captions -->
      <text x="0" y="74" fill="#37474F" font-size="10.5">Perintah bot: /status /on /off /dashboard /menu</text>
      <text x="0" y="92" fill="#37474F" font-size="10.5">Penerima terdaftar: 1</text>
      
      <!-- Button Tes Telegram -->
      <rect x="0" y="106" width="130" height="34" rx="17" fill="url(#btn-gradient)" filter="url(#btn-shadow)"/>
      <text x="65" y="127" fill="#FFFFFF" font-size="12" font-weight="700" text-anchor="middle">Tes Telegram</text>
    </g>
  </g>'''

def get_dashboard_svg():
    sidebar = get_sidebar_svg(active_menu=1)
    return f'''<svg width="1440" height="900" viewBox="0 0 1440 900" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&amp;display=swap');
      text {{ font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; fill: #000000; }}
      .metric-title {{ font-size: 11.5px; font-weight: 700; fill: #455A64; letter-spacing: 0.5px; text-transform: uppercase; }}
      .metric-val {{ font-size: 24px; font-weight: 800; }}
      .metric-sub {{ font-size: 11.5px; fill: #37474F; }}
    </style>
    <filter id="card-shadow" x="0" y="0" width="100%" height="100%" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
      <feDropShadow dx="0" dy="4" stdDeviation="12" flood-color="#0D47A1" flood-opacity="0.08"/>
    </filter>
    <filter id="btn-shadow" x="0" y="0" width="100%" height="100%" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
      <feDropShadow dx="0" dy="3" stdDeviation="6" flood-color="#1976D2" flood-opacity="0.3"/>
    </filter>
    <linearGradient id="btn-gradient" x1="0" y1="0" x2="1" y2="1">
      <stop stop-color="#42A5F5"/>
      <stop offset="1" stop-color="#1976D2"/>
    </linearGradient>
    <linearGradient id="bar-grad" x1="0" y1="0" x2="1" y2="0">
      <stop stop-color="#42A5F5"/>
      <stop offset="1" stop-color="#1976D2"/>
    </linearGradient>
  </defs>

  <!-- Background (Exact Streamlit Aquatic Blue #D1E3F8) -->
  <rect width="1440" height="900" fill="#D1E3F8"/>

  {sidebar}

  <!-- ==================== MAIN CONTENT AREA ==================== -->
  <g id="Main_Content" transform="translate(310, 32)">
    
    <!-- Header Title (Exact web) -->
    <text x="0" y="28" fill="#000000" font-size="28" font-weight="800">Dashboard Monitoring Air</text>

    <!-- ==================== BARIS 1: 5 METRIC CARDS (RESPONSIVE GRID WITH UNIFORM HEIGHT) ==================== -->
    <g id="Metric_Grid" transform="translate(0, 56)">
      
      <!-- CARD 1: STATUS PWM -->
      <g id="Card_PWM" transform="translate(0, 0)">
        <rect width="210" height="125" rx="20" fill="#FFFFFF" fill-opacity="0.95" filter="url(#card-shadow)" stroke="#FFFFFF" stroke-width="1"/>
        <text x="18" y="28" class="metric-title">STATUS PWM</text>
        <text x="18" y="68" class="metric-val" fill="#2E7D32">PWM 255</text>
        <text x="18" y="104" class="metric-sub">Duty: <b>100%</b> (12.0V DC)</text>
      </g>

      <!-- CARD 2: STATUS KECEPATAN -->
      <g id="Card_Speed" transform="translate(225, 0)">
        <rect width="210" height="125" rx="20" fill="#FFFFFF" fill-opacity="0.95" filter="url(#card-shadow)" stroke="#FFFFFF" stroke-width="1"/>
        <text x="18" y="28" class="metric-title">STATUS KECEPATAN</text>
        <text x="18" y="68" class="metric-val" fill="#2E7D32">CEPAT (100%)</text>
        <text x="18" y="104" class="metric-sub">Mode: <b>Otonom Cerdas</b> (ESP32)</text>
      </g>

      <!-- CARD 3: KUALITAS AIR -->
      <g id="Card_Turbidity" transform="translate(450, 0)">
        <rect width="210" height="125" rx="20" fill="#FFFFFF" fill-opacity="0.95" filter="url(#card-shadow)" stroke="#FFFFFF" stroke-width="1"/>
        <text x="18" y="28" class="metric-title">KUALITAS AIR</text>
        <text x="18" y="68" class="metric-val" fill="#2E7D32">8.5 <tspan font-size="14" font-weight="600">NTU</tspan></text>
        <text x="18" y="104" class="metric-sub">Status: <b>JERNIH</b></text>
      </g>

      <!-- CARD 4: DEBIT AIR MASUK -->
      <g id="Card_Flow" transform="translate(675, 0)">
        <rect width="210" height="125" rx="20" fill="#FFFFFF" fill-opacity="0.95" filter="url(#card-shadow)" stroke="#FFFFFF" stroke-width="1"/>
        <text x="18" y="28" class="metric-title">DEBIT AIR MASUK</text>
        <text x="18" y="68" class="metric-val" fill="#000000">0.0 <tspan font-size="14" font-weight="600">L/min</tspan></text>
        <text x="18" y="104" class="metric-sub">Sensor YF-S201</text>
      </g>

      <!-- CARD 5: TOTAL AIR TERPAKAI -->
      <g id="Card_TotalVolume" transform="translate(900, 0)">
        <rect width="210" height="125" rx="20" fill="#FFFFFF" fill-opacity="0.95" filter="url(#card-shadow)" stroke="#FFFFFF" stroke-width="1"/>
        <text x="18" y="28" class="metric-title">TOTAL AIR TERPAKAI</text>
        <text x="18" y="68" class="metric-val" fill="#000000">0.0 <tspan font-size="14" font-weight="600">Liter</tspan></text>
        <text x="18" y="104" class="metric-sub">Akumulasi Pengisian</text>
      </g>
    </g>

    <!-- ==================== BARIS 2: LEVEL BAK MANDI ==================== -->
    <g id="Row_2_Tank" transform="translate(0, 205)">
      <rect width="1110" height="280" rx="22" fill="#FFFFFF" filter="url(#card-shadow)"/>
      
      <text x="555" y="44" fill="#000000" font-size="20" font-weight="800" text-anchor="middle">Ketinggian Bak Mandi</text>
      
      <!-- Big Percentage Display (Exact 0% state) -->
      <text x="555" y="126" fill="#000000" font-size="64" font-weight="800" text-anchor="middle">0%</text>
      
      <!-- Progress Bar Track -->
      <g id="Progress_Bar" transform="translate(155, 155)">
        <rect width="800" height="16" rx="8" fill="#E1F5FE"/>
        <!-- 0% bar has minimal pulse indicator or empty track -->
        <rect width="8" height="16" rx="8" fill="url(#bar-grad)"/>
      </g>
      
      <!-- Details & Sensor Info (Exact matching app.py) -->
      <text x="555" y="210" fill="#000000" font-size="14" text-anchor="middle">
        Jarak Permukaan ke Sensor: <tspan font-weight="700">0.0 cm</tspan> (Tinggi Bak Acuan: 72 cm)
      </text>
      
      <text x="555" y="238" fill="#546E7A" font-size="11" font-style="italic" text-anchor="middle">
        Diperbarui dari ESP32: 00:00:00
      </text>
    </g>
  </g>
</svg>'''

def get_telemetri_svg():
    sidebar = get_sidebar_svg(active_menu=2)
    return f'''<svg width="1440" height="900" viewBox="0 0 1440 900" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&amp;display=swap');
      text {{ font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; fill: #000000; }}
      .th {{ font-size: 12px; font-weight: 700; fill: #455A64; }}
      .td {{ font-size: 12px; fill: #37474F; }}
    </style>
    <filter id="card-shadow" x="0" y="0" width="100%" height="100%" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
      <feDropShadow dx="0" dy="4" stdDeviation="12" flood-color="#0D47A1" flood-opacity="0.08"/>
    </filter>
    <filter id="btn-shadow" x="0" y="0" width="100%" height="100%" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
      <feDropShadow dx="0" dy="3" stdDeviation="6" flood-color="#1976D2" flood-opacity="0.3"/>
    </filter>
    <linearGradient id="btn-gradient" x1="0" y1="0" x2="1" y2="1">
      <stop stop-color="#42A5F5"/>
      <stop offset="1" stop-color="#1976D2"/>
    </linearGradient>
  </defs>

  <rect width="1440" height="900" fill="#D1E3F8"/>

  {sidebar}

  <!-- MAIN TELEMETRI -->
  <g id="Main_Content" transform="translate(310, 24)">
    
    <!-- Button Back ke Dashboard Utama -->
    <g id="Btn_Back" transform="translate(0, 0)">
      <rect width="230" height="36" rx="18" fill="url(#btn-gradient)" filter="url(#btn-shadow)"/>
      <text x="115" y="23" fill="#FFFFFF" font-size="12" font-weight="700" text-anchor="middle">← Kembali ke Dashboard Utama</text>
    </g>

    <text x="0" y="74" fill="#000000" font-size="28" font-weight="800">Grafik dan Historis</text>
    <text x="0" y="98" fill="#000000" font-size="14">Visualisasi tren ketinggian air, fluktuasi kekeruhan (NTU), dan debit aliran air secara berkala.</text>

    <!-- 2 Tables Side-by-Side -->
    <g transform="translate(0, 125)">
      <!-- Left Table Card: Tren Level Air -->
      <g transform="translate(0, 0)">
        <rect width="540" height="260" rx="20" fill="#FFFFFF" fill-opacity="0.95" filter="url(#card-shadow)"/>
        <text x="24" y="32" fill="#000000" font-size="16" font-weight="700">Tren Level Air (%)</text>
        <text x="24" y="50" fill="#546E7A" font-size="11">Data pemantauan status ketinggian air terbaru.</text>
        
        <rect x="24" y="65" width="492" height="30" rx="6" fill="#F1F5F9"/>
        <text x="36" y="84" class="th">WAKTU</text>
        <text x="260" y="84" class="th">STATUS AIR / LEVEL</text>

        <text x="36" y="116" class="td">00:00:00</text>
        <text x="260" y="116" class="td" font-weight="600" fill="#2E7D32">Normal (Level 75%)</text>
        <line x1="24" y1="126" x2="516" y2="126" stroke="#E2E8F0"/>

        <text x="36" y="148" class="td">00:00:03</text>
        <text x="260" y="148" class="td" font-weight="600" fill="#2E7D32">Normal (Level 74%)</text>
        <line x1="24" y1="158" x2="516" y2="158" stroke="#E2E8F0"/>

        <text x="36" y="180" class="td">00:00:06</text>
        <text x="260" y="180" class="td" font-weight="600" fill="#2E7D32">Normal (Level 73%)</text>
        <line x1="24" y1="190" x2="516" y2="190" stroke="#E2E8F0"/>

        <text x="36" y="212" class="td">00:00:09</text>
        <text x="260" y="212" class="td" font-weight="600" fill="#0288D1">Mengisi (Level 71%)</text>
      </g>

      <!-- Right Table Card: Riwayat Sensor -->
      <g transform="translate(570, 0)">
        <rect width="540" height="260" rx="20" fill="#FFFFFF" fill-opacity="0.95" filter="url(#card-shadow)"/>
        <text x="24" y="32" fill="#000000" font-size="16" font-weight="700">Riwayat Sensor</text>
        <text x="24" y="50" fill="#546E7A" font-size="11">Pencatatan sinkronisasi data telemetri ke Firebase Database.</text>
        
        <rect x="24" y="65" width="492" height="30" rx="6" fill="#F1F5F9"/>
        <text x="36" y="84" class="th">WAKTU</text>
        <text x="260" y="84" class="th">AKTIVITAS PENGIRIMAN</text>

        <text x="36" y="116" class="td">00:00:00</text>
        <text x="260" y="116" class="td">Sync Firebase RTDB Success</text>
        <line x1="24" y1="126" x2="516" y2="126" stroke="#E2E8F0"/>

        <text x="36" y="148" class="td">00:00:03</text>
        <text x="260" y="148" class="td">Ultrasonik: 18.0cm, NTU: 8.5</text>
        <line x1="24" y1="158" x2="516" y2="158" stroke="#E2E8F0"/>

        <text x="36" y="180" class="td">00:00:06</text>
        <text x="260" y="180" class="td">Inferensi Fuzzy: PWM 175</text>
        <line x1="24" y1="190" x2="516" y2="190" stroke="#E2E8F0"/>

        <text x="36" y="212" class="td">00:00:09</text>
        <text x="260" y="212" class="td">Telemetri Flow Sensor: 4.2 L/m</text>
      </g>
    </g>

    <!-- Bottom Simulation Card -->
    <g transform="translate(0, 410)">
      <rect width="1110" height="300" rx="22" fill="#FFFFFF" fill-opacity="0.95" filter="url(#card-shadow)"/>
      <text x="28" y="36" fill="#000000" font-size="18" font-weight="700">Simulasi respon terhadap kekeruhan</text>
      <text x="28" y="58" fill="#546E7A" font-size="12">Kurva respon keamanan logika fuzzy terhadap kenaikan nilai turbiditas air.</text>
      
      <!-- Graph Canvas -->
      <g transform="translate(40, 80)">
        <line x1="0" y1="160" x2="1020" y2="160" stroke="#CBD5E1" stroke-width="1.5"/>
        <line x1="0" y1="0" x2="0" y2="160" stroke="#CBD5E1" stroke-width="1.5"/>
        
        <!-- Grid horizontal lines -->
        <line x1="0" y1="40" x2="1020" y2="40" stroke="#F1F5F9" stroke-width="1" stroke-dasharray="4"/>
        <line x1="0" y1="80" x2="1020" y2="80" stroke="#F1F5F9" stroke-width="1" stroke-dasharray="4"/>
        <line x1="0" y1="120" x2="1020" y2="120" stroke="#F1F5F9" stroke-width="1" stroke-dasharray="4"/>

        <!-- Line plot -->
        <path d="M0 0 L150 10 L300 20 L450 45 L600 70 L750 95 L900 160 L1020 160" fill="none" stroke="#0D47A1" stroke-width="3.5" stroke-linecap="round"/>
        <circle cx="0" cy="0" r="5" fill="#0D47A1"/>
        <circle cx="150" cy="10" r="5" fill="#0D47A1"/>
        <circle cx="300" cy="20" r="5" fill="#0D47A1"/>
        <circle cx="450" cy="45" r="5" fill="#0D47A1"/>
        <circle cx="600" cy="70" r="5" fill="#F57F17"/>
        <circle cx="750" cy="95" r="5" fill="#F57F17"/>
        <circle cx="900" cy="160" r="5" fill="#C62828"/>
        <circle cx="1020" cy="160" r="5" fill="#C62828"/>

        <!-- Labels -->
        <text x="0" y="180" fill="#64748B" font-size="11">5 NTU</text>
        <text x="300" y="180" fill="#64748B" font-size="11">25 NTU (Jernih)</text>
        <text x="600" y="180" fill="#64748B" font-size="11">70 NTU (Waspada)</text>
        <text x="890" y="180" fill="#C62828" font-size="11" font-weight="700">110 NTU (Stop Pompa)</text>
      </g>
    </g>
  </g>
</svg>'''

def get_riwayat_svg():
    sidebar = get_sidebar_svg(active_menu=3)
    return f'''<svg width="1440" height="900" viewBox="0 0 1440 900" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&amp;display=swap');
      text {{ font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; fill: #000000; }}
      .th {{ font-size: 12px; font-weight: 700; fill: #455A64; }}
      .td {{ font-size: 12.5px; fill: #37474F; }}
    </style>
    <filter id="card-shadow" x="0" y="0" width="100%" height="100%" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
      <feDropShadow dx="0" dy="4" stdDeviation="12" flood-color="#0D47A1" flood-opacity="0.08"/>
    </filter>
    <filter id="btn-shadow" x="0" y="0" width="100%" height="100%" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
      <feDropShadow dx="0" dy="3" stdDeviation="6" flood-color="#1976D2" flood-opacity="0.3"/>
    </filter>
    <linearGradient id="btn-gradient" x1="0" y1="0" x2="1" y2="1">
      <stop stop-color="#42A5F5"/>
      <stop offset="1" stop-color="#1976D2"/>
    </linearGradient>
  </defs>

  <rect width="1440" height="900" fill="#D1E3F8"/>

  {sidebar}

  <!-- MAIN LOGS -->
  <g id="Main_Content" transform="translate(310, 24)">
    
    <!-- Button Back ke Dashboard Utama -->
    <g id="Btn_Back" transform="translate(0, 0)">
      <rect width="230" height="36" rx="18" fill="url(#btn-gradient)" filter="url(#btn-shadow)"/>
      <text x="115" y="23" fill="#FFFFFF" font-size="12" font-weight="700" text-anchor="middle">← Kembali ke Dashboard Utama</text>
    </g>

    <text x="0" y="74" fill="#000000" font-size="28" font-weight="800">Riwayat Aktivitas &amp; Log Notifikasi</text>
    <text x="0" y="98" fill="#000000" font-size="14">Catatan peristiwa otomatis pengisian air, peringatan Telegram, dan status bak mandi.</text>

    <!-- Table Card Container -->
    <g transform="translate(0, 125)">
      <rect width="1110" height="660" rx="22" fill="#FFFFFF" fill-opacity="0.95" filter="url(#card-shadow)"/>

      <!-- Filter Dropdown Bar -->
      <g transform="translate(32, 28)">
        <text x="0" y="22" fill="#37474F" font-size="13" font-weight="600">Filter berdasarkan status:</text>
        <rect x="180" y="0" width="220" height="36" rx="10" fill="#F8FAFC" stroke="#CBD5E1"/>
        <text x="196" y="23" fill="#1E293B" font-size="13" font-weight="600">Semua</text>
        <path d="M375 16L382 23L389 16" stroke="#64748B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </g>

      <!-- Table Structure -->
      <g transform="translate(32, 85)">
        <rect width="1046" height="40" rx="8" fill="#F1F5F9"/>
        <text x="24" y="25" class="th">WAKTU TRANSMISI</text>
        <text x="280" y="25" class="th">RINCIAN AKTIVITAS</text>
        <text x="820" y="25" class="th">STATUS BAK</text>

        <!-- Row 1 -->
        <g transform="translate(0, 40)">
          <text x="24" y="32" class="td">00:00:00</text>
          <text x="280" y="32" class="td">Pengisian otomatis selesai target penuh</text>
          <rect x="820" y="14" width="130" height="26" rx="13" fill="#E8F5E9"/>
          <text x="885" y="31" fill="#2E7D32" font-size="11.5" font-weight="700" text-anchor="middle">Air Penuh (90%)</text>
          <line x1="16" y1="52" x2="1030" y2="52" stroke="#F1F5F9"/>
        </g>

        <!-- Row 2 -->
        <g transform="translate(0, 92)">
          <text x="24" y="32" class="td">00:00:03</text>
          <text x="280" y="32" class="td">Notifikasi Telegram terkirim ke 1 subscriber</text>
          <rect x="820" y="14" width="130" height="26" rx="13" fill="#E3F2FD"/>
          <text x="885" y="31" fill="#1565C0" font-size="11.5" font-weight="700" text-anchor="middle">Telegram Sent</text>
          <line x1="16" y1="52" x2="1030" y2="52" stroke="#F1F5F9"/>
        </g>

        <!-- Row 3 -->
        <g transform="translate(0, 144)">
          <text x="24" y="32" class="td">00:00:06</text>
          <text x="280" y="32" class="td">Kekeruhan air normal 8.5 NTU (Air Jernih)</text>
          <rect x="820" y="14" width="130" height="26" rx="13" fill="#E8F5E9"/>
          <text x="885" y="31" fill="#2E7D32" font-size="11.5" font-weight="700" text-anchor="middle">Normal</text>
          <line x1="16" y1="52" x2="1030" y2="52" stroke="#F1F5F9"/>
        </g>

        <!-- Row 4 -->
        <g transform="translate(0, 196)">
          <text x="24" y="32" class="td">00:00:09</text>
          <text x="280" y="32" class="td">Pompa diaktifkan modulasi PWM 175</text>
          <rect x="820" y="14" width="130" height="26" rx="13" fill="#E1F5FE"/>
          <text x="885" y="31" fill="#0288D1" font-size="11.5" font-weight="700" text-anchor="middle">Sedang Mengisi</text>
          <line x1="16" y1="52" x2="1030" y2="52" stroke="#F1F5F9"/>
        </g>
      </g>

      <!-- Refresh Button at Bottom -->
      <g transform="translate(32, 580)">
        <rect width="210" height="42" rx="21" fill="url(#btn-gradient)" filter="url(#btn-shadow)"/>
        <text x="105" y="26" fill="#FFFFFF" font-size="13" font-weight="700" text-anchor="middle">🔄 Segarkan Data Log</text>
      </g>
    </g>
  </g>
</svg>'''

def get_mobile_svg():
    return '''<svg width="390" height="844" viewBox="0 0 390 844" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&amp;display=swap');
      text { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; fill: #000000; }
    </style>
    <filter id="m-shadow" x="0" y="0" width="100%" height="100%" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
      <feDropShadow dx="0" dy="4" stdDeviation="8" flood-color="#0D47A1" flood-opacity="0.1"/>
    </filter>
    <linearGradient id="m-bar-grad" x1="0" y1="0" x2="1" y2="0">
      <stop stop-color="#42A5F5"/>
      <stop offset="1" stop-color="#1976D2"/>
    </linearGradient>
  </defs>

  <!-- Mobile Canvas Background -->
  <rect width="390" height="844" fill="#D1E3F8"/>

  <!-- SIDEBAR TERBUKA PERSIS SEPERTI SCREENSHOT USER -->
  <g id="Mobile_Sidebar" transform="translate(0, 0)">
    <rect width="300" height="844" fill="#BBDEFB" filter="url(#m-shadow)"/>
    <line x1="300" y1="0" x2="300" y2="844" stroke="#90CAF9" stroke-width="1.5"/>

    <!-- Tombol Back '← Kembali' (Menggantikan teks keyboard_double) -->
    <g id="Mobile_Back_Btn" transform="translate(18, 16)">
      <rect width="90" height="32" rx="10" fill="#FFFFFF" stroke="#90CAF9"/>
      <text x="12" y="21" fill="#0D47A1" font-size="14" font-weight="800">←</text>
      <text x="30" y="21" fill="#0D47A1" font-size="12" font-weight="700">Kembali</text>
    </g>

    <!-- Logo & Title -->
    <g transform="translate(20, 60)">
      <text x="120" y="32" font-size="34" text-anchor="middle">💧</text>
      <text x="120" y="64" fill="#000000" font-size="20" font-weight="800" text-anchor="middle">Water Monitoring</text>
    </g>

    <line x1="20" y1="138" x2="280" y2="138" stroke="#90CAF9" stroke-width="1"/>

    <!-- Radio Menu (3 Items) -->
    <g transform="translate(20, 150)">
      <text x="4" y="16" fill="#000000" font-size="13" font-weight="700">Menu</text>
      
      <!-- Option 1: Selected -->
      <g transform="translate(0, 28)">
        <circle cx="12" cy="14" r="7" fill="#FFFFFF" stroke="#0D47A1" stroke-width="2"/>
        <circle cx="12" cy="14" r="3.5" fill="#0D47A1"/>
        <text x="28" y="18" fill="#000000" font-size="13" font-weight="700">Dashboard Utama</text>
      </g>
      <!-- Option 2 -->
      <g transform="translate(0, 60)">
        <circle cx="12" cy="14" r="7" fill="#FFFFFF" stroke="#90A4AE" stroke-width="1.5"/>
        <text x="28" y="18" fill="#000000" font-size="13" font-weight="500">Grafik dan Historis</text>
      </g>
      <!-- Option 3 -->
      <g transform="translate(0, 92)">
        <circle cx="12" cy="14" r="7" fill="#FFFFFF" stroke="#90A4AE" stroke-width="1.5"/>
        <text x="28" y="18" fill="#000000" font-size="13" font-weight="500">Riwayat &amp; Notifikasi</text>
      </g>
    </g>

    <line x1="20" y1="274" x2="280" y2="274" stroke="#90CAF9" stroke-width="1"/>

    <!-- ESP32 Status Box (Exact Screenshot) -->
    <g transform="translate(20, 288)">
      <rect width="250" height="74" rx="14" fill="#FFFFFF" stroke="#E2E8F0"/>
      <rect width="4.5" height="74" rx="2" fill="#2E7D32"/>
      <circle cx="18" cy="22" r="5" fill="#2E7D32"/>
      <text x="28" y="25" fill="#2E7D32" font-size="11.5" font-weight="700">ESP32 TERHUBUNG</text>
      <text x="16" y="44" fill="#000000" font-size="11">Waktu: <tspan font-weight="700">00:00:00</tspan></text>
      <text x="16" y="60" fill="#000000" font-size="10">IP: 10.207.82.29</text>
    </g>

    <!-- Checkbox Auto-Refresh -->
    <g transform="translate(20, 380)">
      <rect width="18" height="18" rx="4" fill="#1976D2"/>
      <path d="M4 9L8 13L14 5" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      <text x="26" y="14" fill="#000000" font-size="12" font-weight="700">Auto-Refresh Live Data</text>
    </g>

    <line x1="20" y1="412" x2="280" y2="412" stroke="#90CAF9" stroke-width="1"/>

    <!-- Telegram Bot Section (Exact Screenshot) -->
    <g transform="translate(20, 426)">
      <text x="0" y="16" fill="#000000" font-size="13" font-weight="700">📱 Telegram Bot</text>
      
      <text x="0" y="44" fill="#000000" font-size="11.5" font-weight="600">Notifikasi otomatis</text>
      <rect x="196" y="32" width="44" height="20" rx="10" fill="#1976D2"/>
      <circle cx="230" cy="42" r="8" fill="#FFFFFF"/>
      
      <text x="0" y="74" fill="#37474F" font-size="10.5">Perintah bot: /status /on /off</text>
      <text x="0" y="88" fill="#37474F" font-size="10.5">/dashboard /menu</text>
      <text x="0" y="112" fill="#37474F" font-size="10.5">Penerima terdaftar: 1</text>

      <rect x="0" y="124" width="130" height="34" rx="17" fill="#1976D2"/>
      <text x="65" y="145" fill="#FFFFFF" font-size="12" font-weight="700" text-anchor="middle">Tes Telegram</text>
    </g>
  </g>

  <!-- Mobile Dashboard Behind (Visible Peek like screenshot) -->
  <g transform="translate(315, 60)" opacity="0.85">
    <rect width="65" height="110" rx="16" fill="#FFFFFF"/>
    <text x="8" y="24" fill="#64748B" font-size="8" font-weight="700">KECEPATAN</text>
    <text x="8" y="48" fill="#2E7D32" font-size="12" font-weight="800">CEPAT</text>
    <text x="8" y="80" fill="#64748B" font-size="8">Otonom Cerdas</text>
    
    <rect y="125" width="65" height="110" rx="16" fill="#FFFFFF"/>
    <text x="8" y="148" fill="#64748B" font-size="8" font-weight="700">MASUK</text>
    <text x="8" y="172" fill="#000000" font-size="12" font-weight="800">0.0</text>
  </g>
</svg>'''

def generate_all(out_dir=None):
    if out_dir is None:
        out_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(out_dir, exist_ok=True)

    # 1. Frame 1: Dashboard Utama
    dash_svg = get_dashboard_svg()
    for name in ["frame_1_dashboard.svg", "exact_web_dashboard.svg", "figma_ui_design_dashboard.svg"]:
        with open(os.path.join(out_dir, name), "w", encoding="utf-8") as f:
            f.write(dash_svg)

    # 2. Frame 2: Grafik dan Historis
    tel_svg = get_telemetri_svg()
    for name in ["frame_2_telemetri.svg", "exact_web_telemetri.svg"]:
        with open(os.path.join(out_dir, name), "w", encoding="utf-8") as f:
            f.write(tel_svg)

    # 3. Frame 3: Riwayat & Notifikasi
    riw_svg = get_riwayat_svg()
    for name in ["frame_3_riwayat.svg", "exact_web_riwayat.svg"]:
        with open(os.path.join(out_dir, name), "w", encoding="utf-8") as f:
            f.write(riw_svg)

    # 4. Frame 4: Mobile Responsive View
    mob_svg = get_mobile_svg()
    for name in ["frame_4_mobile.svg", "figma_ui_design_mobile.svg"]:
        with open(os.path.join(out_dir, name), "w", encoding="utf-8") as f:
            f.write(mob_svg)

    # Hapus file lama Settings / Frame 4-5 yang sudah tidak relevan
    for old_file in ["frame_3_settings.svg", "exact_web_settings.svg", "figma_ui_design_settings.svg", "frame_5_mobile.svg"]:
        p = os.path.join(out_dir, old_file)
        if os.path.exists(p):
            try:
                os.remove(p)
            except Exception:
                pass

    msg = f"Berhasil membuat seluruh Frame Desain SVG (Frame 1-4) yang sama persis dengan web di: {out_dir}"
    print(msg)
    return msg

if __name__ == "__main__":
    generate_all()
