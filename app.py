
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import random

# إعدادات الصفحة
st.set_page_config(page_title="لوحة تحكم الحضور", page_icon="📊", layout="wide")

# تصميم الواجهة
st.markdown("<h1 style='text-align: center; color: #1F3864;'>📊 نظام إدارة الحضور والغياب</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# دالة توليد بيانات تجريبية (يمكنك ربطها بقاعدة بيانات لاحقاً)
@st.cache_data
def load_data():
    data = []
    workers = ["محمد أحمد", "علي يوسف", "سعيد كريم", "خالد عمر", "يوسف بن علي"]
    statuses = ["حاضر", "غائب", "جمعة", "عطلة"]
    start_date = datetime(2025, 1, 1)
    for i in range(30):
        current_date = start_date + timedelta(days=i)
        for worker in workers:
            status = random.choices(statuses, weights=[0.7, 0.1, 0.15, 0.05])[0]
            overtime = random.randint(0, 4) if status == "حاضر" and random.random() > 0.7 else 0
            data.append({"التاريخ": current_date, "العامل": worker, "الحالة": status, "ساعات إضافية": overtime})
    return pd.DataFrame(data)

df = load_data()

# الشريط الجانبي
st.sidebar.header("⚙️ خيارات الفلترة")
selected_worker = st.sidebar.multiselect("اختر العامل:", df["العامل"].unique(), default=df["العامل"].unique())
filtered_df = df[df["العامل"].isin(selected_worker)]

# المؤشرات
col1, col2, col3, col4 = st.columns(4)
col1.metric("العمال المحددين", len(selected_worker))
col2.metric("أيام الحضور", len(filtered_df[filtered_df["الحالة"] == "حاضر"]))
col3.metric("أيام الغياب", len(filtered_df[filtered_df["الحالة"] == "غائب"]))
col4.metric("الساعات الإضافية", f"{filtered_df['ساعات إضافية'].sum()} ساعة")

st.markdown("<br>", unsafe_allow_html=True)

# الرسوم البيانية
c1, c2 = st.columns(2)
with c1:
    st.subheader("📈 توزيع الحالات")
    sc = filtered_df["الحالة"].value_counts().reset_index()
    sc.columns = ["الحالة", "العدد"]
    fig = px.pie(sc, names="الحالة", values="العدد", color="الحالة", 
                 color_discrete_map={"حاضر": "#28a745", "غائب": "#dc3545", "جمعة": "#007bff", "عطلة": "#6c757d"})
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("📊 الحضور لكل عامل")
    wc = filtered_df[filtered_df["الحالة"] == "حاضر"]["العامل"].value_counts().reset_index()
    wc.columns = ["العامل", "أيام"]
    fig2 = px.bar(wc, x="العامل", y="أيام", color="العامل")
    st.plotly_chart(fig2, use_container_width=True)

# الجدول
st.subheader("📋 السجل التفصيلي")
st.dataframe(filtered_df.sort_values(by="التاريخ", ascending=False), use_container_width=True)
