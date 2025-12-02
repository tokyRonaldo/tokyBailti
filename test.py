from weasyprint import HTML

html_string = "<p>Test PDF</p>"
pdf = HTML(string=html_string, base_url="http://localhost/").write_pdf()

with open("test.pdf", "wb") as f:
    f.write(pdf)
print("PDF généré !")
