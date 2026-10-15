import os
import sys
import json
import threading
import time
from datetime import datetime

import requests
import pandas as pd
import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

# ============================================================
# KONFIGURASI
# ============================================================
def _secret(nama, default=""):
    try:
        return st.secrets[nama]
    except Exception:
        return os.environ.get(nama, default)

FIREBASE_URL = "https://ketinggian-dd1fb-default-rtdb.firebaseio.com"
KEY_PATH = r"D:\proyek 3 & proposal ta\web\serviceAccountKey.json"
TELEGRAM_TOKEN = _secret("T8953132207:AAE4iCqGj9weJ80VXJWjb4WLaSEzb2aNI78")
TELEGRAM_CHAT_ID = _secret("1156974464", "")
DASHBOARD_URL = "http://localhost:8501"
SUBS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "telegram_subscribers.json")
TG_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

# Menu perintah bot (tampil di tombol "Menu" Telegram)
TG_COMMANDS = [
    {"command": "status", "description": "Lihat kondisi air & pompa saat ini"},
    {"command": "on", "description": "Hidupkan pompa manual"},
    {"command": "off", "description": "Matikan pompa manual"},
    {"command": "dashboard", "description": "Link dashboard"},
    {"command": "menu", "description": "Tampilkan menu"},
]

DEFAULT_CONFIG = {
    "tinggi_bak": 72,
    "batas_atas": 90,
    "batas_bawah": 20,
    "ambang_keruh": 100,
    "mode": "Otomatis (Fuzzy Mamdani)"
}


@st.cache_resource
def init_firebase():
    if not firebase_admin._apps:
        if os.path.exists(KEY_PATH):
            cred = credentials.Certificate(KEY_PATH)
        else:
            cred = credentials.Certificate(json.loads(st.secrets["FIREBASE_KEY"]))
        firebase_admin.initialize_app(cred, {"databaseURL": FIREBASE_URL})
    return True


init_firebase()


# ============================================================
# FUNGSI FIREBASE
# ============================================================
def baca_sensor():
    try:
        data = db.reference("sensor").get()
        return data if data else None
    except Exception:
        return None


def baca_config():
    try:
        data = db.reference("config").get()
        if data:
            return data
    except Exception:
        pass
    return DEFAULT_CONFIG


def baca_logs():
    try:
        data = db.reference("logs").get()
        if data:
            rows = []
            for k, v in data.items():
                if isinstance(v, dict):
                    v_copy = dict(v)
                    v_copy["id"] = k
                    rows.append(v_copy)
            return sorted(rows, key=lambda x: str(x.get("waktu", "")), reverse=True)
    except Exception:
        pass
    return []


def set_command(key: str, value):
    try:
        db.reference(f"command/{key}").set(value)
        return True
    except Exception:
        return False


def simpan_config_firebase(data: dict):
    try:
        db.reference("config").set(data)
        return True
    except Exception:
        return False


