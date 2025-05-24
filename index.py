import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from io import BytesIO
import calendar
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Family Financial Planner",
    layout="wide",
    page_icon="💰",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced styling
st.markdown("""
    <style>
    :root {
        --primary: #2e86ab;
        --secondary: #f18f01;
        --success: #28a745;
        --danger: #dc3545;
    }
    .main {
        max-width: 1400px;
        padding: 2rem;
    }
    .header {
        color: var(--primary);
        border-bottom: 3px solid var(--secondary);
        padding-bottom: 0.5rem;
        margin-bottom: 1.5rem;
    }
    .section {
        background-color: #f8f9fa;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    .category-card {
        background-color: white;
        border-radius: 10px;
        padding: 1.2rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        transition: transform 0.2s;
    }
    .category-card:hover {
        transform: translateY(-2px);
    }
    .summary-card {
        background-color: #e9f5ff;
        border-left: 5px solid var(--primary);
        padding: 1.2rem;
        margin-bottom: 1.2rem;
    }
    .positive {
        color: var(--success);
        font-weight: bold;
    }
    .negative {
        color: var(--danger);
        font-weight: bold;
    }
    .stProgress > div > div > div > div {
        background-color: var(--primary);
    }
    .st-b7 {
        color: var(--primary) !important;
    }
    .stButton button {
        background-color: var(--primary);
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
    }
    .stButton button:hover {
        background-color: #1a6a8a;
        color: white;
    }
    .stDownloadButton button {
        background-color: var(--success);
        color: white;
    }
    .stDownloadButton button:hover {
        background-color: #218838;
        color: white;
    }
    .stExpander {
        border-radius: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# App title with emoji
st.markdown("<h1 class='header'>🚀 Ultimate Family Financial Planner</h1>", unsafe_allow_html=True)

# ===========================================
# NEW FEATURE 1: Multi-Month Planning
# ===========================================
with st.sidebar:
    st.subheader("📅 Rentang Perencanaan")
    planning_months = st.slider(
        "Jumlah Bulan untuk Perencanaan", 
        min_value=1, 
        max_value=36, 
        value=12,
        help="Pilih berapa bulan ke depan untuk perencanaan keuangan"
    )
    
    # NEW FEATURE 2: Income Growth Projection
    st.subheader("📈 Proyeksi Pendapatan")
    income_growth = st.number_input(
        "Pertumbuhan Pendapatan Bulanan (%)", 
        min_value=0.0, 
        max_value=50.0, 
        value=5.0,
        step=0.5,
        format="%.1f"
    ) / 100

# Main columns layout
col1, col2 = st.columns([2, 1])

with col1:
    # Income input section with enhancements
    with st.container():
        st.subheader("💰 Pendapatan Bulanan")
        gaji = st.number_input(
            "Masukkan total gaji bulanan (Rp)",
            min_value=0,
            value=50000000,
            step=1000000,
            format="%d"
        )
        
        # NEW FEATURE 3: Additional Income Sources
        with st.expander("➕ Sumber Pendapatan Lainnya", expanded=False):
            bonus = st.number_input("Bonus/Tunjangan (Rp)", min_value=0, value=0, step=100000, format="%d")
            pendapatan_lain = st.number_input("Pendapatan Lainnya (Rp)", min_value=0, value=0, step=100000, format="%d")
            gaji_total = gaji + bonus + pendapatan_lain
            st.metric("Total Pendapatan Bulanan", f"Rp {gaji_total:,}")

# Enhanced category input function with saving capability
# def kategori_input(nama_kategori, default_items, key_prefix):
#     with st.expander(f"📌 {nama_kategori}", expanded=True):
#         col1, col2 = st.columns([3,1])
#         with col1:
#             use_default = st.checkbox(
#                 f"Gunakan nilai default untuk {nama_kategori}?",
#                 value=True,
#                 key=f"default_{key_prefix}"
#             )
        
#         items = {}
#         if use_default:
#             for item, default_val in default_items.items():
#                 st.write(f"▪️ {item}: Rp {default_val:,}")
#                 items[item] = default_val
#         else:
#             for item, default_val in default_items.items():
#                 val = st.number_input(
#                     f"{item} (Rp)",
#                     min_value=0,
#                     value=default_val,
#                     step=100000,
#                     key=f"{key_prefix}_{item}",
#                     format="%d"
#                 )
#                 items[item] = val
#         return items

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


# Default values for categories (enhanced with more items)
kebutuhan_pokok_default = {
    "Sewa Rumah": 3000000,
    "Listrik": 700000,
    "Air": 300000,
    "Internet & TV Kabel": 500000,
    "Makanan Pokok & Dapur": 3000000,
    "Makan di Luar / Pesan Antar": 1500000,
    "Pulsa & Paket Data": 300000
}

transportasi_default = {
    "BBM / Transport Umum": 1000000,
    "Perawatan Kendaraan": 300000,
    "Parkir & Tol": 300000
}

perawatan_ratna_default = {
    "Skincare & Kosmetik": 1500000,
    "Perawatan Rambut & Tubuh": 500000,
    "Pakaian & Aksesoris": 1000000
}

kesehatan_asuransi_default = {
    "Asuransi Kesehatan": 1000000,
    "Obat-obatan & Check-up": 500000,
    "Asuransi Jiwa": 500000
}

rumah_tangga_default = {
    "Kebersihan & Peralatan": 500000,
    "Perawatan & Perbaikan Rumah": 300000,
    "Furniture & Elektronik": 1000000
}

pendidikan_anak_default = {
    "Tabungan Pendidikan Anak": 1500000,
    "Les & Ekstrakurikuler": 1000000,
    "Buku & Alat Tulis": 500000
}

gaya_hidup_default = {
    "Jalan-jalan & Nongkrong": 2000000,
    "Hobi & Olahraga": 500000,
    "Langganan (Netflix, Spotify, dll)": 50000
}

sedekah_default = {
    "Sedekah & Amal": 2000000,
    "Zakat": 500000,
    "Donasi Sosial": 500000
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

# Savings and investments in the sidebar with enhanced features
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

        with st.expander("Tabungan Khusus", expanded=True):
            # NEW FEATURE 4: Multiple Savings Goals
            tabungan_mobil = st.number_input(
                "Target Tabungan Mobil (Rp)",
                min_value=0,
                value=100000000,
                step=10000000,
                format="%d"
            )
            waktu_mobil_bulan = st.number_input(
                "Waktu Nabung Mobil (bulan)",
                min_value=1,
                value=48
            )
            tabungan_mobil_bulanan = tabungan_mobil / waktu_mobil_bulan if waktu_mobil_bulan > 0 else 0
            st.write(f"▪️ Tabungan Bulanan: Rp {tabungan_mobil_bulanan:,.0f}")
            
            # NEW: Additional savings goal
            tabungan_liburan = st.number_input(
                "Target Tabungan Liburan (Rp)",
                min_value=0,
                value=20000000,
                step=1000000,
                format="%d"
            )
            waktu_liburan_bulan = st.number_input(
                "Waktu Nabung Liburan / haji / umroh (bulan)",
                min_value=1,
                value=24
            )
            tabungan_liburan_bulanan = tabungan_liburan / waktu_liburan_bulan if waktu_liburan_bulan > 0 else 0
            st.write(f"▪️ Tabungan Bulanan: Rp {tabungan_liburan_bulanan:,.0f}")

        # NEW FEATURE 5: Debt Tracker
        with st.expander("🔄 Cicilan & Utang", expanded=True):
            cicilan_kartu_kredit = st.number_input(
                "Cicilan Kartu Kredit (Rp)",
                min_value=0,
                value=0,
                step=100000,
                format="%d"
            )
            cicilan_lain = st.number_input(
                "Cicilan Lainnya (Rp)",
                min_value=0,
                value=0,
                step=100000,
                format="%d"
            )

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
total_cicilan = cicilan_kartu_kredit + cicilan_lain
total_pengeluaran = (
    total_kebutuhan_pokok + total_transportasi + total_perawatan_ratna +
    total_kesehatan_asuransi + total_rumah_tangga + total_pendidikan_anak +
    total_gaya_hidup + total_sedekah + total_tabungan_investasi +
    dana_darurat + tabungan_mobil_bulanan + tabungan_liburan_bulanan +
    total_cicilan
)

sisa_gaji = gaji_total - total_pengeluaran

# ===========================================
# NEW FEATURE 6: Multi-Month Projection
# ===========================================
def calculate_projection(months, income_growth_rate):
    projection = []
    current_income = gaji_total
    current_date = datetime.now()
    
    for month in range(months):
        month_data = {
            "Bulan": (current_date + timedelta(days=30*month)).strftime("%B %Y"),
            "Pendapatan": current_income,
            "Pengeluaran": total_pengeluaran,
            "Tabungan": current_income - total_pengeluaran,
            "Akumulasi Tabungan": (current_income - total_pengeluaran) * (month + 1)
        }
        projection.append(month_data)
        current_income *= (1 + income_growth_rate)
    
    return pd.DataFrame(projection)

projection_df = calculate_projection(planning_months, income_growth)

# Summary section with enhanced layout
st.markdown("---")
st.markdown("<h2 class='header'>📊 Ringkasan Keuangan</h2>", unsafe_allow_html=True)

summary_cols = st.columns([2, 1])

with summary_cols[0]:
    # Enhanced summary table with more metrics
    summary = {
        "Pendapatan": gaji_total,
        "Kebutuhan Pokok": total_kebutuhan_pokok,
        "Transportasi": total_transportasi,
        "Perawatan Pribadi": total_perawatan_ratna,
        "Kesehatan & Asuransi": total_kesehatan_asuransi,
        "Rumah Tangga": total_rumah_tangga,
        "Pendidikan Anak": total_pendidikan_anak,
        "Gaya Hidup & Hiburan": total_gaya_hidup,
        "Sedekah & Amal": total_sedekah,
        "Cicilan & Utang": total_cicilan,
        "Tabungan & Investasi": total_tabungan_investasi,
        "Dana Darurat": dana_darurat,
        "Tabungan Khusus": tabungan_mobil_bulanan + tabungan_liburan_bulanan
    }

    df_summary = pd.DataFrame.from_dict(summary, orient='index', columns=['Amount'])
    df_summary['Percentage'] = (df_summary['Amount'] / gaji_total * 100).round(1)
    df_summary['Amount'] = df_summary['Amount'].apply(lambda x: f"Rp {x:,.0f}")
    df_summary['Percentage'] = df_summary['Percentage'].apply(lambda x: f"{x}%")
    
    st.dataframe(
        df_summary,
        use_container_width=True,
        column_config={
            "index": st.column_config.Column("Kategori", width="medium"),
            "Amount": st.column_config.Column("Jumlah", width="medium"),
            "Percentage": st.column_config.Column("% dari Pendapatan", width="small")
        }
    )

with summary_cols[1]:
    # Enhanced financial summary card
    savings_rate = ((gaji_total - total_pengeluaran) / gaji_total * 100) if gaji_total > 0 else 0
    
    st.markdown(f"""
    <div class='summary-card'>
        <h4>Ringkasan Bulanan</h4>
        <p><strong>Total Pendapatan:</strong> Rp {gaji_total:,.0f}</p>
        <p><strong>Total Pengeluaran:</strong> Rp {total_pengeluaran:,.0f}</p>
        <p><strong>Sisa Gaji:</strong> <span class={'positive' if sisa_gaji >= 0 else 'negative'}>Rp {sisa_gaji:,.0f}</span></p>
        <p><strong>Rasio Tabungan:</strong> {savings_rate:.1f}%</p>
        <div style="margin-top: 1rem;">
            <small>Proyeksi {planning_months} Bulan:</small>
            <div style="background: #f1f1f1; border-radius: 5px; height: 6px; margin-top: 0.3rem;">
                <div style="background: var(--primary); width: {min(100, planning_months/12*100)}%; height: 100%; border-radius: 5px;"></div>
            </div>
            <small style="float: right;">{planning_months}/12 bulan</small>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if sisa_gaji < 0:
        st.error("⚠️ Pengeluaran melebihi pendapatan! Kurangi pengeluaran atau tingkatkan pendapatan.")
    elif savings_rate < 20:
        st.warning("ℹ️ Rasio tabungan di bawah 20%. Pertimbangkan untuk menabung lebih banyak.")
    else:
        st.success("✅ Keuangan sehat! Rasio tabungan baik.")

    # NEW FEATURE 7: Quick Action Buttons
    st.markdown("### 🚀 Aksi Cepat")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Optimasi Pengeluaran"):
            st.session_state.optimize = True
    with col2:
        if st.button("Reset Semua"):
            st.session_state.clear()
            st.rerun()

# ===========================================
# NEW FEATURE 8: Financial Projection Charts
# ===========================================
st.markdown("---")
st.markdown("<h2 class='header'>📈 Proyeksi & Visualisasi</h2>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📊 Ringkasan", "📅 Proyeksi Bulanan", "💰 Akumulasi Tabungan"])

