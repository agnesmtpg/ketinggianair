import os
import sys
import json
import threading
import time
from datetime import datetime

import requests
import pandas as pd
import streamlit as st

try:
    import firebase_admin
    from firebase_admin import credentials, db
except ImportError:
    firebase_admin = None
    credentials = None
    db = None

# ============================================================
# KONFIGURASI FIREBASE & TELEGRAM (SESUAI KODINGAN ARDUINO)
# ============================================================
FIREBASE_URL  = "https://ketinggian-dd1fb-default-rtdb.firebaseio.com"
FIREBASE_AUTH = "N6jEJCYluaJ0aHZYRGN3WUAiqEaMGXd37d2haHHY"
KEY_PATH      = r"D:\proyek 3 & proposal ta\web\serviceAccountKey.json"

TELEGRAM_TOKEN   = os.environ.get("TELEGRAM_TOKEN", "8953132207:AAE4iCqGj9weJ80VXJWjb4WLaSEzb2aNI78")
TELEGRAM_CHAT_ID = "1156974464"
DASHBOARD_URL    = "http://localhost:8501"
SUBS_PATH        = os.path.join(os.path.dirname(os.path.abspath(__file__)), "telegram_subscribers.json")
TG_API           = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

TG_COMMANDS = [
    {"command": "status", "description": "Lihat kondisi air & pompa saat ini"},
    {"command": "dashboard", "description": "Buka link web dashboard"},
    {"command": "menu", "description": "Tampilkan menu perintah"},
]


@st.cache_resource
def init_firebase():
    """Inisialisasi Firebase Admin SDK jika tersedia & serviceAccountKey valid."""
    if firebase_admin is not None and not firebase_admin._apps:
        try:
            if os.path.exists(KEY_PATH):
                cred = credentials.Certificate(KEY_PATH)
                firebase_admin.initialize_app(cred, {"databaseURL": FIREBASE_URL})
                return True
        except Exception:
            pass
    return False


init_firebase()


# ============================================================
# FUNGSI PEMBACAAN DATA FIREBASE (SESUAI NODE ARDUINO)
# ============================================================
def baca_sensor():
    """
    Membaca data LATEST dari node '/bak_mandi/latest'.
    Struktur data dari ESP32:
    - distanceCm, levelPersen, pwmMosfet, statusPompa,
    - flowRate, totalLiter, turbidityVolt, turbidityRaw, timestamp
    """
    data = None
    try:
        if firebase_admin and firebase_admin._apps:
            data = db.reference("bak_mandi/latest").get()
    except Exception:
        pass

    if not data:
        try:
            r = requests.get(f"{FIREBASE_URL}/bak_mandi/latest.json?auth={FIREBASE_AUTH}", timeout=5)
            if r.status_code == 200 and r.json():
                data = r.json()
        except Exception:
            pass

    return data if isinstance(data, dict) else None


def baca_history(limit=250):
    """
    Membaca data HISTORIS dari node '/bak_mandi/history' (Firebase RTDB).
    Setiap entri disimpan oleh ESP32 secara periodik.
    """
    data = None
    try:
        if firebase_admin and firebase_admin._apps:
            data = db.reference("bak_mandi/history").order_by_key().limit_to_last(limit).get()
    except Exception:
        pass

    if not data:
        try:
            r = requests.get(
                f"{FIREBASE_URL}/bak_mandi/history.json",
                params={"orderBy": '"$key"', "limitToLast": limit, "auth": FIREBASE_AUTH},
                timeout=8
            )
            if r.status_code == 200 and r.json():
                data = r.json()
        except Exception:
            pass

    if not data:
        try:
            r = requests.get(f"{FIREBASE_URL}/bak_mandi/history.json?auth={FIREBASE_AUTH}", timeout=8)
            if r.status_code == 200 and r.json():
                data = r.json()
        except Exception:
            pass

    rows = []
    if isinstance(data, dict):
        for k, v in data.items():
            if isinstance(v, dict):
                row = dict(v)
                row["id_log"] = str(k)
                rows.append(row)

    def sort_key(item):
        ts = str(item.get("timestamp", item.get("id_log", "")))
        if ts.startswith("2026"):
            return (2, ts)
        elif ts[:4].isdigit() and 2024 <= int(ts[:4]) <= 2030:
            return (1, ts)
        return (0, ts)

    rows = sorted(rows, key=sort_key, reverse=True)
    return rows