# ============================================================
# LOGIKA FUZZY LOGIC MAMDANI
# ============================================================
def evaluasi_fuzzy_mamdani(level_percent, ntu):
    """
    Kendali adaptif pompa 12V via driver MOSFET D4184 PWM (0-255):
    Masukan 1 : Level Air (%) [Kosong, Sedang, Penuh]
    Masukan 2 : Kekeruhan (NTU) [Jernih, Agak Keruh, Keruh]
    Keluaran  : PWM (0 - 255), status kecepatan motor, proteksi kualitas air
    """
    if ntu <= 25:
        mutu_air = "JERNIH"
        warna_mutu = "#2e7d32"
    elif ntu <= 100:
        mutu_air = "AGAK KERUH"
        warna_mutu = "#f57f17"
    else:
        mutu_air = "KERUH (BAHAYA)"
        warna_mutu = "#c62828"

    if ntu > 100:
        keputusan = "PROTEKSI DARURAT (AIR KERUH)"
        pwm_val = 0
        kecepatan_label = "MATI (STOP)"
        tegangan_volt = 0.0
        keterangan = "Sensor turbidity mendeteksi air keruh (> 100 NTU). Pengisian dimatikan otomatis via MOSFET PWM 0 untuk mencegah masuknya air kotor ke bak mandi."
        badge_color = "#c62828"
    elif level_percent >= 90:
        keputusan = "TARGET PENUH TERCAPAI"
        pwm_val = 0
        kecepatan_label = "MATI (0%)"
        tegangan_volt = 0.0
        keterangan = "Air telah mencapai ambang batas target aman (level >= 90% / jarak <= 10 cm). Daya motor diputus total (PWM 0) secara presisi tanpa luapan air."
        badge_color = "#1565c0"
    elif level_percent <= 20:
        keputusan = "PENGISIAN CEPAT (KOSONG)"
        pwm_val = 255
        kecepatan_label = "CEPAT (100%)"
        tegangan_volt = 12.0
        keterangan = "Air berada di bawah ambang minimum (level <= 20% / jarak >= 48 cm). Driver MOSFET memacu pompa pada daya maksimal (PWM 255 / 12V) agar pengisian efisien."
        badge_color = "#2e7d32"
    elif level_percent <= 60:
        keputusan = "PENGISIAN STABIL (SEDANG)"
        pwm_val = 175
        kecepatan_label = "SEDANG (~68%)"
        tegangan_volt = 8.2
        keterangan = "Level air berada di zona sedang (21% - 60%). Mesin inferensi Mamdani memberikan sinyal PWM 175 untuk menjaga debit pengisian stabil."
        badge_color = "#0288d1"
    else:
        keputusan = "DESELERASI HALUS (MENDEKATI PENUH)"
        pwm_val = 95
        kecepatan_label = "PELAN (~37%)"
        tegangan_volt = 4.5
        keterangan = "Level air mendekati ambang batas target (61% - 89%). Pompa melambat secara halus (PWM 95 / ~4.5V) guna meredam riak air dan mencegah luapan (overshoot)."
        badge_color = "#f57f17"

    duty_percent = int((pwm_val / 255.0) * 100)

    return {
        "mutu_air": mutu_air,
        "warna_mutu": warna_mutu,
        "keputusan": keputusan,
        "badge_color": badge_color,
        "pwm": pwm_val,
        "duty": duty_percent,
        "kecepatan_label": kecepatan_label,
        "tegangan_volt": tegangan_volt,
        "pompa_aktif": (pwm_val > 0),
        "keterangan": keterangan
    }


def hitung_level(sensor, tinggi_bak):
    """Persentase level air dari data sensor."""
    if not sensor:
        return 0
    jarak = float(sensor.get("jarak", 0.0))
    if jarak > 0:
        return max(0, min(100, int((tinggi_bak - jarak) / tinggi_bak * 100)))
    return int(sensor.get("level", 0))


def ambil_ntu(sensor):
    if not sensor:
        return 8.5
    return float(sensor.get("turbidity", sensor.get("kekeruhan", sensor.get("ntu", 8.5))))


# ============================================================
# TELEGRAM: SUBSCRIBER, KIRIM PESAN, BOT PERINTAH
# ============================================================
_subs_lock = threading.Lock()


def baca_subscribers():
    try:
        with open(SUBS_PATH, "r", encoding="utf-8") as f:
            daftar = [str(x) for x in json.load(f)]
    except Exception:
        daftar = []
    if TELEGRAM_CHAT_ID and str(TELEGRAM_CHAT_ID) not in daftar:
        daftar.append(str(TELEGRAM_CHAT_ID))
    return daftar


def tambah_subscriber(chat_id):
    with _subs_lock:
        daftar = set(baca_subscribers())
        daftar.add(str(chat_id))
        try:
            with open(SUBS_PATH, "w", encoding="utf-8") as f:
                json.dump(sorted(daftar), f)
        except Exception:
            pass


def tg_kirim(chat_id, teks):
    try:
        r = requests.post(f"{TG_API}/sendMessage",
                          json={"chat_id": chat_id, "text": teks}, timeout=10)
        return r.status_code == 200, r.text
    except Exception as e:
        return False, str(e)


