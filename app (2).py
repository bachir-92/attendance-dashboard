
import streamlit as st
import pandas as pd
import datetime

# إعدادات الصفحة
st.set_page_config(page_title="مخزن الحبوب", page_icon="🌾", layout="wide")
st.markdown("<h1 style='text-align: center; color: #1F3864;'>🌾 نظام تسيير السطوك (المخزن)</h1>", unsafe_allow_html=True)

# الرصيد الافتتاحي
RASED_IFTTITAHI = 83.77

# تهيئة الجلسة (الذاكرة المؤقتة)
if 'operations' not in st.session_state:
    st.session_state.operations = pd.DataFrame(columns=["Date", "Type", "Quantité (Qx)"])

# ================= الشريط الجانبي (الإدخال) =================
st.sidebar.header("📝 Ajouter une opération")

with st.sidebar.form("form_ajout"):
    date_op = st.date_input("Date de l'opération", datetime.date.today())
    
    type_op = st.selectbox("Type d'opération", ["Entrée (دخول)", "Sortie (خروج)"])
    
    qte = st.number_input("Quantité (Qx)", min_value=0.01, step=0.01, format="%.2f")
    
    submit = st.form_submit_button("➕ Ajouter au registre", use_container_width=True)

    if submit:
        new_row = pd.DataFrame({
            "Date": [str(date_op)], 
            "Type": [type_op], 
            "Quantité (Qx)": [qte]
        })
        st.session_state.operations = pd.concat([st.session_state.operations, new_row], ignore_index=True)
        st.success(f"Opération ajoutée avec succès !")

# ================= الحسابات =================
if not st.session_state.operations.empty:
    total_entrees = st.session_state.operations[st.session_state.operations["Type"] == "Entrée (دخول)"]["Quantité (Qx)"].sum()
    total_sorties = st.session_state.operations[st.session_state.operations["Type"] == "Sortie (خروج)"]["Quantité (Qx)"].sum()
else:
    total_entrees = 0.0
    total_sorties = 0.0

rased_hali = RASED_IFTTITAHI + total_entrees - total_sorties

# ================= لوحة التحكم =================
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

col1.metric("Stock Initial (Qx)", f"{RASED_IFTTITAHI:.2f}")
col2.metric("Total Entrées (Qx)", f"+{total_entrees:.2f}", delta_color="normal")
col3.metric("Total Sorties (Qx)", f"-{total_sorties:.2f}", delta_color="inverse")
col4.metric("🌟 Stock Actuel (Reste)", f"{rased_hali:.2f}")

st.markdown("---")

# ================= الجدول =================
st.subheader("📋 Registre des Opérations")
if not st.session_state.operations.empty:
    st.dataframe(st.session_state.operations.style.format({"Quantité (Qx)": "{:.2f}"}), use_container_width=True)
    
    if st.button("🗑️ Effacer toutes les données"):
        st.session_state.operations = pd.DataFrame(columns=["Date", "Type", "Quantité (Qx)"])
        st.rerun()
else:
    st.info("Le registre est vide. Utilisez le menu de gauche pour ajouter votre première opération.")