def evaluasi_kualitas_air(volt):
    """
    Sensor turbidity murni memantau kualitas air (tidak menghentikan pompa):
      - volt >= 2.4 V : Jernih
      - 1.6 V <= volt < 2.4 V : Agak Keruh
      - volt < 1.6 V : Keruh
    """
    try:
        v = float(volt)
    except Exception:
        v = 3.0

    if v >= 2.4:
        return "JERNIH", "#2e7d32"
    elif v >= 1.6:
        return "AGAK KERUH", "#f57f17"
    else:
        return "KERUH", "#c62828"


def get_badge_pompa(status_pompa):
    """Warna badge status pompa (murni berdasarkan ketinggian air)."""
    st_upper = str(status_pompa).upper()
    if "80%" in st_upper or "PENUH" in st_upper:
        return "#1565c0"  # Biru Target Tercapai
    elif "CEPAT" in st_upper:
        return "#2e7d32"  # Hijau Cepat
    elif "SEDANG" in st_upper:
        return "#0288d1"  # Biru Cerah Sedang
    elif "PELAN" in st_upper:
        return "#f57f17"  # Oranye Pelan
    else:
        return "#546e7a"  # Abu-abu Mati


# ============================================================
# TELEGRAM BOT & NOTIFIKASI
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
    """Broadcast pesan ke seluruh subscriber Telegram terdaftar."""
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
        "Halo! Notifikasi Sistem Pemantauan Air Bak Mandi aktif.\n\n"
        "/status - Cek kondisi air & pompa saat ini\n"
        f"/dashboard - Buka dashboard {DASHBOARD_URL}"
    )


def teks_status():
    sensor = baca_sensor()
    if not sensor:
        return f"📊 KONDISI SAAT INI:\n⚠️ ESP32 Offline / belum ada data di /bak_mandi/latest.\nDashboard: {DASHBOARD_URL}"

    level = float(sensor.get("levelPersen", 0.0))
    jarak = float(sensor.get("distanceCm", 0.0))
    pwm = int(sensor.get("pwmMosfet", 0))
    status_p = str(sensor.get("statusPompa", "MATI"))
    flow = float(sensor.get("flowRate", 0.0))
    volt = float(sensor.get("turbidityVolt", 0.0))
    wkt = str(sensor.get("timestamp", "-"))
    mutu, _ = evaluasi_kualitas_air(volt)

    return (
        "📊 KONDISI AIR & POMPA SAAT INI:\n"
        f"💧 Level Bak: {level:.1f}% (Jarak: {jarak:.1f} cm)\n"
        f"🚰 Status Pompa: {status_p} (PWM: {pwm})\n"
        f"🌊 Debit Aliran: {flow:.1f} L/min\n"
        f"🧪 Turbidity: {volt:.2f} V ({mutu})\n"
        f"⏰ Terakhir Diperbarui: {wkt}\n"
        f"Dashboard: {DASHBOARD_URL}"
    )


def tangani_perintah(chat_id, text):
    cmd = text.split()[0].split("@")[0].lower() if text else ""
    if cmd in ("/start", "/menu"):
        tambah_subscriber(chat_id)
        tg_kirim(chat_id, teks_menu())
    elif cmd == "/status":
        tg_kirim(chat_id, teks_status())
    elif cmd == "/dashboard":
        tg_kirim(chat_id, f"Link Dashboard Monitoring: {DASHBOARD_URL}")


def telegram_polling_worker():
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
    try:
        requests.post(f"{TG_API}/setMyCommands", json={"commands": TG_COMMANDS}, timeout=10)
    except Exception:
        pass
    thread = threading.Thread(target=telegram_polling_worker, daemon=True)
    thread.start()
    return True


start_telegram_bot()


