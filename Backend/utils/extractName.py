def extract_name_from_content(content: str):
    # Convert ke list baris
    lines = content.split("\n")

    # Prioritas kata kunci nama
    keywords = ["nama", "nama siswa", "nama ekskul", "nama ekskul/komunitas"]

    for line in lines:
        for key in keywords:
            if line.lower().startswith(key):
                # Ambil setelah ":"
                parts = line.split(":", 1)
                if len(parts) > 1:
                    return parts[1].strip()

    # fallback: ambil 1 baris pertama dari content
    return lines[0][:40]  # potong biar rapi
