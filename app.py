import streamlit as st
import numpy as np
from utils import extract_aac_features
from tensorflow.keras.models import load_model
import joblib

# === 假模型（代替 SVM） ===
class DummyModel:
    def predict(self, X):
        return [0]

class DummyLabelEncoder:
    def inverse_transform(self, labels):
        return ["ABC Transporter"]

# 模型選單
model_option = st.selectbox("請選擇預測模型", ["SVM (AAC)", "CNN (AAC)"])

# 載入 CNN 模型與編碼器
try:
    cnn_model = load_model("family_predictor_cnn.h5")
    cnn_label_encoder = joblib.load("family_label_encoder.pkl")
    cnn_available = True
except Exception as e:
    cnn_model = None
    cnn_label_encoder = None
    cnn_available = False
    st.warning("⚠️ 無法載入 CNN 模型或編碼器，請確認檔案是否存在。")

# SVM 目前使用假模型
svm_model = DummyModel()
svm_label_encoder = DummyLabelEncoder()

# === 使用介面 ===
st.title("Efflux Protein Family Predictor 🧬")
st.markdown("請貼上蛋白質序列（FASTA 格式），並選擇預測模型。")

fasta_input = st.text_area("請貼上蛋白質序列（FASTA 格式）")

if st.button("開始預測"):
    if not fasta_input.strip():
        st.warning("請輸入蛋白質序列")
    else:
        lines = fasta_input.strip().split('\n')
        sequence = ''.join([line.strip() for line in lines if not line.startswith(">")])

        if not sequence.isalpha():
            st.error("序列中包含非字母字符，請確認格式正確")
        else:
            features = extract_aac_features(sequence).reshape(1, -1)

            if model_option == "SVM (AAC)":
                pred = svm_model.predict(features)[0]
                result = svm_label_encoder.inverse_transform([pred])[0]
                st.success(f"✅ 模擬預測家族（SVM）：**{result}**")

            elif model_option == "CNN (AAC)":
                if not cnn_available:
                    st.error("❌ 無法使用 CNN，請確認檔案存在且能成功載入。")
                else:
                    features_cnn = features.reshape(1, 20, 1)
                    pred = np.argmax(cnn_model.predict(features_cnn), axis=1)[0]
                    result = cnn_label_encoder.inverse_transform([pred])[0]
                    st.success(f"✅ 預測家族（CNN）：**{result}**")
