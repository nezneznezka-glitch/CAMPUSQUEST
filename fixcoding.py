import streamlit as st
import time

# Fungsi header dengan warna oranye tanpa garis pembatas
def tampilkan_header():
    st.markdown("<h1 style='color: orange;'>CAMPUSQUEST</h1>", unsafe_allow_html=True)
    st.markdown("##### Student Productivity Quest")

tampilkan_header()

# Inisialisasi Session State agar data tersimpan selama aplikasi berjalan
if "total_xp" not in st.session_state:
    st.session_state.total_xp = 0
if "total_menit" not in st.session_state:
    st.session_state.total_menit = 0
if "jumlah_quest_selesai" not in st.session_state:
    st.session_state.jumlah_quest_selesai = 0
if "step" not in st.session_state:
    st.session_state.step = "input_profil"

pilihan_durasi = [30, 60, 90, 120]

# --- STEP 1: INPUT PROFIL ---
if st.session_state.step == "input_profil":
    nama = st.text_input("Masukkan nama:")
    fakultas = st.text_input("Masukkan fakultas:")

    if st.button("Lanjutkan"):
        if not nama:
            st.warning("Nama tidak boleh kosong.")
        elif not fakultas:
            st.warning("Fakultas tidak boleh kosong.")
        else:
            st.session_state.nama = nama
            st.session_state.fakultas = fakultas
            st.session_state.step = "input_aktivitas"
            st.rerun()

# --- STEP 2: INPUT AKTIVITAS ---
elif st.session_state.step == "input_aktivitas":
    st.write(f"Selamat datang {st.session_state.nama} dari {st.session_state.fakultas}")
    
    aktivitas = st.text_input("Kamu mau belajar apa? (ketik 'selesai' untuk keluar):")

    if st.button("Proses Aktivitas"):
        if aktivitas == "selesai":
            st.session_state.step = "ringkasan"
            st.rerun()
        elif not aktivitas:
            st.warning("Aktivitas tidak boleh kosong.")
        else:
            st.session_state.aktivitas = aktivitas
            st.session_state.step = "pilih_durasi"
            st.rerun()

# --- STEP 3: PILIH DURASI ---
elif st.session_state.step == "pilih_durasi":
    st.write(f"Aktivitas kamu: {st.session_state.aktivitas}")
    
    pilihan_teks = []
    for i, durasi in enumerate(pilihan_durasi, start=1):
        pilihan_teks.append(f"{i}. {durasi} menit")
        
    pilihan = st.selectbox("Pilih durasi (1-4):", options=["1", "2", "3", "4"], format_func=lambda x: pilihan_teks[int(x)-1])

    if st.button("Mulai Timer Belajar"):
        st.session_state.durasi_menit = pilihan_durasi[int(pilihan) - 1]
        st.session_state.step = "jalankan_timer"
        st.rerun()

# --- STEP 4: JALANKAN TIMER ---
elif st.session_state.step == "jalankan_timer":
    durasi_menit = st.session_state.durasi_menit
    st.write(f"Target belajar {durasi_menit} menit")
    st.info("Timer dimulai!")

    durasi_detik = int(durasi_menit * 60)
    waktu_mulai = time.monotonic()

    timer_placeholder = st.empty()

    while True:
        waktu_berlalu = time.monotonic() - waktu_mulai
        sisa_waktu = durasi_detik - waktu_berlalu

        if sisa_waktu <= 0:
            break

        menit = int(sisa_waktu // 60)
        detik = int(sisa_waktu % 60)

        timer_placeholder.markdown(f"### Sisa waktu: {menit:02d}:{detik:02d}")
        time.sleep(1)

    st.success("Waktu belajar selesai!")
    if st.button("Lanjut ke Istirahat"):
        st.session_state.step = "pilih_istirahat"
        st.rerun()

# --- STEP 5: PILIH & JALANKAN ISTIRAHAT ---
elif st.session_state.step == "pilih_istirahat":
    st.write("Waktunya istirahat!")
    pilihan_istirahat = st.selectbox("Pilih durasi istirahat:", ["1. Istirahat 5 menit", "2. Istirahat 10 menit"])

    if st.button("Mulai Istirahat"):
        if "5 menit" in pilihan_istirahat:
            st.session_state.durasi_istirahat = 5
        else:
            st.session_state.durasi_istirahat = 10

        st.session_state.step = "jalankan_istirahat"
        st.rerun()

elif st.session_state.step == "jalankan_istirahat":
    durasi_istirahat = st.session_state.durasi_istirahat
    st.write(f"Target istirahat: {durasi_istirahat} menit")
    st.info("Timer istirahat dimulai!")

    durasi_detik = int(durasi_istirahat * 60)
    waktu_mulai = time.monotonic()

    timer_placeholder = st.empty()

    while True:
        waktu_berlalu = time.monotonic() - waktu_mulai
        sisa_waktu = durasi_detik - waktu_berlalu

        if sisa_waktu <= 0:
            break

        menit = int(sisa_waktu // 60)
        detik = int(sisa_waktu % 60)

        timer_placeholder.markdown(f"### Sisa istirahat: {menit:02d}:{detik:02d}")
        time.sleep(1)

    st.success("Istirahat selesai!")
    if st.button("Lanjutkan ke Konfirmasi Selesai"):
        st.session_state.step = "konfirmasi_selesai"
        st.rerun()

# --- STEP 6: KONFIRMASI SELESAI ---
elif st.session_state.step == "konfirmasi_selesai":
    selesai = st.radio("Apakah aktivitas selesai? (ya/tidak):", ["ya", "tidak"])

    if st.button("Simpan Quest"):
        if selesai == "ya":
            xp = (st.session_state.durasi_menit // 10) * 10
            st.session_state.total_xp += xp
            st.session_state.total_menit += st.session_state.durasi_menit
            st.session_state.jumlah_quest_selesai += 1
            st.success(f"Quest selesai! Mendapat +{xp} XP")
        else:
            st.info("Quest belum selesai.")

        st.session_state.step = "input_aktivitas"
        st.rerun()

# --- STEP 7: RINGKASAN AKHIR ---
elif st.session_state.step == "ringkasan":
    st.markdown("##### RINGKASAN BELAJAR")
    st.write(f"Nama: {st.session_state.nama} Fakultas: {st.session_state.fakultas}")
    st.write(f"Quest selesai: {st.session_state.jumlah_quest_selesai}")
    st.write(f"Total waktu belajar: {st.session_state.total_menit} menit")
    st.write(f"Total XP: {st.session_state.total_xp}")
    st.markdown("Terima kasih sudah menggunakan CampusQuest!")