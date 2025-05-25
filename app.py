import streamlit as st
import joblib
import numpy as np
import os
import tensorflow as tf
from utils import extract_aac_features

# 載入 SVM 模型
svm_model = joblib.load("svm_model_AAC.pkl")
svm_label_encoder = joblib.load("label_encoder_AAC.pkl")

# 載入 CNN 模型（SavedModel 格式）
cnn_model = tf.keras.models.load_model("family_predictor_model")
cnn_label_encoder = joblib.load("family_label_encoder.pkl")

# 建立模型選單
model_option = st.selectbox("請選擇要使用的模型", ["SVM (AAC)", "CNN (AAC)"])

# Streamlit 主畫面
st.title("Efflux Protein Family Predictor 🧬")
st.markdown("請輸入單條蛋白質序列（FASTA 格式），使用 SVM 或 CNN 進行分類。")

# 使用者輸入序列
fasta_input = st.text_area("請貼上蛋白質序列（FASTA 格式）")

# 當按下按鈕時進行預測
if st.button("開始預測"):
    if not fasta_input.strip():
        st.warning("請輸入蛋白質序列")
    else:
        lines = fasta_input.strip().split('\n')
        sequence = ''.join([line.strip() for line in lines if not line.startswith(">")])

        if not sequence.isalpha():
            st.error("❌ 序列中包含非字母字符，請確認僅輸入 A-Z 字母")
        else:
            features = extract_aac_features(sequence).reshape(1, -1)

            if model_option == "SVM (AAC)":
                pred = svm_model.predict(features)[0]
                result = svm_label_encoder.inverse_transform([pred])[0]
                st.success(f"✅ SVM 預測家族：**{result}**")

            elif model_option == "CNN (AAC)":
                features_cnn = features.reshape(1, 20, 1)  # CNN 輸入形狀
                pred = np.argmax(cnn_model.predict(features_cnn), axis=1)[0]
                result = cnn_label_encoder.inverse_transform([pred])[0]
                st.success(f"✅ CNN 預測家族：**{result}**")
