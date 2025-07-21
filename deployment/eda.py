import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
from PIL import Image


def run():
    # Title and Subheader
    st.title('Heart Failure Mortality Prediction')
    st.subheader('Page ini mengenai EDA dari dataset Heart Failure Clinical Records')

    # Menambahkan Gambar 
    image = Image.open('./src/hearthfailure.jpeg')
    st.image(image, caption='Heart Failure')

    # Menambahkan Teks
    st.write('Page ini dibuat oleh *Fadhola Asandi*')
    st.write('# Exploratory Data Analysis (EDA)')

    # Load DataFrame
    DATA_URL = (
        'https://archive.ics.uci.edu/ml/machine-learning-databases/00519/heart_failure_clinical_records_dataset.csv'
    )
    df = pd.read_csv(DATA_URL)
    st.dataframe(df)

    # 1. Bagaimana pola distribusi umur pasien dan dan platelets, apakah banyak lansia? dan apakah platelets/trombosit pasien normal?
    st.write('## 1. Bagaimana pola distribusi umur pasien dan dan platelets, apakah banyak lansia? dan apakah platelets/trombosit pasien normal?')
    fig1, axs1 = plt.subplots(1, 2, figsize=(14, 5))
    sns.histplot(df['age'], kde=True, ax=axs1[0])
    axs1[0].set_title('Distribusi Umur Pasien')
    sns.histplot(df['platelets'], kde=True, ax=axs1[1])
    axs1[1].set_title('Distribusi Platelets')
    st.pyplot(fig1)

    # 2. Bagaimana pola distribusi kadar serum_creatinine dalam darah pasien dan tingkat serum_sodium dalam darah pasien, apakah normal?
    st.write('## 2. Bagaimana pola distribusi kadar serum_creatinine dalam darah pasien dan tingkat serum_sodium dalam darah pasien, apakah normal?')
    fig2, axs2 = plt.subplots(1, 2, figsize=(14, 5))
    sns.histplot(df['serum_creatinine'], kde=True, ax=axs2[0])
    axs2[0].set_title('Serum Creatinine')
    sns.histplot(df['serum_sodium'], kde=True, ax=axs2[1])
    axs2[1].set_title('Serum Sodium')
    st.pyplot(fig2)

       # 3. Kelompok jenis kelamin mana yang lebih banyak mengalami `anaemia`, `diabetes`, `high_blood_pressure`, dan `smoking`?
    st.write('## 3. Kelompok jenis kelamin mana yang lebih banyak mengalami `anaemia`, `diabetes`, `high_blood_pressure`, dan `smoking`?')
    option3 = st.selectbox(
        'Pilih kondisi untuk ditampilkan (per jenis kelamin):',
        ['anaemia', 'diabetes', 'high_blood_pressure', 'smoking']
    )
    fig3 = plt.figure(figsize=(6, 4))
    sns.countplot(x=option3, data=df, hue='sex')
    plt.title(f'{option3.capitalize()} per Jenis Kelamin')
    st.pyplot(fig3)

    # 4. Bagaimana pengaruh kondisi kesehatan dan jenis kelamin terhadap kematian 
    st.write('## 4. Bagaimana pengaruh kondisi kesehatan dan jenis kelamin terhadap kematian ')
    option4 = st.selectbox(
        'Pilih variabel untuk analisis kematian:',
        ['anaemia', 'diabetes', 'high_blood_pressure', 'sex', 'smoking']
    )
    fig4 = plt.figure(figsize=(6, 4))
    sns.barplot(x=option4, y='DEATH_EVENT', data=df)
    plt.title(f'Kematian Berdasarkan {option4.capitalize()}')
    st.pyplot(fig4)

    # 5. Bagaimana distribusi `serum_creatinine`, `age`, `platelets`, `ejection_fraction`, `creatinine_phosphokinase`, `serum_sodium` berdasarkan status kematian 
    st.write('## 5. Bagaimana distribusi `serum_creatinine`, `age`, `platelets`, `ejection_fraction`, `creatinine_phosphokinase`, `serum_sodium` berdasarkan status kematian ')
    features = ['age', 'ejection_fraction', 'creatinine_phosphokinase',
                'serum_creatinine', 'serum_sodium', 'platelets', 'time']
    option5 = st.selectbox(
        'Pilih fitur numerik untuk boxplot vs DEATH_EVENT:',
        features
    )
    fig5 = plt.figure(figsize=(6, 4))
    sns.boxplot(x='DEATH_EVENT', y=option5, data=df)
    plt.title(f'Kematian Berdasarkan {option5.capitalize()}')
    st.pyplot(fig5)

    # 6. Distribusi Waktu Follow-up
    st.write('## 6. Distribusi Waktu Follow-up')
    fig6 = plt.figure(figsize=(14, 5))
    sns.histplot(data=df, x='time', hue='DEATH_EVENT', kde=True)
    plt.title('Follow-up Time & Kematian')
    st.pyplot(fig6)

    # 7. Jumlah Kondisi vs Risiko Kematian
    st.write('## 7. Jumlah Kondisi Kesehatan vs Tingkat Kematian')
    df['risk_count'] = df[['anaemia', 'diabetes', 'high_blood_pressure', 'smoking']].sum(axis=1)
    fig7 = plt.figure(figsize=(10, 5))
    sns.barplot(x='risk_count', y='DEATH_EVENT', data=df)
    plt.title('Jumlah Risiko vs Kematian')
    plt.xlabel('Jumlah Kondisi Risiko')
    st.pyplot(fig7)


if __name__ == '__main__':
    run()