def cek_notifikasi_otomatis(sensor):
    """Notifikasi hanya fokus pada target ketinggian air."""
    if not sensor or not st.session_state.get("notifikasi_aktif", True):
        return

    status_kini = str(sensor.get("statusPompa", "MATI"))
    if status_kini == st.session_state.get("last_status_pompa"):
        return

    st.session_state.last_status_pompa = status_kini
    level = float(sensor.get("levelPersen", 0.0))
    wkt = str(sensor.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    if "80%" in status_kini or "PENUH" in status_kini:
        kirim_telegram(
            f"✅ TARGET 80% TERCAPAI!\n"
            f"Bak mandi telah mencapai 80%. Pompa telah dimatikan otomatis oleh ESP32.\n\n"
            f"💧 Level Air: {level:.1f}%\n"
            f"⏰ Waktu: {wkt}\n"
            f"Dashboard: {DASHBOARD_URL}"
        )
    elif "CEPAT" in status_kini and level <= 25.0:
        kirim_telegram(
            f"⚠️ AIR BAK RENDAH!\n"
            f"Level air rendah ({level:.1f}%). Pompa mulai mengisi daya penuh.\n\n"
            f"⏰ Waktu: {wkt}\n"
            f"Dashboard: {DASHBOARD_URL}"
        )


# ============================================================
# KONFIGURASI TAMPILAN STREAMLIT
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

    [class*="material-symbols"], [class*="material-icons"], .material-symbols-rounded, .material-symbols-outlined {
        font-family: 'Material Symbols Rounded', 'Material Icons' !important;
    }

    /* TOMBOL KEMBALI SIDEBAR */
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
        font-size: 0px !important;
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
    
    [data-testid="stSidebarCollapseButton"] button * {
        font-size: 0px !important;
        display: none !important;
        visibility: hidden !important;
        width: 0 !important;
        height: 0 !important;
    }
    
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

    /* LATAR BELAKANG AQUATIC BLUE */
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
    
    .block-container, [data-testid="block-container"] {
        padding-top: 1.8rem !important;
        padding-bottom: 2rem !important;
        padding-left: clamp(1rem, 3vw, 2.5rem) !important;
        padding-right: clamp(1rem, 3vw, 2.5rem) !important;
        max-width: 100% !important;
    }
    
    /* SIDEBAR */
    [data-testid="stSidebar"] {
        background-color: #bbdefb !important;
        border-right: 1px solid #90caf9;
    }
    [data-testid="stSidebarUserContent"] {
        padding-top: 1.2rem !important;
        padding-bottom: 1.5rem !important;
    }
    
    /* GRID KARTU METRIK */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
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
    
    /* TANGKI AIR */
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

# State
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
        ["Dashboard Utama", "Riwayat & Notifikasi"],
        key="nav_menu"
    )

    if menu != "Dashboard Utama":
        if st.button("← Kembali ke Dashboard Utama", key="btn_back_sidebar", use_container_width=True):
            st.session_state.nav_menu = "Dashboard Utama"
            st.rerun()

    st.write("---")

    sensor_now = baca_sensor()
    if sensor_now:
        wkt = sensor_now.get("timestamp", datetime.now().strftime("%H:%M:%S"))
        st.markdown(f"""
            <div style='background: rgba(255,255,255,0.85); padding: 12px; border-radius: 14px; border-left: 4px solid #2e7d32; margin-bottom: 12px;'>
                <p style='margin:0; font-size: 12px; font-weight: 700; color: #2e7d32;'>● ESP32 TERHUBUNG</p>
                <p style='margin:2px 0 0 0; font-size: 11px; color: #000000;'>Node: <b>/bak_mandi/latest</b></p>
                <p style='margin:0; font-size: 10px; color: #000000;'>Waktu: {wkt}</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style='background: rgba(255,255,255,0.85); padding: 12px; border-radius: 14px; border-left: 4px solid #c62828; margin-bottom: 12px;'>
                <p style='margin:0; font-size: 12px; font-weight: 700; color: #c62828;'>○ ESP32 OFFLINE</p>
                <p style='margin:2px 0 0 0; font-size: 11px; color: #000000;'>Menunggu data di /bak_mandi/latest...</p>
            </div>
        """, unsafe_allow_html=True)

    st.session_state.auto_refresh = st.checkbox("Auto-Refresh Live Data", value=st.session_state.auto_refresh)

    st.write("---")
    st.markdown("**📱 Telegram Bot**")
    st.session_state.notifikasi_aktif = st.toggle("Notifikasi otomatis", value=st.session_state.notifikasi_aktif)
    st.caption("Perintah bot: /status /dashboard /menu")
    st.caption(f"Penerima terdaftar: {len(baca_subscribers())}")
    if st.button("Tes Telegram"):
        st.session_state.hasil_tes = kirim_telegram("Tes notifikasi dari dashboard monitoring air.")
    if "hasil_tes" in st.session_state:
        ok, info = st.session_state.hasil_tes
        if ok:
            st.success(info)
        else:
            st.error(info)