def kirim_telegram(pesan: str):
    """Broadcast ke semua subscriber."""
    subs = baca_subscribers()
    if not subs:
        return False, "Belum ada penerima (kirim /start ke bot)"
    gagal = []
    for cid in subs:
        ok, info = tg_kirim(cid, pesan)
        if not ok:
            gagal.append(f"{cid}: {info}")
    if gagal:
        return False, " | ".join(gagal)
    return True, f"Terkirim ke {len(subs)} penerima"


def teks_menu():
    return (
        "Halo! Notifikasi Pemantauan Air sudah aktif.\n\n"
        "/status - lihat kondisi saat ini\n"
        "/on - hidupkan pompa manual\n"
        "/off - matikan pompa manual\n"
        f"/dashboard - {DASHBOARD_URL}"
    )


def teks_status():
    sensor = baca_sensor()
    if not sensor:
        return f"📊 KONDISI SAAT INI:\n⚠️ ESP32 offline / belum ada data.\nDashboard: {DASHBOARD_URL}"
    cfg = baca_config()
    tinggi = cfg.get("tinggi_bak", 72)
    level = hitung_level(sensor, tinggi)
    ntu = ambil_ntu(sensor)
    fz = evaluasi_fuzzy_mamdani(level, ntu)
    cmd = None
    try:
        cmd = db.reference("command/pompa").get()
    except Exception:
        pass
    return (
        "📊 KONDISI SAAT INI:\n"
        f"💧 Level Bak: {level}%\n"
        f"🧪 Kekeruhan: {ntu:.1f} NTU ({fz['mutu_air']})\n"
        f"🚰 Pompa: {'ON' if fz['pompa_aktif'] else 'OFF'} - PWM {fz['pwm']} ({fz['kecepatan_label']})\n"
        f"⚙️ Keputusan: {fz['keputusan']}\n"
        f"🕹️ Perintah manual terakhir: {cmd if cmd else '-'}\n"
        f"Dashboard: {DASHBOARD_URL}"
    )


def tangani_perintah(chat_id, text):
    cmd = text.split()[0].split("@")[0].lower() if text else ""
    if cmd in ("/start", "/menu"):
        tambah_subscriber(chat_id)
        tg_kirim(chat_id, teks_menu())
    elif cmd == "/on":
        ok = set_command("pompa", "ON")
        tg_kirim(chat_id, "🔌 Pompa berhasil DIHIDUPKAN secara manual." if ok
                 else "❌ Gagal mengirim perintah ke Firebase.")
    elif cmd == "/off":
        ok = set_command("pompa", "OFF")
        tg_kirim(chat_id, "🛑 Pompa berhasil DIMATIKAN secara manual." if ok
                 else "❌ Gagal mengirim perintah ke Firebase.")
    elif cmd == "/dashboard":
        tg_kirim(chat_id, f"Dashboard: {DASHBOARD_URL}")
    elif cmd == "/status":
        tg_kirim(chat_id, teks_status())


def telegram_polling_worker():
    """Baca perintah Telegram terus-menerus (jalan di thread terpisah, tanpa st.session_state)."""
    last_update_id = 0
    while True:
        try:
            res = requests.get(f"{TG_API}/getUpdates",
                               params={"offset": last_update_id + 1, "timeout": 5}, timeout=15)
            if res.status_code == 200:
                data = res.json()
                if data.get("ok"):
                    for result in data.get("result", []):
                        last_update_id = result["update_id"]
                        msg = result.get("message")
                        if msg:
                            tangani_perintah(msg["chat"]["id"], msg.get("text", "").strip())
        except Exception:
            time.sleep(3)
        time.sleep(1)


@st.cache_resource
def start_telegram_bot():
    """Jalankan bot sekali saja per proses Streamlit."""
    try:
        requests.post(f"{TG_API}/setMyCommands", json={"commands": TG_COMMANDS}, timeout=10)
    except Exception:
        pass
    thread = threading.Thread(target=telegram_polling_worker, daemon=True)
    thread.start()
    return True


