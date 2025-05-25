import streamlit as st
import joblib
import numpy as np
from utils import extract_aac_features

# 載入模型與 LabelEncoder
model = joblib.load("svm_model_AAC.pkl")
label_encoder = joblib.load("label_encoder_AAC.pkl")

st.title("Efflux Protein Family Predictor 🧬")
st.markdown("請輸入或上傳蛋白質序列（FASTA 格式，僅支援單條序列）進行家族分類預測。")

# 使用者輸入方式選擇
input_method = st.radio("請選擇輸入方式：", ["貼上序列", "上傳 FASTA 檔案"])

sequence = ""

if input_method == "貼上序列":
    fasta_input = st.text_area("請貼上蛋白質序列（FASTA 格式）")
    if fasta_input.strip():
        lines = fasta_input.strip().split('\n')
        sequence = ''.join([line.strip() for line in lines if not line.startswith(">")])

elif input_method == "上傳 FASTA 檔案":
    uploaded_file = st.file_uploader("請上傳 FASTA 檔案", type=["fasta", "fa", "txt"])
    if uploaded_file is not None:
        content = uploaded_file.read().decode("utf-8")
        lines = content.strip().split('\n')
        sequence = ''.join([line.strip() for line in lines if not line.startswith(">")])

# 預測按鈕
if st.button("開始預測"):
    if not sequence:
        st.warning("請提供蛋白質序列輸入")
    elif not sequence.isalpha():
        st.error("❌ 序列中包含非字母字符，請確認格式正確（僅限 A-Z）")
    else:
        # 特徵萃取 + 預測
        features = extract_aac_features(sequence)
        prediction = model.predict([features])[0]
        decoded = label_encoder.inverse_transform([prediction])[0]
        st.success(f"✅ 預測家族：**{decoded}**")
