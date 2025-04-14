import streamlit as st
import pdfplumber
import pandas as pd
import io

st.title("📄 PDF 文字抽出 & CSVダウンロード")

# アップロード
uploaded_file = st.file_uploader("PDFファイルをアップロードしてください", type=["pdf"])

if uploaded_file is not None:
    # テキスト格納用リスト
    text_lines = []

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                lines = text.split('\n')
                text_lines.extend(lines)

    # 表形式に整形（1列CSV）
    df = pd.DataFrame(text_lines, columns=["抽出テキスト"])

    # 表示
    st.write("🔍 抽出されたテキスト内容:")
    st.dataframe(df)

    # ダウンロード処理
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_data = csv_buffer.getvalue().encode("utf-8-sig")

    st.download_button(
        label="📥 CSVとしてダウンロード",
        data=csv_data,
        file_name="extracted_text.csv",
        mime="text/csv"
    )