# ============================================================
# 1. MENU: DASHBOARD UTAMA
# ============================================================
if menu == "Dashboard Utama":
    st.markdown("<h2 style='margin-bottom: 24px; color: #000000;'>Dashboard Monitoring Air</h2>", unsafe_allow_html=True)

    sensor = baca_sensor()

    # Ekstraksi Data dari Node /bak_mandi/latest
    distanceCm       = float(sensor.get("distanceCm", 0.0))       if sensor else 0.0
    levelPersen      = float(sensor.get("levelPersen", 0.0))      if sensor else 0.0
    pwmMosfet        = int(sensor.get("pwmMosfet", 0))            if sensor else 0
    statusPompa      = str(sensor.get("statusPompa", "MATI"))     if sensor else "OFFLINE"
    flowRate         = float(sensor.get("flowRate", 0.0))         if sensor else 0.0
    totalLiter       = float(sensor.get("totalLiter", 0.0))       if sensor else 0.0
    turbidityVolt    = float(sensor.get("turbidityVolt", 3.0))    if sensor else 3.0
    turbidityRaw     = int(sensor.get("turbidityRaw", 0))         if sensor else 0
    timestamp_str    = str(sensor.get("timestamp", "—"))          if sensor else "—"

    # Evaluasi Mutu Air & Badge (Kekeruhan murni informasi kualitas)
    mutu_air, warna_mutu = evaluasi_kualitas_air(turbidityVolt)
    badge_pompa = get_badge_pompa(statusPompa)

    # Cek notifikasi otomatis Telegram
    cek_notifikasi_otomatis(sensor)

    duty_percent = int((pwmMosfet / 255.0) * 100)
    tegangan_motor = round((pwmMosfet / 255.0) * 12.0, 1)
    pwm_color = "#2e7d32" if pwmMosfet > 0 else "#546e7a"
    pwm_text = f"PWM {pwmMosfet}" if pwmMosfet > 0 else "MATI (0)"

    # Format status kecepatan tanpa persenan
    status_kecepatan = statusPompa.replace(" 80%", "").replace("80%", "").replace("(100%)", "").replace("%", "").strip()
    if not status_kecepatan:
        status_kecepatan = "PENUH" if "PENUH" in statusPompa.upper() else "MATI"

    # BARIS 1: 4 KARTU METRIK LENGKAP
    st.markdown(f"""
        <div class='metric-grid'>
            <div class='metric-card'>
                <div class='metric-title'>Status PWM</div>
                <div class='metric-value' style='color: {pwm_color};'>{pwm_text}</div>
                <div class='metric-sub'>Duty: <b>{duty_percent}%</b> ({tegangan_motor:.1f}V DC)</div>
            </div>
            <div class='metric-card'>
                <div class='metric-title'>Status Kecepatan</div>
                <div class='metric-value' style='color: {badge_pompa};'>{status_kecepatan}</div>
                <div class='metric-sub'>&nbsp;</div>
            </div>
            <div class='metric-card'>
                <div class='metric-title'>Kualitas Air</div>
                <div class='metric-value' style='color: {warna_mutu};'>{turbidityVolt:.2f} <span style='font-size: 14px;'>Volt</span></div>
                <div class='metric-sub'>Kondisi: <b>{mutu_air}</b> (ADC: {turbidityRaw})</div>
            </div>
            <div class='metric-card'>
                <div class='metric-title'>Debit Air Masuk</div>
                <div class='metric-value'>{flowRate:.1f} <span style='font-size: 14px;'>L/min</span></div>
                <div class='metric-sub'>Sensor YF-S201</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # BARIS 2: KARTU VISUALISASI LEVEL BAK AIR
    water_display = int(round(levelPersen))
    st.markdown(f"""
        <div class='tank-container'>
            <h3 style='margin: 0 0 8px 0; font-size: 1.25rem; color: #000000;'>Status Ketinggian Air</h3>
            <div class='tank-percentage'>
                {water_display}%
            </div>
            <div style='background: #e1f5fe; border-radius: 12px; height: 16px; width: 100%; overflow: hidden; margin: 12px 0;'>
                <div style='background: linear-gradient(90deg, #42a5f5, #1976d2); width: {min(100, max(0, water_display))}%; height: 100%; transition: width 0.5s ease;'></div>
            </div>
            <p style='margin: 6px 0; font-size: 13.5px; color: #000000;'>
                Jarak Permukaan ke Sensor: <b>{distanceCm:.1f} cm</b>
            </p>
            <p style='margin: 4px 0 0 0; font-size: 11px; color: #546E7A; font-style: italic;'>
                Diperbarui dari ESP32: {timestamp_str}
            </p>
        </div>
    """, unsafe_allow_html=True)

    if st.session_state.auto_refresh:
        time.sleep(3)
        st.rerun()


# ============================================================
# 2. MENU: RIWAYAT & NOTIFIKASI
# ============================================================
elif menu == "Riwayat & Notifikasi":
    if st.button("← Kembali ke Dashboard Utama", key="btn_back_p2"):
        st.session_state.nav_menu = "Dashboard Utama"
        st.rerun()

    st.markdown("<h2 style='color: #000000;'>Riwayat Aktivitas & Log Notifikasi</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#000000; font-size: 14px;'>Catatan telemetri berkala pengisian air, status kecepatan pompa, dan kondisi bak mandi dari node <code>/bak_mandi/history</code>.</p>", unsafe_allow_html=True)

    hist_data = baca_history(limit=250)
    if hist_data:
        cleaned_rows = []
        for r in hist_data:
            ts = str(r.get("timestamp", r.get("id_log", "-")))

            # Mendukung nama field 'statusPompa' maupun 'status' dari ESP32
            status_raw = str(r.get("statusPompa") or r.get("status") or "-")
            status_clean = status_raw.replace(" 80%", "").replace("80%", "").replace("(100%)", "").replace("%", "").strip()

            level = r.get("levelPersen")
            level_str = f"{float(level):.1f}%" if level is not None and float(level) >= 0 else "-"

            dist = r.get("distanceCm")
            dist_str = f"{float(dist):.1f} cm" if dist is not None and float(dist) >= 0 else "-"

            volt = r.get("turbidityVolt")
            if volt is not None:
                mutu, _ = evaluasi_kualitas_air(volt)
                volt_str = f"{float(volt):.2f} V ({mutu})"
            else:
                volt_str = "-"

            flow = r.get("flowRate")
            flow_str = f"{float(flow):.1f} L/m" if flow is not None else "-"

            total = r.get("totalLiter")
            total_str = f"{float(total):.1f} L" if total is not None else "-"

            pwm = r.get("pwmMosfet")
            pwm_str = str(int(pwm)) if pwm is not None else "-"

            cleaned_rows.append({
                "Waktu Transmisi": ts,
                "Status Pompa": status_clean,
                "Level Air": level_str,
                "Jarak Sensor": dist_str,
                "Kualitas Air": volt_str,
                "Debit Aliran": flow_str,
                "Total Volume": total_str,
                "PWM Pompa": pwm_str
            })

        df_tampil = pd.DataFrame(cleaned_rows)

        # Fitur Filter Status Pompa
        if "Status Pompa" in df_tampil.columns:
            status_unik = ["Semua"] + [s for s in df_tampil["Status Pompa"].dropna().unique() if s != "-"]
            pilihan_filter = st.selectbox("Filter berdasarkan status pompa:", status_unik)
            if pilihan_filter != "Semua":
                df_tampil = df_tampil[df_tampil["Status Pompa"] == pilihan_filter]

        st.dataframe(df_tampil, use_container_width=True, height=480)
    else:
        st.info("Belum ada data riwayat yang tersimpan di node /bak_mandi/history Firebase.")

    if st.button("🔄 Segarkan Data Log"):
        st.rerun()


if __name__ == "__main__":
    print("=" * 60)
    print("  SISTEM MONITORING AIR IoT - STREAMLIT DASHBOARD")
    print("  Terkoneksi ke node: /bak_mandi/latest & /bak_mandi/history")
    print("=" * 60)
    print("Jalankan web dengan perintah: streamlit run app.py")
    print("=" * 60)