"""
Aplikasi Streamlit untuk menggambarkan statistik penumpang TransJakarta

Sumber data berasal dari Jakarta Open Data
Referensi API Streamlit: https://docs.streamlit.io/library/api-reference
"""

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import streamlit as st
import json

st.set_page_config(layout="wide",page_icon="valorant.png")
logo1,kosong,logo2 = st.columns((1,2,1))
logo1.image("logo_itb_1024.png", width=150)
kosong.header("UAS Pemrogramman Komputer 12220057")
logo2.image("patra.png", width=150)
st.title("Data Produksi Minyak Berbagai Negara")

###membaca data csv dan menyesuaikan dengan file json, mengeluarkan data yg tidak ada di json###
df = pd.read_csv('produksi_minyak_mentah.csv')
df_clean = df.set_index('kode_negara')
df_clean.head()

df_clean = df_clean.drop(['WLD','G20','OEU','EU28','OECD'])
df_clean.reset_index(drop=False,inplace=True)


kode_negara = list(df['kode_negara'].unique())#membuat kode negara unik
#print(f"Kode: {kode_negara}")
total_produksi = []
for kode in kode_negara:
    jumlah_produksi = df[df['kode_negara']==kode]['produksi'].replace(",", "").astype(int)
    total_produksi.append(jumlah_produksi.sum())
#print(f"Total Produksi: {total_produksi}")


file_json = pd.read_json('kode_negara_lengkap.json')
df_json = pd.DataFrame.from_dict(file_json)

selain_negara = []#memasukkan data yang tidak ada di json ke dalam list baru selain negara
kode_negara = list(df['kode_negara'].unique())
for i in kode_negara:
    if i not in list(df_json['alpha-3']):
        selain_negara.append(i)

for i in selain_negara:
    df = df[df.kode_negara != i]
    if i in kode_negara:
        kode_negara.remove(i)

nama_negara = []
kode_angka = []
region_json = []
subregion_json = []
for i in range(len(kode_negara)):
    for j in range(len(list(df_json['alpha-3']))):
        if list(df_json['alpha-3'])[j] == kode_negara[i] and list(df_json['name'])[j] not in nama_negara:
            nama_negara.append(list(df_json['name'])[j])
            kode_angka.append(list(df_json['country-code'])[j])
            region_json.append(list(df_json['region'])[j])
            subregion_json.append(list(df_json['sub-region'])[j])

df_lengkap = pd.DataFrame(list(zip(nama_negara, kode_negara, kode_angka, region_json, subregion_json)), columns=['negara', 'alpha-3', 'kode negara', 'region', 'sub-region'])

## User inputs on the control panel
pilihan1, pilihan2,pilihan3 = st.columns((2,1,1))
judul1, judul2 = st.columns(2)
grafik1,grafik2 = st.columns((1,1))

N = pilihan1.selectbox("Pilih Negara", nama_negara)
judul1.subheader("Produksi Negara "+str(N)+ " Pada seluruh tahun") 

kodenegarahuruf = []
for i in range(len(nama_negara)):
    if nama_negara[i] == N:
        kodenegarahuruf = kode_negara[i]
        kodenegaraangka = kode_angka[i]
        region = region_json[i]
        subregion = subregion_json[i]

# Membuat list baru untuk menampung data produksi negara dan tahunnya
list_produksi = []
list_tahun = []

# Mengambil data produksi dan tahun berdasarkan N yang dipilih dan memasukkannya
for i in range(len(list(df_clean['kode_negara']))):
    if kodenegarahuruf == list(df_clean['kode_negara'])[i]:
        list_produksi.append(list(df_clean['produksi'])[i])
        list_tahun.append(list(df_clean['tahun'])[i])

fig1, ax = plt.subplots()
ax.plot(list_tahun,list_produksi),ax.set_xlabel('Tahun'),ax.set_ylabel('Produksi'),plt.show()
grafik1.pyplot(fig1)

###persoalan b###
T = pilihan2.selectbox("Tahun ", list_tahun)

gambar, pilihan = st.columns((0.5,1))


df_nomer2 = df_clean.loc[df_clean['tahun'] ==T].sort_values(by=['produksi'], ascending=False)