start_telegram_bot()


def cek_notifikasi(fuzzy_res, water_level, ntu):
    """Kirim peringatan otomatis hanya saat kondisi penting BERUBAH (tidak spam tiap refresh)."""
    if not st.session_state.get("notifikasi_aktif", True):
        return
    penting = {
        "PROTEKSI DARURAT (AIR KERUH)": "🚨 AIR KERUH! Pompa dihentikan otomatis.",
        "TARGET PENUH TERCAPAI": "✅ Bak sudah penuh. Pompa dimatikan.",
        "PENGISIAN CEPAT (KOSONG)": "⚠️ Air bak hampir kosong. Pompa mengisi penuh.",
    }
    kini = fuzzy_res["keputusan"]
    if kini == st.session_state.get("last_keputusan"):
        return
    st.session_state.last_keputusan = kini
    if kini in penting:
        kirim_telegram(
            f"{penting[kini]}\n\n"
            f"💧 Level: {water_level}%\n"
            f"🧪 Kekeruhan: {ntu:.1f} NTU\n"
            f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"Dashboard: {DASHBOARD_URL}"
        )


# ============================================================
# EKSPOR ASET FIGMA
# ============================================================
def generate_all_figma_svgs(out_dir=None):
    if out_dir is None:
        out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figma")
    os.makedirs(out_dir, exist_ok=True)
    try:
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from figma.generate_all import generate_all as gen_figma
        return gen_figma(out_dir)
    except Exception as e:
        return f"Terjadi kesalahan saat mengekspor: {e}"


