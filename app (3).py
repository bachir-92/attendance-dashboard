
import streamlit as st
import pandas as pd
import datetime
import io
import streamlit.components.v1 as components

# إعدادات الصفحة
st.set_page_config(page_title="URCA CCLS JIJEL - Stock", page_icon="🌾", layout="wide")

# --- الترويسة الرسمية ---
st.markdown(
    """
    <div style='text-align: center; border-bottom: 2px solid #1F3864; padding-bottom: 10px; margin-bottom: 20px;'>
        <h2 style='color: #1F3864; margin: 0;'>URCA CCLS JIJEL</h2>
        <h4 style='color: #2E75B6; margin: 5px 0 0 0;'>نظام تسيير السطوك (المخزن)</h4>
    </div>
    """, 
    unsafe_allow_html=True
)

# الرصيد الافتتاحي
RASED_IFTTITAHI = 83.77

# تهيئة الجلسة
if 'operations' not in st.session_state:
    st.session_state.operations = pd.DataFrame(columns=["Date", "Type", "Quantité (Qx)"])

# ================= الشريط الجانبي =================
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
        st.success("Opération ajoutée avec succès !")

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

# ================= الجدول والتحميل والطباعة =================
st.subheader("📋 Registre des Opérations")

if not st.session_state.operations.empty:
    # عرض الجدول
    st.dataframe(st.session_state.operations.style.format({"Quantité (Qx)": "{:.2f}"}), use_container_width=True)
    
    # --- أزرار التحميل والطباعة ---
    col_excel, col_print, col_clear = st.columns(3)
    
    # 1. تحميل الإكسل (مع الترويسة)
    with col_excel:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # كتابة اسم المؤسسة في الصف الأول
            df_to_excel = st.session_state.operations.copy()
            df_to_excel.to_excel(writer, index=False, sheet_name='Stock', startrow=2)
            
            # تنسيق الإكسل
            workbook = writer.book
            worksheet = writer.sheets['Stock']
            worksheet.cell(row=1, column=1, value="URCA CCLS JIJEL - Registre de Stock")
            worksheet.cell(row=1, column=1).font = openpyxl.styles.Font(bold=True, size=14)
            
        excel_data = output.getvalue()
        
        st.download_button(
            label="📥 Télécharger Excel",
            data=excel_data,
            file_name=f"URCA_CCLS_JIJEL_Stock_{datetime.date.today()}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    
    # 2. طباعة التقرير
    with col_print:
        print_js = '''
        <button onclick="window.print()" style="width: 100%; height: 38px; background-color: #f0f2f6; border: 1px solid #d6d6d6; border-radius: 8px; cursor: pointer; font-family: sans-serif; font-size: 14px;">
            🖨️ Imprimer (PDF)
        </button>
        '''
        components.html(print_js, height=45)

    # 3. مسح البيانات
    with col_clear:
        if st.button("🗑️ Effacer les données", use_container_width=True):
            st.session_state.operations = pd.DataFrame(columns=["Date", "Type", "Quantité (Qx)"])
            st.rerun()

else:
    st.info("Le registre est vide. Utilisez le menu de gauche pour ajouter votre première opération.")
