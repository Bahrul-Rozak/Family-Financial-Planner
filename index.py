import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Family Financial Planner",
    layout="wide",
    page_icon="💰"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        max-width: 1200px;
        padding: 2rem;
    }
    .header {
        color: #2e86ab;
        border-bottom: 2px solid #f18f01;
        padding-bottom: 0.5rem;
        margin-bottom: 1.5rem;
    }
    .section {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .category-card {
        background-color: white;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .summary-card {
        background-color: #e9f5ff;
        border-left: 4px solid #2e86ab;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .positive {
        color: #28a745;
        font-weight: bold;
    }
    .negative {
        color: #dc3545;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# App title
st.markdown("<h1 class='header'>Family Financial Planner</h1>", unsafe_allow_html=True)

# Main columns layout
col1, col2 = st.columns([2, 1])

with col1:
    # Income input section
    with st.container():
        st.subheader("💰 Pendapatan Bulanan")
        gaji = st.number_input(
            "Masukkan total gaji bulanan (Rp)",
            min_value=0,
            value=50000000,
            step=1000000,
            format="%d"
        )

# Function to create category input cards
def kategori_input(nama_kategori, default_items, key_prefix):
    with st.expander(f"📌 {nama_kategori}", expanded=True):
        use_default = st.checkbox(
            f"Gunakan nilai default untuk {nama_kategori}?",
            value=True,
            key=f"default_{key_prefix}"
        )
        
        items = {}
        if use_default:
            for item, default_val in default_items.items():
                st.write(f"▪️ {item}: Rp {default_val:,}")
                items[item] = default_val
        else:
            for item, default_val in default_items.items():
                val = st.number_input(
                    f"{item} (Rp)",
                    min_value=0,
                    value=default_val,
                    step=100000,
                    key=f"{key_prefix}_{item}",
                    format="%d"
                )
                items[item] = val
        return items

# Default values for categories
kebutuhan_pokok_default = {
    "Cicilan KPR / Sewa Rumah": 6000000,
    "Listrik": 800000,
    "Air": 300000,
    "Internet & TV Kabel": 600000,
    "Makanan Pokok & Dapur": 5500000,
    "Makan di Luar / Pesan Antar": 1500000
}

transportasi_default = {
    "BBM / Transport Umum": 1200000,
    "Perawatan Kendaraan": 300000
}

perawatan_ratna_default = {
    "Skincare & Kosmetik": 1500000,
    "Perawatan Rambut & Tubuh": 500000
}

kesehatan_asuransi_default = {
    "Asuransi Kesehatan": 1200000,
    "Obat-obatan & Check-up": 600000
}

rumah_tangga_default = {
    "Kebersihan & Peralatan": 500000,
    "Perawatan & Perbaikan Rumah": 300000
}

pendidikan_anak_default = {
    "Tabungan Pendidikan Anak": 2000000
}

gaya_hidup_default = {
    "Jalan-jalan & Nongkrong": 3000000,
    "Hobi & Olahraga": 1000000
}

sedekah_default = {
    "Sedekah & Amal": 2500000
}

# Expense categories in the main column
with col1:
    with st.container():
        st.subheader("📋 Kategori Pengeluaran")
        
        # Using columns for better organization
        cols = st.columns(2)
        
        with cols[0]:
            kebutuhan_pokok = kategori_input("1. Kebutuhan Pokok", kebutuhan_pokok_default, "pokok")
            transportasi = kategori_input("2. Transportasi", transportasi_default, "transport")
            perawatan_ratna = kategori_input("3. Perawatan Ratna", perawatan_ratna_default, "ratna")
            kesehatan_asuransi = kategori_input("4. Kesehatan & Asuransi", kesehatan_asuransi_default, "kesehatan")
        
        with cols[1]:
            rumah_tangga = kategori_input("5. Kebutuhan Rumah Tangga", rumah_tangga_default, "rumah")
            pendidikan_anak = kategori_input("6. Pendidikan Anak", pendidikan_anak_default, "pendidikan")
            gaya_hidup = kategori_input("7. Gaya Hidup & Hiburan", gaya_hidup_default, "gaya")
            sedekah = kategori_input("8. Sedekah & Amal", sedekah_default, "sedekah")

# Savings and investments in the sidebar
with col2:
    with st.container():
        st.subheader("💵 Tabungan & Investasi")
        
        with st.expander("Tabungan & Investasi", expanded=True):
            use_default_tabungan = st.checkbox(
                "Gunakan nilai default?",
                value=True,
                key="tabungan_investasi"
            )
            if use_default_tabungan:
                tabungan_rumah = 8000000
                tabungan_pensiun = 3000000
                investasi_lain = 4000000
                st.write(f"▪️ Tabungan Rumah: Rp {tabungan_rumah:,}")
                st.write(f"▪️ Tabungan Pensiun: Rp {tabungan_pensiun:,}")
                st.write(f"▪️ Investasi Lainnya: Rp {investasi_lain:,}")
            else:
                tabungan_rumah = st.number_input(
                    "Tabungan Rumah (Rp)",
                    min_value=0,
                    value=8000000,
                    step=100000,
                    key="tabungan_rumah",
                    format="%d"
                )
                tabungan_pensiun = st.number_input(
                    "Tabungan Pensiun (Rp)",
                    min_value=0,
                    value=3000000,
                    step=100000,
                    key="tabungan_pensiun",
                    format="%d"
                )
                investasi_lain = st.number_input(
                    "Investasi Lainnya (Rp)",
                    min_value=0,
                    value=4000000,
                    step=100000,
                    key="investasi_lain",
                    format="%d"
                )

        with st.expander("Dana Darurat", expanded=True):
            use_default_dana_darurat = st.checkbox(
                "Gunakan nilai default?",
                value=True,
                key="dana_darurat"
            )
            if use_default_dana_darurat:
                dana_darurat = 5000000
                st.write(f"▪️ Dana Darurat: Rp {dana_darurat:,}")
            else:
                dana_darurat = st.number_input(
                    "Dana Darurat (Rp)",
                    min_value=0,
                    value=5000000,
                    step=100000,
                    key="dana_darurat",
                    format="%d"
                )

        with st.expander("Tabungan Mobil", expanded=True):
            target_mobil = st.number_input(
                "Target Total Tabungan Mobil (Rp)",
                min_value=0,
                value=100000000,
                step=10000000,
                format="%d"
            )
            waktu_mobil_bulan = st.number_input(
                "Waktu Nabung Mobil (bulan)",
                min_value=1,
                value=24
            )
            tabungan_mobil_bulanan = target_mobil / waktu_mobil_bulan if waktu_mobil_bulan > 0 else 0
            st.write(f"▪️ Tabungan Bulanan: Rp {tabungan_mobil_bulanan:,.0f}")

# Calculation functions
def total_kategori(kategori_dict):
    return sum(kategori_dict.values())

# Calculate totals
total_kebutuhan_pokok = total_kategori(kebutuhan_pokok)
total_transportasi = total_kategori(transportasi)
total_perawatan_ratna = total_kategori(perawatan_ratna)
total_kesehatan_asuransi = total_kategori(kesehatan_asuransi)
total_rumah_tangga = total_kategori(rumah_tangga)
total_pendidikan_anak = total_kategori(pendidikan_anak)
total_gaya_hidup = total_kategori(gaya_hidup)
total_sedekah = total_kategori(sedekah)

total_tabungan_investasi = tabungan_rumah + tabungan_pensiun + investasi_lain
total_pengeluaran = (
    total_kebutuhan_pokok + total_transportasi + total_perawatan_ratna +
    total_kesehatan_asuransi + total_rumah_tangga + total_pendidikan_anak +
    total_gaya_hidup + total_sedekah + total_tabungan_investasi +
    dana_darurat + tabungan_mobil_bulanan
)

sisa_gaji = gaji - total_pengeluaran

# Summary section
st.markdown("---")
st.markdown("<h2 class='header'>📊 Ringkasan Keuangan</h2>", unsafe_allow_html=True)

summary_cols = st.columns([2, 1])

with summary_cols[0]:
    # Summary table
    summary = {
        "Kebutuhan Pokok": total_kebutuhan_pokok,
        "Transportasi": total_transportasi,
        "Perawatan Ratna": total_perawatan_ratna,
        "Kesehatan & Asuransi": total_kesehatan_asuransi,
        "Kebutuhan Rumah Tangga": total_rumah_tangga,
        "Pendidikan Anak": total_pendidikan_anak,
        "Gaya Hidup & Hiburan": total_gaya_hidup,
        "Sedekah & Amal": total_sedekah,
        "Tabungan & Investasi": total_tabungan_investasi,
        "Dana Darurat": dana_darurat,
        "Tabungan Mobil": tabungan_mobil_bulanan
    }

    df_summary = pd.DataFrame.from_dict(summary, orient='index', columns=['Amount'])
    df_summary['Percentage'] = (df_summary['Amount'] / gaji * 100).round(1)
    df_summary['Amount'] = df_summary['Amount'].apply(lambda x: f"Rp {x:,.0f}")
    df_summary['Percentage'] = df_summary['Percentage'].apply(lambda x: f"{x}%")
    
    st.dataframe(
        df_summary,
        use_container_width=True,
        column_config={
            "index": st.column_config.Column("Kategori", width="medium"),
            "Amount": st.column_config.Column("Jumlah", width="medium"),
            "Percentage": st.column_config.Column("Persentase", width="small")
        }
    )

with summary_cols[1]:
    # Financial summary card
    st.markdown(f"""
    <div class='summary-card'>
        <h4>Ringkasan Bulanan</h4>
        <p><strong>Total Pendapatan:</strong> Rp {gaji:,.0f}</p>
        <p><strong>Total Pengeluaran:</strong> Rp {total_pengeluaran:,.0f}</p>
        <p><strong>Sisa Gaji:</strong> <span class={'positive' if sisa_gaji >= 0 else 'negative'}>Rp {sisa_gaji:,.0f}</span></p>
    </div>
    """, unsafe_allow_html=True)

    if sisa_gaji < 0:
        st.error("⚠️ Pengeluaran melebihi gaji! Kurangi pengeluaran atau tingkatkan pendapatan.")
    else:
        st.success("✅ Alokasi pengeluaran sudah sesuai dengan gaji bulanan.")

# Visualization section
st.markdown("---")
st.markdown("<h2 class='header'>📈 Visualisasi Alokasi Keuangan</h2>", unsafe_allow_html=True)

viz_cols = st.columns(2)

with viz_cols[0]:
    # Pie chart
    st.subheader("Persentase Pengeluaran")
    fig = px.pie(
        names=list(summary.keys()),
        values=list(summary.values()),
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with viz_cols[1]:
    # Bar chart
    st.subheader("Perbandingan Kategori")
    fig = px.bar(
        x=list(summary.values()),
        y=list(summary.keys()),
        orientation='h',
        text=[f"Rp {x:,.0f}" for x in summary.values()],
        color=list(summary.keys()),
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_layout(showlegend=False, xaxis_title="Amount (Rp)", yaxis_title="Category")
    st.plotly_chart(fig, use_container_width=True)

# Tips section
st.markdown("---")
st.markdown("<h2 class='header'>💡 Tips Manajemen Keuangan</h2>", unsafe_allow_html=True)

tips = [
    "✅ Selalu alokasikan minimal 10% pendapatan untuk tabungan darurat",
    "✅ Prioritaskan pembayaran utang dengan bunga tinggi terlebih dahulu",
    "✅ Gunakan aturan 50-30-20 (50% kebutuhan, 30% keinginan, 20% tabungan)",
    "✅ Tinjau pengeluaran bulanan secara berkala dan sesuaikan dengan kebutuhan",
    "✅ Manfaatkan aplikasi budgeting untuk memantau pengeluaran harian"
]

for tip in tips:
    st.markdown(f"- {tip}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6c757d; font-size: 0.9rem;">
    <p>Family Financial Planner v1.0 • © 2025</p>
</div>
""", unsafe_allow_html=True)