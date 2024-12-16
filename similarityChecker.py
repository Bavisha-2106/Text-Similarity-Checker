import tkinter as tk
from tkinter import filedialog, messagebox
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import fitz  
import re
import os
import requests

def preprocess_text(text):
    return text

def remove_headers_footers(text):
    text = re.sub(r"Page \d+", "", text)  
    text = re.sub(r"Introduction|Conclusion", "", text)
    return text

def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        messagebox.showerror("Error", f"Error reading {pdf_path}: {e}")
        return ""

def download_pdf(url, save_path):
    try:
        response = requests.get(url)
        with open(save_path, 'wb') as file:
            file.write(response.content)
        return save_path
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download PDF from URL: {e}")
        return ""

def compute_similarity(doc1, doc2):
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform([doc1, doc2])
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return similarity[0][0]

def select_file(entry_field):
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    entry_field.delete(0, tk.END)
    entry_field.insert(0, file_path)

def compare_pdfs():
    pdf1_path = entry_pdf1.get()
    pdf2_path = entry_pdf2.get()

    if not pdf1_path or not pdf2_path:
        messagebox.showwarning("Warning", "Please provide paths or URLs for both PDFs.")
        return

    if pdf1_path.startswith("http"):
        pdf1_path = download_pdf(pdf1_path, "temp_pdf1.pdf")
    if pdf2_path.startswith("http"):
        pdf2_path = download_pdf(pdf2_path, "temp_pdf2.pdf")

    if not os.path.exists(pdf1_path) or not os.path.exists(pdf2_path):
        messagebox.showerror("Error", "One or both PDF files are invalid or could not be downloaded.")
        return

    text1 = extract_text_from_pdf(pdf1_path)
    text2 = extract_text_from_pdf(pdf2_path)

    if text1 and text2:
        text1 = remove_headers_footers(text1)
        text2 = remove_headers_footers(text2)

        similarity_score = compute_similarity(text1, text2)
        messagebox.showinfo("Similarity Score", f"The similarity between the two PDFs is {similarity_score * 100:.2f}%")
    else:
        messagebox.showerror("Error", "Could not extract text from one or both PDFs.")

root = tk.Tk()
root.title("PDF Similarity Checker")

frame_pdf1 = tk.Frame(root)
frame_pdf1.pack(pady=10, padx=10)
tk.Label(frame_pdf1, text="PDF 1 (File):").grid(row=0, column=0, padx=5, pady=5)
entry_pdf1 = tk.Entry(frame_pdf1, width=50)
entry_pdf1.grid(row=0, column=1, padx=5, pady=5)
btn_browse_pdf1 = tk.Button(frame_pdf1, text="Browse", command=lambda: select_file(entry_pdf1))
btn_browse_pdf1.grid(row=0, column=2, padx=5, pady=5)

frame_pdf2 = tk.Frame(root)
frame_pdf2.pack(pady=10, padx=10)
tk.Label(frame_pdf2, text="PDF 2 (File):").grid(row=0, column=0, padx=5, pady=5)
entry_pdf2 = tk.Entry(frame_pdf2, width=50)
entry_pdf2.grid(row=0, column=1, padx=5, pady=5)
btn_browse_pdf2 = tk.Button(frame_pdf2, text="Browse", command=lambda: select_file(entry_pdf2))
btn_browse_pdf2.grid(row=0, column=2, padx=5, pady=5)

btn_compare = tk.Button(root, text="Compare PDFs", command=compare_pdfs, bg="blue", fg="white")
btn_compare.pack(pady=20)

root.mainloop()
