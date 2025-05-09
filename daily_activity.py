import streamlit as st
import pandas as pd
import os
from datetime import datetime
import base64

def set_background(image_file_path):
    with open(image_file_path, 'rb') as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode()

    css_code = f""" 
    <style>
    .stApp {{ 
        background-image: url("data:image/png;base64,{encoded_string}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """
    
    st.markdown(css_code, unsafe_allow_html=True)

set_background('9161244.png')

# Path file CSV
file_path = "activity.csv"

# 11/04/2025
def remove_empty_rows(file_path):
    try:
        df = pd.read_csv(file_path, delimiter=";")
        df_clean = df.dropna(how='all')  # Hapus baris yang semua kolomnya kosong
        df_clean.to_csv(file_path, sep=";", index=False)
    except Exception as e:
        st.error(f"Tidak ada baris data yang kosong: {e}")
# 11/04/2025

def get_day_name(date):
    hari_dict = {
        "Monday": "Senin",
        "Tuesday": "Selasa",
        "Wednesday": "Rabu",
        "Thursday": "Kamis",
        "Friday": "Jum'at",
        "Saturday": "Sabtu",
        "Sunday": "Minggu"
    }
    return hari_dict[date.strftime("%A")]

def form_callback(date, day, bangun, tidur, ibadah, olahraga, belajar, makan, bermasyarakat):
    file_exists = os.path.exists(file_path)
    
    if not file_exists:
        with open(file_path, 'w') as f:
            f.write("Tanggal;Hari;Bangun;Tidur;Ibadah;Olahraga;Belajar;Makan;Bermasyarakat\n")

    with open(file_path, 'a') as f:
        f.write(f"{date};{day};{bangun};{tidur};{ibadah};{olahraga};{belajar};{makan};{bermasyarakat}\n")
    
    # 11/04/2025
    remove_empty_rows(file_path)
    # 11/04/2025

with st.form(key="my_form", clear_on_submit=True):
    st.subheader("Aktivitas Harian")
    
    today = datetime.today().date()
    date_input = st.date_input('Tanggal', value=today, max_value=today)
    
    day_input = get_day_name(date_input)
    
    if "wake_hour" not in st.session_state:
        st.session_state["wake_hour"] = 0
    if "wake_minute" not in st.session_state:
        st.session_state["wake_minute"] = 0
    
    if "sleep_hour" not in st.session_state:
        st.session_state["sleep_hour"] = 0
    if "sleep_minute" not in st.session_state:
        st.session_state["sleep_minute"] = 0
        
    st.write("Waktu Bangun")
    col1, col2 = st.columns(2)

    with col1:
        wake_hour = st.selectbox("Jam", list(range(0, 9)), index=st.session_state["wake_hour"], key="wake_hour")

    with col2:
        wake_minute = st.selectbox("Menit", list(range(0, 60)), index=st.session_state["wake_minute"], key="wake_minute")

    wake_input = f"{wake_hour:02d}:{wake_minute:02d}"

    st.write("Waktu Tidur")
    
    col1, col2 = st.columns(2)

    with col1:
        sleep_hour = st.selectbox("Jam", list(range(0, 24)), index=st.session_state["sleep_hour"], key="sleep_hour")
    
    with col2:
        sleep_minute = st.selectbox("Menit", list(range(0, 60)), index=st.session_state["sleep_minute"], key="sleep_minute")

    sleep_input = f"{sleep_hour:02d}:{sleep_minute:02d}"
        
    # Input Aktivitas Ibadah
    st.write('**Sholat:**')
    
    # Using a list to store selected prayers
    ibadah_list = []
    
    sholat_labels = ["Subuh", "Dhuhur", "Ashar", "Maghrib", "Isya"]
    col = st.columns(len(sholat_labels))  # Membuat 5 kolom sesuai jumlah checkbox

    for i, label in enumerate(sholat_labels):
        with col[i]:
            if st.checkbox(label, key=f"ibadah_{label}", label_visibility="visible"):
                ibadah_list.append(label)
    
    ibadah_input = ','.join(ibadah_list)

    olahraga_input = st.text_input('Olahraga', key='olahraga')
    belajar_input = st.text_input('Belajar', key='belajar')
    makan_input = st.text_input('Makan Sehat & Bergizi', key='makan')
    bermasyarakat_input = st.text_input('Bermasyarakat', key='bermasyarakat')

    submitted = st.form_submit_button("Submit")
    if submitted:
        tanggal_input = date_input.strftime("%d-%m-%Y")
        bangun_input = wake_input
        tidur_input = sleep_input
        
        output = f"""
        Aktivitas
        Tanggal: {tanggal_input}
        Hari: {day_input} 
        Bangun Pagi. Aku bangun pukul: {bangun_input}
        Beribadah. Sholat: {ibadah_input} 
        Berolahraga. Olahraga hari ini adalah: {olahraga_input} 
        Gemar belajar. Hari ini aku belajar: {belajar_input} 
        Makan Sehat & Bergizi. Salah satu menu makananku hari ini adalah : {makan_input} 
        Bermasyarakat. Hari ini aku melakukan aktivitas: {bermasyarakat_input}
        Istirahat cukup. Aku tidur malam pukul: {tidur_input}
        """
        
        st.text(output)
                
        # Call function with correct number of arguments
        form_callback(tanggal_input, day_input, bangun_input, tidur_input, ibadah_input, olahraga_input, belajar_input, makan_input, bermasyarakat_input)

# Display CSV Contents
st.info("#### List Daily 7 habits")

if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
    # 11/04/2025
    remove_empty_rows(file_path)  # bersihkan dulu sebelum ditampilkan
    # 11/04/2025
    
    df = pd.read_csv(file_path, delimiter=";")
    
    # Editable dataframe
    edited_df = st.data_editor(df, num_rows="dynamic")

    # Tombol Simpan Perubahan
    if st.button("Simpan Perubahan"):
        edited_df.to_csv(file_path, sep=";", index=False)
        st.success("✅ Perubahan berhasil disimpan!")
    #st.dataframe(df.set_index(df.columns[0]), height=300)
else:
    st.warning("⚠️ The file is empty or does not exist.")