# ============================================================
# KONFIGURASI HALAMAN & TEMA STREAMLIT
# ============================================================
st.set_page_config(
    page_title="Sistem Monitoring Air IoT",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    html, body, .stApp, p, div, label, input, select, textarea, h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        color: #000000 !important;
    }

    /* Kembalikan font Material Symbols agar icon bawaan Streamlit tidak rusak */
    [class*="material-symbols"], [class*="material-icons"], .material-symbols-rounded, .material-symbols-outlined {
        font-family: 'Material Symbols Rounded', 'Material Icons' !important;
    }

    /* 1. HILANGKAN TULISAN MENTAH 'keyboard_double' & GANTI JADI TOMBOL BACK '← Kembali' */
    [data-testid="stSidebarHeader"] {
        padding: 0.8rem 1rem 0.2rem 1rem !important;
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
    }
    
    [data-testid="stSidebarCollapseButton"] {
        display: inline-flex !important;
        align-items: center !important;
        margin: 0 !important;
    }
    
    [data-testid="stSidebarCollapseButton"] button {
        background: #ffffff !important;
        border: 1px solid #90caf9 !important;
        border-radius: 12px !important;
        padding: 6px 14px !important;
        box-shadow: 0 2px 8px rgba(13, 71, 161, 0.12) !important;
        display: inline-flex !important;
        align-items: center !important;
        gap: 6px !important;
        cursor: pointer !important;
        font-size: 0px !important; /* Hapus teks mentah keyboard_double */
        line-height: 0 !important;
        overflow: hidden !important;
        min-height: 34px !important;
        transition: all 0.2s ease !important;
    }
    
    [data-testid="stSidebarCollapseButton"] button:hover {
        background: #e3f2fd !important;
        border-color: #1976d2 !important;
        transform: translateX(-2px) !important;
    }
    
    /* Sembunyikan semua elemen teks/span internal keyboard_double */
    [data-testid="stSidebarCollapseButton"] button * {
        font-size: 0px !important;
        display: none !important;
        visibility: hidden !important;
        width: 0 !important;
        height: 0 !important;
    }
    
    /* Tampilkan icon panah back dan teks 'Kembali' */
    [data-testid="stSidebarCollapseButton"] button::before {
        content: "←" !important;
        font-size: 16px !important;
        font-weight: 800 !important;
        color: #0d47a1 !important;
        line-height: 1 !important;
        display: inline-block !important;
        margin-right: 6px !important;
    }
    
    [data-testid="stSidebarCollapseButton"] button::after {
        content: "Kembali" !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        color: #0d47a1 !important;
        font-family: 'Inter', sans-serif !important;
        line-height: 1 !important;
        display: inline-block !important;
    }

    /* TOMBOL BUKA SIDEBAR SAAT COLLAPSED */
    [data-testid="stSidebarCollapsedControl"] {
        top: 0.8rem !important;
        left: 0.8rem !important;
        z-index: 999992 !important;
    }
    
    [data-testid="stSidebarCollapsedControl"] button {
        background: #ffffff !important;
        border: 1px solid #90caf9 !important;
        border-radius: 12px !important;
        padding: 6px 14px !important;
        box-shadow: 0 2px 8px rgba(13, 71, 161, 0.12) !important;
        font-size: 0px !important;
        line-height: 0 !important;
        min-height: 34px !important;
    }
    
    [data-testid="stSidebarCollapsedControl"] button * {
        font-size: 0px !important;
        display: none !important;
    }
    
    [data-testid="stSidebarCollapsedControl"] button::before {
        content: "☰" !important;
        font-size: 16px !important;
        font-weight: 800 !important;
        color: #0d47a1 !important;
        margin-right: 6px !important;
    }
    
    [data-testid="stSidebarCollapsedControl"] button::after {
        content: "Menu" !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        color: #0d47a1 !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* 2. HILANGKAN WARNA HITAM PADA HEADER & ATUR WARNA TEMA PENUH */
    header, [data-testid="stHeader"], .stAppHeader {
        background-color: transparent !important;
        background: transparent !important;
    }
    
    [data-testid="stDecoration"] {
        display: none !important;
    }
    
    [data-testid="stToolbar"] {
        right: 1.5rem !important;
        background: transparent !important;
    }
    
    [data-testid="stToolbar"] button, [data-testid="stToolbar"] span, [data-testid="stToolbar"] svg {
        color: #000000 !important;
        fill: #000000 !important;
    }
    
    [data-testid="stAppViewContainer"], .stApp {
        background-color: #d1e3f8 !important;
    }
    
    /* 2. OPTIMALISASI CONTAINER HALAMAN UTAMA (RESPONSIF & PADDING BERSIH) */
    .block-container, [data-testid="block-container"] {
        padding-top: 1.8rem !important;
        padding-bottom: 2rem !important;
        padding-left: clamp(1rem, 3vw, 2.5rem) !important;
        padding-right: clamp(1rem, 3vw, 2.5rem) !important;
        max-width: 100% !important;
    }
    
    /* 3. SIDEBAR RESPONSIF */
    [data-testid="stSidebar"] {
        background-color: #bbdefb !important;
        border-right: 1px solid #90caf9;
    }
    [data-testid="stSidebarUserContent"] {
        padding-top: 1.2rem !important;
        padding-bottom: 1.5rem !important;
    }
    
    /* 4. GRID KARTU METRIK RESPONSIF DENGAN TINGGI SERAGAM */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(185px, 1fr));
        gap: 14px;
        width: 100%;
        margin-bottom: 20px;
    }
    
    .metric-card {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 16px 18px;
        box-shadow: 0 4px 16px rgba(13, 71, 161, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.8);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 125px;
        box-sizing: border-box;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(13, 71, 161, 0.12);
    }
    .metric-title {
        font-size: 11.5px;
        font-weight: 700;
        color: #455A64 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
    }
    .metric-value {
        font-size: 24px;
        font-weight: 800;
        color: #000000 !important;
        line-height: 1.2;
        margin-bottom: 4px;
    }
    .metric-sub {
        font-size: 11.5px;
        color: #37474F !important;
        line-height: 1.3;
    }
    
    /* 5. TANK CONTAINER RESPONSIF */
    .tank-container {
        background: #ffffff;
        border-radius: 22px;
        padding: 22px 24px;
        box-shadow: 0 6px 20px rgba(13, 71, 161, 0.07);
        border: 1px solid rgba(255, 255, 255, 0.8);
        text-align: center;
        width: 100%;
        box-sizing: border-box;
    }
    .tank-percentage {
        font-size: clamp(2.8rem, 5vw, 4.2rem);
        font-weight: 800;
        color: #000000;
        line-height: 1.1;
        margin: 8px 0;
    }
    
    .stButton>button {
        border-radius: 30px !important;
        border: none !important;
        background: linear-gradient(135deg, #42a5f5, #1976d2) !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 10px 24px !important;
        box-shadow: 0 4px 15px rgba(25, 118, 210, 0.35) !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #1e88e5, #0d47a1) !important;
        box-shadow: 0 6px 20px rgba(13, 71, 161, 0.45) !important;
    }
    
    .badge-pill {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.3px;
        text-transform: uppercase;
    }

    @media (max-width: 768px) {
        .block-container, [data-testid="block-container"] {
            padding-top: 1rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        .metric-grid {
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)) !important;
            gap: 10px !important;
        }
        .metric-value {
            font-size: 20px !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Session state
if "auto_refresh" not in st.session_state:
    st.session_state.auto_refresh = True
if "notifikasi_aktif" not in st.session_state:
    st.session_state.notifikasi_aktif = True

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("""
        <div style='text-align:center; padding: 10px 0;'>
            <span style='font-size: 42px;'>💧</span>
            <h2 style='margin: 0; color: #000000; font-size: 24px;'>Water Monitoring</h2>
        </div>
    """, unsafe_allow_html=True)
    menu = st.radio(
        "Menu",
        ["Dashboard Utama", "Grafik dan Historis", "Riwayat & Notifikasi"],
        key="nav_menu"
    )

    if menu != "Dashboard Utama":
        if st.button("← Kembali ke Dashboard Utama", key="btn_back_sidebar", use_container_width=True):
            st.session_state.nav_menu = "Dashboard Utama"
            st.rerun()

    st.write("---")

    sensor_now = baca_sensor()
    if sensor_now:
        wkt = sensor_now.get("waktu", datetime.now().strftime("%H:%M:%S"))
        ip = sensor_now.get("ipv4", "WiFi Online")
        st.markdown(f"""
            <div style='background: rgba(255,255,255,0.8); padding: 12px; border-radius: 14px; border-left: 4px solid #2e7d32; margin-bottom: 12px;'>
                <p style='margin:0; font-size: 12px; font-weight: 700; color: #2e7d32;'>● ESP32 TERHUBUNG</p>
                <p style='margin:2px 0 0 0; font-size: 11px; color: #000000;'>Waktu: <b>{wkt}</b></p>
                <p style='margin:0; font-size: 10px; color: #000000;'>IP: {ip}</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style='background: rgba(255,255,255,0.8); padding: 12px; border-radius: 14px; border-left: 4px solid #c62828; margin-bottom: 12px;'>
                <p style='margin:0; font-size: 12px; font-weight: 700; color: #c62828;'>○ ESP32 OFFLINE</p>
                <p style='margin:2px 0 0 0; font-size: 11px; color: #000000;'>Menunggu transmisi data...</p>
            </div>
        """, unsafe_allow_html=True)

    st.session_state.auto_refresh = st.checkbox("Auto-Refresh Live Data", value=st.session_state.auto_refresh)

    st.write("---")
    st.markdown("**📱 Telegram Bot**")
    st.session_state.notifikasi_aktif = st.toggle(
        "Notifikasi otomatis", value=st.session_state.notifikasi_aktif)
    st.caption("Perintah bot: /status /on /off /dashboard /menu")
    st.caption(f"Penerima terdaftar: {len(baca_subscribers())}")
    if st.button("Tes Telegram"):
        st.session_state.hasil_tes = kirim_telegram("Tes notifikasi dari dashboard")
    if "hasil_tes" in st.session_state:
        ok, info = st.session_state.hasil_tes
        if ok:
            st.success(info)
        else:
            st.error(info)



# ============================================================
# 1. DASHBOARD UTAMA
# ============================================================
if menu == "Dashboard Utama":
    st.markdown("<h2 style='margin-bottom: 24px; color: #000000;'>Dashboard Monitoring Air</h2>", unsafe_allow_html=True)

    cfg = baca_config()
    tinggi_bak = cfg.get("tinggi_bak", 72)
    sensor = baca_sensor()

    jarak       = float(sensor.get("jarak", 0.0))       if sensor else 0.0
    debit       = float(sensor.get("debit", 0.0))       if sensor else 0.0
    total_liter = float(sensor.get("total_liter", 0.0)) if sensor else 0.0
    ntu         = ambil_ntu(sensor)
    waktu_str   = str(sensor.get("waktu", datetime.now().strftime("%H:%M:%S"))) if sensor else "—"

    water_level = hitung_level(sensor, tinggi_bak)

    fuzzy_res = evaluasi_fuzzy_mamdani(water_level, ntu)
    if sensor:
        cek_notifikasi(fuzzy_res, water_level, ntu)

    pwm_color = "#2e7d32" if fuzzy_res["pompa_aktif"] else "#546e7a"
    pwm_text = "PWM " + str(fuzzy_res["pwm"]) if fuzzy_res["pompa_aktif"] else "MATI"

    st.markdown(f"""
        <div class='metric-grid'>
            <div class='metric-card'>
                <div class='metric-title'>Status PWM</div>
                <div class='metric-value' style='color: {pwm_color};'>{pwm_text}</div>
                <div class='metric-sub'>Duty: <b>{fuzzy_res["duty"]}%</b> ({fuzzy_res["tegangan_volt"]:.1f}V DC)</div>
            </div>
            <div class='metric-card'>
                <div class='metric-title'>Status Kecepatan</div>
                <div class='metric-value' style='color: {fuzzy_res["badge_color"]};'>{fuzzy_res["kecepatan_label"]}</div>
                <div class='metric-sub'>Mode: <b>Otonom Cerdas</b> (ESP32)</div>
            </div>
            <div class='metric-card'>
                <div class='metric-title'>Kualitas Air</div>
                <div class='metric-value' style='color: {fuzzy_res["warna_mutu"]};'>{ntu:.1f} <span style='font-size: 14px;'>NTU</span></div>
                <div class='metric-sub'>Status: <b>{fuzzy_res["mutu_air"]}</b></div>
            </div>
            <div class='metric-card'>
                <div class='metric-title'>Debit Air Masuk</div>
                <div class='metric-value'>{debit:.1f} <span style='font-size: 14px;'>L/min</span></div>
                <div class='metric-sub'>Sensor YF-S201</div>
            </div>
            <div class='metric-card'>
                <div class='metric-title'>Total Air Terpakai</div>
                <div class='metric-value'>{total_liter:.1f} <span style='font-size: 14px;'>Liter</span></div>
                <div class='metric-sub'>Akumulasi Pengisian</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class='tank-container'>
            <h3 style='margin: 0 0 8px 0; font-size: 1.25rem; color: #000000;'>Ketinggian Bak Mandi</h3>
            <div class='tank-percentage'>
                {water_level}%
            </div>
            <div style='background: #e1f5fe; border-radius: 12px; height: 16px; width: 100%; overflow: hidden; margin: 12px 0;'>
                <div style='background: linear-gradient(90deg, #42a5f5, #1976d2); width: {water_level}%; height: 100%; transition: width 0.5s ease;'></div>
            </div>
            <p style='margin: 6px 0; font-size: 13.5px; color: #000000;'>
                Jarak Permukaan ke Sensor: <b>{jarak:.1f} cm</b> (Tinggi Bak Acuan: {tinggi_bak} cm)
            </p>
            <p style='margin: 4px 0 0 0; font-size: 11px; color: #546E7A; font-style: italic;'>
                Diperbarui dari ESP32: {waktu_str}
            </p>
        </div>
    """, unsafe_allow_html=True)

    if st.session_state.auto_refresh:
        time.sleep(3)
        st.rerun()


# ============================================================
# 2. GRAFIK & HISTORIS
# ============================================================
elif menu == "Grafik dan Historis":
    if st.button("← Kembali ke Dashboard Utama", key="btn_back_p1"):
        st.session_state.nav_menu = "Dashboard Utama"
        st.rerun()

    st.markdown("<h2 style='color: #000000;'>Grafik dan Historis</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#000000; font-size: 14px;'>Visualisasi tren ketinggian air, fluktuasi kekeruhan (NTU), dan debit aliran air secara berkala.</p>", unsafe_allow_html=True)

    logs = baca_logs()

    if logs:
        df_logs = pd.DataFrame(logs)
        st.subheader("Historis")

        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.markdown("### Tren Level Air (%)")
            chart_data_level = df_logs[["waktu", "status"]].copy().head(30)
            st.caption("Data pemantauan status ketinggian air terbaru.")
            st.dataframe(chart_data_level, use_container_width=True)

        with col_g2:
            st.markdown("### Riwayat Sensor")
            st.caption("Pencatatan sinkronisasi data telemetri ke Firebase Database.")
            st.dataframe(df_logs[["waktu", "aktivitas"]].head(30), use_container_width=True)
    else:
        st.info("💡 Belum ada riwayat telemetri yang tercatat di Firebase logs.")

    st.write("---")
    st.markdown("### Simulasi respon terhadap kekeruhan")
    sim_data = pd.DataFrame({
        "Kekeruhan (NTU)": [5, 15, 25, 40, 70, 95, 110, 150],
        "Tingkat Keamanan": [100, 95, 90, 75, 60, 45, 0, 0],
        "Rekomendasi": ["Air Bersih", "Air Bersih", "Air Bersih", "Waspada", "Agak Keruh", "Batas Kritis", "Stop Pompa", "Stop Pompa"]
    })
    st.line_chart(sim_data.set_index("Kekeruhan (NTU)")["Tingkat Keamanan"])


# ============================================================
# 3. RIWAYAT & NOTIFIKASI
# ============================================================
elif menu == "Riwayat & Notifikasi":
    if st.button("← Kembali ke Dashboard Utama", key="btn_back_p2"):
        st.session_state.nav_menu = "Dashboard Utama"
        st.rerun()

    st.markdown("<h2 style='color: #000000;'>Riwayat Aktivitas & Log Notifikasi</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#000000; font-size: 14px;'>Catatan peristiwa otomatis pengisian air, peringatan Telegram, dan status bak mandi.</p>", unsafe_allow_html=True)

    logs = baca_logs()
    if logs:
        df = pd.DataFrame(logs)

        kolom_tersedia = [c for c in ["waktu", "aktivitas", "status"] if c in df.columns]
        df_tampil = df[kolom_tersedia].copy()
        df_tampil.rename(columns={
            "waktu": "Waktu Transmisi",
            "aktivitas": "Rincian Aktivitas",
            "status": "Status Bak"
        }, inplace=True)

        if "Status Bak" in df_tampil.columns:
            status_unik = ["Semua"] + list(df_tampil["Status Bak"].dropna().unique())
            pilihan_filter = st.selectbox("Filter berdasarkan status:", status_unik)
            if pilihan_filter != "Semua":
                df_tampil = df_tampil[df_tampil["Status Bak"] == pilihan_filter]

        st.dataframe(df_tampil, use_container_width=True, height=450)
    else:
        st.info("Belum ada riwayat aktivitas yang tersimpan di Firebase.")

    if st.button("🔄 Segarkan Data Log"):
        st.rerun()


if __name__ == "__main__":
    print("=" * 60)
    print("  SISTEM MONITORING AIR IoT - ALL IN ONE SCRIPT")
    print("=" * 60)
    print(generate_all_figma_svgs())
    print("\nUntuk menjalankan Web Dashboard Streamlit:")
    print("  streamlit run app.py")
    print("=" * 60)