nama_df2 = []
for i in range(len(list(df_nomer2['kode_negara']))):
    for j in range(len(list(df_lengkap['alpha-3']))):
        if list(df_nomer2['kode_negara'])[i] == list(df_lengkap['alpha-3'])[j]:
            nama_df2.append(list(df_lengkap['negara'])[j])

df_nomer2['negara'] = nama_df2

B1 = int(pilihan3.number_input("Jumlah Negara Ditampilkan ",min_value=1, max_value=None,value=10))
df_nomer2 = df_nomer2[:B1]

judul2.subheader("Grafik Produksi Sejumlah Negara Pada Tahun "+str(T))
fig2,ax2 = plt.subplots()
ax2.barh(df_nomer2['negara'],df_nomer2['produksi'])
grafik2.pyplot(fig2)
############### persoalan c ###############

B2 = st.number_input("Jumlah Negara ",min_value=1,max_value=None,value=10,key="kumulatif")
produksi_kumulatif = []

for i in kode_negara:
    n = df_clean.loc[df_clean['kode_negara']==i,'produksi'].sum()
    produksi_kumulatif.append(n)

df_nomer3 = pd.DataFrame(list(zip(kode_negara,produksi_kumulatif)),columns =['kode_negara','produksi_kumulatif']).sort_values(by=['produksi_kumulatif'], ascending=False)
df_nomer3 = df_nomer3[:B2]

negara3 = df_nomer3['kode_negara']
produksi_nomer3 = df_nomer3['produksi_kumulatif']

st.subheader("Sejumlah Negara dengan Produksi Kumulatif tertinggi")
fig3,ax3 = plt.subplots()
ax3.pie(df_nomer3['produksi_kumulatif'],labels=df_nomer3['kode_negara'])
st.pyplot(fig3)
############### nomer 4 ###############
###Produksi Terbesar pada tahunnya dan kumulatif
st.title("Informasi")
#produksi minyak terbesar pada tahunnya
df_nomer4 = df_clean[df_clean['tahun']==T].sort_values(by=['produksi'],ascending=False).head(1).to_numpy()
st.subheader("Negara Produksi Minyak Terbesar pada tahun "+str(T))
st.write(df_nomer4[0][0], df_nomer4[0][2])
df_nomer4lagi = df_lengkap[df_lengkap['alpha-3'] == df_nomer4[0][0]].head(1).to_numpy()
st.write(df_nomer4lagi[0][0],df_nomer4lagi[0][1],df_nomer4lagi[0][2],df_nomer4lagi[0][3],df_nomer4lagi[0][4])
#produksi minyak terbesar
produksiminyakterbesar = df_clean[df_clean['produksi'] == df_clean['produksi'].max()].to_numpy()
st.subheader("Negara Produksi Minyak Terbesar Pada Keseluruhan Tahun")
st.write(produksiminyakterbesar[0][0], produksiminyakterbesar[0][2])
produksiminyakterbesardetail = df_lengkap[df_lengkap['alpha-3'] == produksiminyakterbesar[0][0]].to_numpy()
st.write(produksiminyakterbesardetail[0][0],produksiminyakterbesardetail[0][1],produksiminyakterbesardetail[0][2],produksiminyakterbesardetail[0][3],produksiminyakterbesardetail[0][4])

###Produksi Terkecil Kumulatif !=0
df_4coba = pd.DataFrame(list(zip(kode_negara,nama_negara,produksi_kumulatif,region_json,subregion_json)),columns =['kode_negara','nama_negara','produksi_kumulatif','region','subregion']).sort_values(by=['produksi_kumulatif'], ascending=True)
df_4 = df_4coba[df_4coba['produksi_kumulatif'] != 0]
df_4 = df_4[['kode_negara','nama_negara','produksi_kumulatif','region','subregion']]
terkecil_kumulatif = df_4[df_4['produksi_kumulatif']==df_4['produksi_kumulatif'].min()]
st.subheader("Negara dengan Produksi Kumulatif Terkecil")
st.write(terkecil_kumulatif)

##Produksi Kumulatif = 0
df_4nol = df_4coba[df_4coba['produksi_kumulatif'] == 0]
df_4nol = df_4nol[['kode_negara','nama_negara','produksi_kumulatif','region','subregion']]
nol = df_4nol[df_4nol['produksi_kumulatif']==df_4nol['produksi_kumulatif']]
st.subheader("Negara dengan Jumlah Produksi samadengan 0")
st.write(nol)







