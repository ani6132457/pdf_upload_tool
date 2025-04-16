import streamlit as st
import pandas as pd
from pdf2image import convert_from_bytes
import pytesseract
import os
import io

# Ghostscript パス（必要なら）
os.environ["PATH"] += os.pathsep + r"C:\Program Files\gs\gs10.05.0\bin"

# Tesseract OCR のパス
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Poppler のパス（←あなたの環境に合わせて書き換えてOK）
poppler_path = r"C:\poppler-24.08.0\Library\bin"

st.title("🧠 スキャンPDF OCR抽出ツール")
uploaded_file = st.file_uploader("📤 スキャンPDFファイルをアップロードしてください", type=["pdf"])

if uploaded_file:
    with st.spinner("OCR処理中...お待ちください！"):
        # Popplerのパスを渡すことでPDF → 画像変換が有効になる！
        images = convert_from_bytes(uploaded_file.read(), dpi=300, poppler_path=poppler_path)
        text_data = []

        for i, image in enumerate(images):
            text = pytesseract.image_to_string(image, lang="jpn")
            text_data.append([f"{i+1}ページ", text])

        df = pd.DataFrame(text_data, columns=["ページ", "抽出テキスト"])
        st.success("✅ OCR抽出完了！")

        st.subheader("📋 抽出結果プレビュー")
        st.dataframe(df)

        # CSV出力
        csv = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button("📥 CSVでダウンロード", csv, file_name="ocr_output.csv", mime="text/csv")
