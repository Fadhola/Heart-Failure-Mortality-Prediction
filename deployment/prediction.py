import streamlit as st
import pickle
import pandas as pd

# Load model
with open('./src/model.pkl', 'rb') as f:
    model = pickle.load(f)

def run():
# Title
    st.title('Heart Failure Mortality Prediction')
    st.subheader('Masukkan data klinis pasien untuk memprediksi risiko kematian')
# Form input
    with st.form(key='heart-failure-form'):
        age = st.number_input('Umur (tahun)', min_value=40, max_value=95, value=60, step=1)
        sex = st.radio('Jenis Kelamin - Perempuan (0)' 'Pria (1)', (0,1))
        anaemia = st.radio('Anaemia - Tidak (0)' 'Ya (1)', (0,1))
        high_blood_pressure = st.radio('Hipertensi - Tidak (0)' 'Ya (1)', (0,1))
        diabetes = st.radio('Diabetes - Tidak (0)' 'Ya (1)', (0,1))
        smoking = st.radio('Merokok - Tidak (0)' 'Ya (1)', (0,1))
        ejection_fraction = st.number_input('Ejection Fraction (%) normal 50% - 70%', min_value=14, max_value=80, value=50, step=1)
        platelets = st.number_input('Platelets (mcL) noemal 150.000 - 450.000/mcL', min_value=47000.0, max_value=604750.0, value=250000.0, step=1000.0)
        serum_creatinine = st.number_input('Serum Creatinine (mg/dL) Normal pria: 0.7 - 1.3 mg/dL. Wanita: 0.6 - 1.1 mg/dL.', min_value=0.5, max_value=3.7, value=1.0, step=0.1)
        serum_sodium = st.number_input('Serum Sodium (mEq/L) normal 135 - 145 mEq/L', min_value=118.25, value=146.0, step=1.0)
        creatinine_phosphokinase = st.number_input('Creatinine Phosphokinase (mcg/L) normal 10 - 120 mcg/L', min_value=23, max_value=1967, value=100, step=10)
        time = st.number_input('Waktu Follow-up (hari)', min_value=4, max_value=285, value=100, step=1)
        submitted = st.form_submit_button('Predict')

    # When submitted
    if submitted:
        # Construct DataFrame for prediction
        data_inf = pd.DataFrame([{
            'age': age,
            'anaemia': anaemia,
            'creatinine_phosphokinase': creatinine_phosphokinase,
            'diabetes': diabetes,
            'ejection_fraction': ejection_fraction,
            'high_blood_pressure': high_blood_pressure,
            'platelets': platelets,
            'serum_creatinine': serum_creatinine,
            'serum_sodium': serum_sodium,
            'sex': sex,
            'smoking': smoking,
            'time': time,
        }])

        # Predict probability of death_event = 1
        proba = model.predict_proba(data_inf)[0][1]
        st.write(f'**Probabilitas Risiko Kematian:** {proba:.2f}')

        # Interpretasi
        if proba >= 0.7:
            st.error('Status: Berisiko Tinggi')
            st.write('**Tindakan:** Segera bawa pasien ke rumah sakit atau klinik yang memiliki fasilitas perawatan jantung (ICCU/CCU) untuk evaluasi dan penanganan intensif.')
        elif proba >= 0.4:
            st.warning('Status: Risiko Sedang')
            st.write('**Tindakan:** Disarankan konsultasi medis lebih lanjut untuk evaluasi menyeluruh, mulai modifikasi gaya hidup dan cek rutin.')
        else:
            st.success('Status: Tidak Berisiko Tinggi/Tidak berisiko jika 0')
            st.write('**Tindakan:** Berikan edukasi pentingnya kontrol rutin dan mengenali gejala awal gagal jantung.')
if __name__ == '__main__':
    run()