with tab1:
    viz_cols = st.columns(2)
    with viz_cols[0]:
        # Enhanced pie chart
        st.subheader("Komposisi Pengeluaran")
        fig = px.pie(
            names=list(summary.keys())[1:],  # Exclude income
            values=list(summary.values())[1:],
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)

    with viz_cols[1]:
        # Enhanced bar chart
        st.subheader("Perbandingan Kategori")
        fig = px.bar(
            x=list(summary.values())[1:],
            y=list(summary.keys())[1:],
            orientation='h',
            text=[f"Rp {x:,.0f}" for x in list(summary.values())[1:]],
            color=list(summary.keys())[1:],
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig.update_layout(
            showlegend=False, 
            xaxis_title="Amount (Rp)", 
            yaxis_title="Kategori",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    # Monthly projection chart
    st.subheader(f"Proyeksi {planning_months} Bulan Ke Depan")
    fig = px.line(
        projection_df,
        x="Bulan",
        y=["Pendapatan", "Pengeluaran"],
        color_discrete_map={"Pendapatan": "#2e86ab", "Pengeluaran": "#f18f01"},
        markers=True
    )
    fig.update_layout(
        yaxis_title="Amount (Rp)",
        hovermode="x unified",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Show projection table
    st.dataframe(
        projection_df.style.format({
            "Pendapatan": "Rp {:,.0f}",
            "Pengeluaran": "Rp {:,.0f}",
            "Tabungan": "Rp {:,.0f}",
            "Akumulasi Tabungan": "Rp {:,.0f}"
        }),
        use_container_width=True
    )

with tab3:
    # Savings accumulation chart
    st.subheader("Akumulasi Tabungan Jangka Panjang")
    fig = px.area(
        projection_df,
        x="Bulan",
        y="Akumulasi Tabungan",
        color_discrete_sequence=["#28a745"]
    )
    fig.update_layout(
        yaxis_title="Amount (Rp)",
        hovermode="x",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Savings milestones
    milestones = {
        "Dana Darurat 6 Bulan": total_pengeluaran * 6,
        "Uang Muka Rumah": 200000000,
        "Pendidikan Anak": 50000000
    }
    
    months_to_milestone = {}
    for name, target in milestones.items():
        for i, row in projection_df.iterrows():
            if row['Akumulasi Tabungan'] >= target:
                months_to_milestone[name] = i + 1
                break
    
    if months_to_milestone:
        st.subheader("🏆 Target Tabungan")
        for name, months in months_to_milestone.items():
            st.metric(
                label=name,
                value=f"{months} bulan",
                help=f"Akan tercapai pada {projection_df.iloc[months-1]['Bulan']}"
            )

# ===========================================
# NEW FEATURE 9: Financial Health Check
# ===========================================
st.markdown("---")
st.markdown("<h2 class='header'>🩺 Cek Kesehatan Keuangan</h2>", unsafe_allow_html=True)

health_cols = st.columns(3)

with health_cols[0]:
    # Emergency fund check
    emergency_months = (dana_darurat * planning_months) / total_pengeluaran if total_pengeluaran > 0 else 0
    st.metric(
        "Dana Darurat", 
        f"{emergency_months:.1f} bulan", 
        help="Dana darurat ideal 3-6 bulan pengeluaran"
    )
    st.progress(min(1, emergency_months/6))

with health_cols[1]:
    # Debt-to-income ratio
    debt_ratio = (total_cicilan / gaji_total * 100) if gaji_total > 0 else 0
    st.metric(
        "Rasio Cicilan", 
        f"{debt_ratio:.1f}%", 
        help="Rasio cicilan sebaiknya <30% dari pendapatan"
    )
    st.progress(min(1, debt_ratio/30))

with health_cols[2]:
    # Savings rate
    st.metric(
        "Rasio Tabungan", 
        f"{savings_rate:.1f}%", 
        help="Rasio tabungan ideal 20% dari pendapatan"
    )
    # st.progress(min(1, savings_rate/20))
    st.progress(min(1.0, max(0.0, savings_rate / 20)))

# Tips section with dynamic recommendations
st.markdown("---")
st.markdown("<h2 class='header'>💡 Rekomendasi & Tips</h2>", unsafe_allow_html=True)

recommendations = []
if savings_rate < 20:
    recommendations.append("💡 Tingkatkan rasio tabungan Anda minimal 20% dari pendapatan")
if debt_ratio > 30:
    recommendations.append("💡 Rasio cicilan Anda tinggi. Pertimbangkan untuk melunasi utang dengan bunga tinggi terlebih dahulu")
if emergency_months < 3:
    recommendations.append(f"💡 Dana darurat Anda hanya {emergency_months:.1f} bulan. Targetkan minimal 3-6 bulan pengeluaran")
if sisa_gaji < 0:
    recommendations.append("💡 Pengeluaran melebihi pendapatan. Tinjau kategori pengeluaran terbesar untuk penghematan")
if not recommendations:
    recommendations.append("🎉 Keuangan Anda dalam kondisi sehat! Pertahankan kebiasaan baik ini")

for rec in recommendations:
    st.markdown(f"- {rec}")

# Enhanced tips section
tips = [
    "✅ Gunakan metode amplop digital untuk mengelola pengeluaran harian",
    "✅ Manfaatkan cashback dan promo untuk pengeluaran rutin",
    "✅ Lakukan review keuangan mingguan bersama keluarga",
    "✅ Investasikan dana darurat di instrumen likuid dengan bunga menarik",
    f"✅ Dengan menabung Rp {int((gaji_total - total_pengeluaran)/1000)*1000:,} per bulan, dalam {planning_months} bulan Anda akan memiliki Rp {int(projection_df.iloc[-1]['Akumulasi Tabungan']/1000)*1000:,}"
]

for tip in tips:
    st.markdown(f"- {tip}")

# ===========================================
# NEW FEATURE 10: Export & Share
# ===========================================
st.markdown("---")
st.markdown("<h2 class='header'>📤 Export & Share</h2>", unsafe_allow_html=True)

export_cols = st.columns(3)
with export_cols[0]:
    # Export as CSV
    csv = projection_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Export ke CSV",
        data=csv,
        file_name="financial_projection.csv",
        mime="text/csv"
    )
with export_cols[1]:
    # Export as Excel
    excel_buffer = BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
        projection_df.to_excel(writer, index=False, sheet_name='Proyeksi')
        df_summary.to_excel(writer, sheet_name='Ringkasan')
    excel_data = excel_buffer.getvalue()
    st.download_button(
        label="📊 Export ke Excel",
        data=excel_data,
        file_name="financial_plan.xlsx",
        mime="application/vnd.ms-excel"
    )
with export_cols[2]:
    # Shareable link
    if st.button("🔗 Buat Link Share"):
        st.warning("Fitur ini membutuhkan integrasi dengan database. Coming soon!")

# Footer with enhanced info
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6c757d; font-size: 0.9rem; margin-top: 2rem;">
    <p>Family Financial Planner v2.0 • © 2025</p>
</div>
""", unsafe_allow_html=True)