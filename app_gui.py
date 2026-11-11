import html
import os
import webbrowser
import customtkinter as ctk

from demo_program import PasienUmum, PasienBPJS, PasienAsuransi
from db_klinik import verifikasi_pasien, simpan_transaksi, cari_pasien_by_id

def buat_nota_html(pasien):
    subtotal = pasien.get_biaya_tindakan() + pasien.get_biaya_obat()
    total_bayar = pasien.hitung_tagihan()
    potongan = subtotal - total_bayar

    id_pasien = html.escape(str(pasien.get_id_pasien()))
    nama_pasien = html.escape(str(pasien.get_nama()))

    if isinstance(pasien, PasienUmum):
        tipe_str = "Pasien Umum"
        ket_str = "Membayar 100% biaya tindakan & obat"
        diskon_str = "Rp 0"
    elif isinstance(pasien, PasienBPJS):
        tipe_str = "Pasien BPJS"
        ket_str = "Biaya obat dikover penuh oleh BPJS"
        diskon_str = f"Rp {pasien.get_biaya_obat():,.0f}"
    elif isinstance(pasien, PasienAsuransi):
        tipe_str = "Pasien Asuransi"
        ket_str = "Diskon Klaim Polis Asuransi"
        diskon_str = f"Rp {potongan:,.0f}"

    html_content = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nota Pembayaran | Klinik Kelompok 7</title>
    <style>
        :root {{
            --ink: #1e293b;
            --muted: #64748b;
            --teal: #0d9488;
            --teal-dark: #0f766e;
            --teal-light: #f0fdfa;
            --teal-border: #ccfbf1;
            --line: #e2e8f0;
            --red: #f43f5e;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            min-height: 100vh;
            padding: 40px 15px;
            display: grid;
            place-items: center;
            color: var(--ink);
            background-color: #f8fafc;
            background-image: 
                radial-gradient(at 10% 10%, rgba(13, 148, 136, 0.08) 0px, transparent 50%),
                radial-gradient(at 90% 90%, rgba(20, 184, 166, 0.06) 0px, transparent 50%);
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
        }}
        .card {{
            position: relative;
            width: 100%;
            max-width: 460px;
            padding: 32px;
            border-radius: 20px;
            background: #ffffff;
            border: 1px solid rgba(226, 232, 240, 0.8);
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01);
        }}
        .clinic-heading {{ display: flex; align-items: center; gap: 14px; margin-bottom: 24px; }}
        .clinic-mark {{
            flex: 0 0 46px;
            width: 46px;
            height: 46px;
            display: grid;
            place-items: center;
            border-radius: 14px;
            background: var(--teal-light);
            color: var(--teal);
            border: 1px solid var(--teal-border);
        }}
        .clinic-mark svg {{ width: 26px; height: 26px; }}
        .clinic-name {{ margin: 0; font-size: 18px; font-weight: 700; color: #0f172a; letter-spacing: -0.3px; }}
        .clinic-address {{ margin: 3px 0 0; color: var(--muted); font-size: 12px; }}
        .receipt-title {{
            margin: 0 0 24px;
            padding: 16px 18px;
            border-radius: 14px;
            background: var(--teal-light);
            border: 1px solid var(--teal-border);
        }}
        .receipt-title span {{ display: block; color: var(--teal); font-size: 11px; font-weight: 800; letter-spacing: 1.2px; text-transform: uppercase; }}
        .receipt-title strong {{ display: block; margin-top: 4px; font-size: 15px; font-weight: 700; color: #0f172a; }}
        .section-label {{
            margin: 20px 0 10px;
            color: #94a3b8;
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 1px;
            text-transform: uppercase;
        }}
        table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
        td {{ padding: 8px 0; vertical-align: middle; }}
        td:first-child {{ color: var(--muted); }}
        td.right {{ padding-left: 12px; color: var(--ink); text-align: right; font-weight: 600; }}
        tr + tr td {{ border-top: 1px solid var(--line); }}
        .subtotal td {{ padding-top: 10px; color: var(--ink); font-weight: 700; }}
        .discount {{ color: var(--red) !important; }}
        .total-box {{
            margin-top: 22px;
            padding: 16px 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            border-radius: 14px;
            background: var(--teal-light);
            border: 1px solid var(--teal-border);
        }}
        .total-box span {{ color: var(--teal-dark); font-size: 13px; font-weight: 800; letter-spacing: 0.8px; }}
        .total-box strong {{ color: var(--teal-dark); font-size: 19px; font-weight: 800; white-space: nowrap; }}
        .thank-you {{ margin: 24px 0 0; color: #94a3b8; font-size: 12px; line-height: 1.5; text-align: center; }}
        .actions {{ display: flex; gap: 12px; margin-top: 22px; }}
        .actions button {{
            flex: 1;
            padding: 12px 14px;
            border-radius: 12px;
            cursor: pointer;
            font: inherit;
            font-size: 13px;
            font-weight: 600;
            transition: all 0.2s ease;
        }}
        .print-button {{
            background: var(--teal);
            border: none;
            color: white;
            box-shadow: 0 4px 12px rgba(13, 148, 136, 0.25);
        }}
        .print-button:hover {{ background: var(--teal-dark); }}
        .download-button {{
            border: 1px solid #cbd5e1;
            background: #ffffff;
            color: var(--teal-dark);
        }}
        .download-button:hover {{ background: #f8fafc; border-color: #94a3b8; }}
        .download-status {{ min-height: 18px; margin: 10px 0 0; color: var(--muted); font-size: 11px; text-align: center; }}
        @media (max-width: 520px) {{
            body {{ padding: 20px 10px; }}
            .card {{ padding: 24px 18px; border-radius: 16px; }}
        }}
        @media print {{
            @page {{ margin: 10mm; }}
            body {{ min-height: auto; padding: 0; background: white; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
            .card {{ width: 100%; max-width: 460px; margin: 0 auto; border: 1px solid var(--line); box-shadow: none; }}
            .actions, .download-status {{ display: none !important; }}
        }}
    </style>
</head>
<body>
    <main class="card" id="receipt">
        <header class="clinic-heading">
            <div class="clinic-mark" aria-hidden="true">
                <svg viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M8 5v7a6 6 0 0 0 12 0V5M8 5H6v3m14-3h2v3M14 18v1a7 7 0 0 0 14 0v-3" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
                    <circle cx="26" cy="14" r="2" fill="currentColor"/>
                </svg>
            </div>
            <div>
                <h1 class="clinic-name">Klinik Kelompok 7</h1>
                <p class="clinic-address">Jl. Sipelem, Kampus UBSI Tegal</p>
            </div>
        </header>
        <h2 class="receipt-title">
            <span>BUKTI PEMBAYARAN</span>
            <strong>Terima kasih atas kepercayaan Anda</strong>
        </h2>
        <h3 class="section-label">Informasi pasien</h3>
        <table class="patient-table">
            <tbody>
                <tr><td>ID Pasien</td><td class="right">{id_pasien}</td></tr>
                <tr><td>Nama Pasien</td><td class="right">{nama_pasien}</td></tr>
                <tr><td>Kategori</td><td class="right">{html.escape(tipe_str)}</td></tr>
            </tbody>
        </table>
        <h3 class="section-label">Rincian pembayaran</h3>
        <table class="payment-table">
            <tbody>
                <tr><td>Biaya Tindakan Medis</td><td class="right">Rp {pasien.get_biaya_tindakan():,.0f}</td></tr>
                <tr><td>Biaya Obat-obatan</td><td class="right">Rp {pasien.get_biaya_obat():,.0f}</td></tr>
                <tr class="subtotal"><td>Subtotal</td><td class="right">Rp {subtotal:,.0f}</td></tr>
                <tr><td>{html.escape(ket_str)}</td><td class="right discount">- {diskon_str}</td></tr>
            </tbody>
        </table>
        <div class="total-box">
            <span>TOTAL BAYAR</span>
            <strong>Rp {total_bayar:,.0f}</strong>
        </div>
        <p class="thank-you">Semoga lekas sehat. Terima kasih telah berobat di Klinik Kelompok 7.</p>
        <div class="actions" aria-label="Aksi struk">
            <button class="print-button" type="button" onclick="window.print()">Cetak / Simpan PDF</button>
            <button class="download-button" type="button" onclick="downloadReceipt()">Unduh JPG</button>
        </div>
        <p class="download-status" role="status" aria-live="polite"></p>
    </main>
    <script>
        async function downloadReceipt() {{
            const status = document.querySelector(".download-status");
            let imageUrl;
            try {{
                const text = selector => document.querySelector(selector).textContent.trim();
                const patientRows = [...document.querySelectorAll(".patient-table tr")];
                const paymentRows = [...document.querySelectorAll(".payment-table tr")];
                const data = {{
                    clinic: text(".clinic-name"),
                    address: text(".clinic-address"),
                    title: text(".receipt-title span"),
                    subtitle: text(".receipt-title strong"),
                    patientHeading: "INFORMASI PASIEN",
                    patient: patientRows.map(row => [...row.cells].map(cell => cell.textContent.trim())),
                    paymentHeading: "RINCIAN PEMBAYARAN",
                    payment: paymentRows.map(row => [...row.cells].map(cell => cell.textContent.trim())),
                    totalLabel: text(".total-box span"),
                    total: text(".total-box strong"),
                    thankYou: text(".thank-you")
                }};
                const escapeXml = value => String(value).replace(/[&<>"']/g, char => ({{
                    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&apos;"
                }})[char]);
                const line = (value, x, y, options = {{}}) =>
                    `<text x="${{x}}" y="${{y}}" fill="${{options.color || "#17323b"}}" font-family="Segoe UI, Arial, sans-serif" font-size="${{options.size || 13}}" font-weight="${{options.weight || 400}}" text-anchor="${{options.anchor || "start"}}" letter-spacing="${{options.spacing || 0}}">${{escapeXml(value)}}</text>`;
                const parts = [
                    '<svg xmlns="http://www.w3.org/2000/svg" width="940" height="1320" viewBox="0 0 470 660">',
                    '<defs><radialGradient id="glow"><stop stop-color="#69cfb1" stop-opacity=".24"/><stop offset="1" stop-color="#69cfb1" stop-opacity="0"/></radialGradient></defs>',
                    '<rect width="470" height="660" rx="24" fill="#ffffff"/>',
                    '<ellipse cx="420" cy="24" rx="130" ry="118" fill="url(#glow)"/>',
                    '<rect x="34" y="34" width="52" height="52" rx="17" fill="#e1f5ee" stroke="#d4ebe4"/>',
                    '<g transform="translate(46 46)" fill="none" stroke="#087f82" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M8 5v7a6 6 0 0 0 12 0V5M8 5H6v3m14-3h2v3M14 18v1a7 7 0 0 0 14 0v-3"/><circle cx="26" cy="14" r="2" fill="#087f82" stroke="none"/></g>',
                    line(data.clinic, 100, 57, {{ size: 19, weight: 750 }}),
                    line(data.address, 100, 77, {{ size: 12, color: "#6f858b" }}),
                    '<rect x="34" y="108" width="402" height="66" rx="16" fill="#eaf8f3" stroke="#e1efeb"/>',
                    line(data.title, 52, 134, {{ size: 10, weight: 800, color: "#087f82", spacing: 1.8 }}),
                    line(data.subtitle, 52, 158, {{ size: 16, weight: 700 }}),
                    line(data.patientHeading, 34, 207, {{ size: 10, weight: 800, color: "#6f858b", spacing: 1.4 }})
                ];
                let y = 235;
                for (const [label, value] of data.patient) {{
                    parts.push(line(label, 34, y, {{ color: "#6f858b" }}));
                    parts.push(line(value, 436, y, {{ anchor: "end" }}));
                    y += 34;
                }}
                y += 8;
                parts.push(line(data.paymentHeading, 34, y, {{ size: 10, weight: 800, color: "#6f858b", spacing: 1.4 }}));
                y += 28;
                for (const [index, [label, value]] of data.payment.entries()) {{
                    const isSubtotal = index === 2;
                    const isDiscount = index === 3;
                    parts.push(line(label, 34, y, {{ color: isSubtotal ? "#17323b" : "#6f858b", weight: isSubtotal ? 700 : 400, size: 12 }}));
                    parts.push(line(value, 436, y, {{ anchor: "end", color: isDiscount ? "#d45e4b" : "#17323b", weight: isSubtotal ? 700 : 400, size: 12 }}));
                    y += isSubtotal ? 38 : 32;
                }}
                y += 2;
                parts.push(`<rect x="34" y="${{y}}" width="402" height="58" rx="16" fill="#eaf5f3" stroke="#dcebe8"/>`);
                parts.push(line(data.totalLabel, 52, y + 35, {{ size: 14, weight: 800, color: "#087f82", spacing: 1.2 }}));
                parts.push(line(data.total, 418, y + 36, {{ size: 19, weight: 750, color: "#087f82", anchor: "end" }}));
                y += 91;
                parts.push(line(data.thankYou, 235, y, {{ size: 11, color: "#6f858b", anchor: "middle" }}));
                parts[0] = `<svg xmlns="http://www.w3.org/2000/svg" width="940" height="${{(y + 28) * 2}}" viewBox="0 0 470 ${{y + 28}}">`;
                parts.push("</svg>");

                const svgBlob = new Blob(parts, {{ type: "image/svg+xml;charset=utf-8" }});
                imageUrl = URL.createObjectURL(svgBlob);
                const image = new Image();
                image.src = imageUrl;
                await image.decode();

                const canvas = document.createElement("canvas");
                canvas.width = image.naturalWidth;
                canvas.height = image.naturalHeight;
                const context = canvas.getContext("2d");
                if (!context) throw new Error("Tidak dapat membuat gambar struk.");
                context.fillStyle = "#ffffff";
                context.fillRect(0, 0, canvas.width, canvas.height);
                context.drawImage(image, 0, 0);

                const jpg = await new Promise((resolve, reject) => {{
                    canvas.toBlob(file => file ? resolve(file) : reject(new Error("Gambar struk gagal dibuat.")), "image/jpeg", .95);
                }});
                const patientId = document.querySelector(".patient-table tr td.right").textContent.trim().replace(/[^a-zA-Z0-9_-]/g, "_");
                const link = document.createElement("a");
                link.href = URL.createObjectURL(jpg);
                link.download = `struk-klinik-${{patientId}}.jpg`;
                document.body.appendChild(link);
                link.click();
                link.remove();
                status.textContent = "Struk berhasil diunduh sebagai gambar JPG.";
                window.setTimeout(() => URL.revokeObjectURL(link.href), 1000);
            }} catch (error) {{
                console.error("Gagal mengunduh struk sebagai JPG.", error);
                status.textContent = "Gagal membuat gambar struk. Silakan coba tombol cetak.";
            }} finally {{
                if (imageUrl) URL.revokeObjectURL(imageUrl);
            }}
        }}
    </script>
</body>
</html>
"""
    filename = "nota_pembayaran.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    webbrowser.open("file://" + os.path.realpath(filename))

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class AppKlinik(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.FONT_MAIN = "Arial"

        self.title("Sistem Tagihan Klinik (GUI Mode)")
        self.geometry("490x740")
        self.resizable(False, False)
        
        self.configure(fg_color="#f8fafc")

        self.frame_header = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_header.pack(padx=24, pady=(20, 10), fill="x")

        self.lbl_logo = ctk.CTkLabel(
            self.frame_header,
            text="🩺",
            font=ctk.CTkFont(size=22),
            width=46,
            height=46,
            fg_color="#f0fdfa",
            text_color="#0d9488",
            corner_radius=14
        )
        self.lbl_logo.pack(side="left", padx=(0, 12))

        self.frame_header_text = ctk.CTkFrame(self.frame_header, fg_color="transparent")
        self.frame_header_text.pack(side="left", fill="both")

        self.lbl_clinic_name = ctk.CTkLabel(
            self.frame_header_text,
            text="Klinik Kelompok 7",
            font=ctk.CTkFont(family=self.FONT_MAIN, size=18, weight="bold"),
            text_color="#0f172a"
        )
        self.lbl_clinic_name.pack(anchor="w")

        self.lbl_clinic_addr = ctk.CTkLabel(
            self.frame_header_text,
            text="Jl. Sipelem, Kampus UBSI Tegal",
            font=ctk.CTkFont(family=self.FONT_MAIN, size=12),
            text_color="#64748b"
        )
        self.lbl_clinic_addr.pack(anchor="w")

        self.frame = ctk.CTkFrame(
            self,
            corner_radius=20,
            fg_color="#ffffff",
            border_width=1,
            border_color="#e2e8f0"
        )
        self.frame.pack(padx=24, pady=(0, 20), fill="both", expand=True)

        self.frame_banner = ctk.CTkFrame(
            self.frame,
            corner_radius=12,
            fg_color="#f0fdfa",
            border_width=1,
            border_color="#ccfbf1"
        )
        self.frame_banner.pack(padx=20, pady=(16, 12), fill="x")

        self.lbl_banner_tag = ctk.CTkLabel(
            self.frame_banner,
            text="TRANSAKSI KASIR",
            font=ctk.CTkFont(family=self.FONT_MAIN, size=10, weight="bold"),
            text_color="#0d9488"
        )
        self.lbl_banner_tag.pack(anchor="w", padx=14, pady=(8, 1))

        self.lbl_banner_title = ctk.CTkLabel(
            self.frame_banner,
            text="Input Data Tagihan & Pembayaran",
            font=ctk.CTkFont(family=self.FONT_MAIN, size=14, weight="bold"),
            text_color="#0f172a"
        )
        self.lbl_banner_title.pack(anchor="w", padx=14, pady=(0, 8))

        self.lbl_id = ctk.CTkLabel(self.frame, text="ID Pasien:", font=ctk.CTkFont(family=self.FONT_MAIN, size=12, weight="bold"), text_color="#1e293b")
        self.lbl_id.pack(anchor="w", padx=20, pady=(4, 2))

        self.frame_id = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.frame_id.pack(padx=20, pady=(0, 6), fill="x")

        self.entry_id = ctk.CTkEntry(
            self.frame_id, 
            placeholder_text="Contoh: P-000",
            font=ctk.CTkFont(family=self.FONT_MAIN, size=12),
            fg_color="#f8fafc",
            border_color="#cbd5e1",
            text_color="#1e293b",
            placeholder_text_color="#94a3b8",
            corner_radius=10
        )
        self.entry_id.pack(side="left", expand=True, fill="x", padx=(0, 6))

        self.btn_search = ctk.CTkButton(
            self.frame_id,
            text="🔍 Cari",
            width=75,
            command=self.cari_pasien,
            fg_color="#0d9488",
            hover_color="#0f766e",
            text_color="#ffffff",
            corner_radius=10,
            font=ctk.CTkFont(family=self.FONT_MAIN, size=12, weight="bold")
        )
        self.btn_search.pack(side="right")

        self.entry_nama = self._buat_input("Nama Pasien:", "Masukkan nama pasien")
        self.entry_tindakan = self._buat_input("Biaya Tindakan Medis (Rp):", "0")
        self.entry_obat = self._buat_input("Biaya Obat-obatan (Rp):", "0")

        self.lbl_jenis = ctk.CTkLabel(self.frame, text="Jenis Kepesertaan Pasien:", font=ctk.CTkFont(family=self.FONT_MAIN, size=12, weight="bold"), text_color="#1e293b")
        self.lbl_jenis.pack(anchor="w", padx=20, pady=(4, 2))
        
        self.combo_jenis = ctk.CTkOptionMenu(
            self.frame, 
            values=["Pasien Umum", "Pasien BPJS", "Pasien Asuransi"],
            command=self._on_jenis_change,
            fg_color="#f0fdfa",
            button_color="#0d9488",
            button_hover_color="#0f766e",
            text_color="#0f766e",
            dropdown_fg_color="#ffffff",
            dropdown_text_color="#1e293b",
            corner_radius=10,
            font=ctk.CTkFont(family=self.FONT_MAIN, size=12, weight="bold")
        )
        self.combo_jenis.pack(padx=20, pady=(0, 8), fill="x")

        self.frame_extra = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.lbl_extra = ctk.CTkLabel(self.frame_extra, text="", font=ctk.CTkFont(family=self.FONT_MAIN, size=12, weight="bold"), text_color="#1e293b")
        self.entry_extra = ctk.CTkEntry(
            self.frame_extra,
            font=ctk.CTkFont(family=self.FONT_MAIN, size=12),
            fg_color="#f8fafc",
            border_color="#cbd5e1",
            text_color="#1e293b",
            placeholder_text_color="#94a3b8",
            corner_radius=10
        )

        self.frame_btn = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.frame_btn.pack(padx=20, pady=(14, 8), fill="x")

        self.btn_hitung = ctk.CTkButton(
            self.frame_btn, 
            text="Hitung & Cetak Nota HTML", 
            command=self.proses_transaksi, 
            fg_color="#0d9488", 
            hover_color="#0f766e",
            text_color="#ffffff",
            corner_radius=10,
            font=ctk.CTkFont(family=self.FONT_MAIN, size=12, weight="bold"),
            height=40
        )
        self.btn_hitung.pack(side="left", expand=True, fill="x", padx=(0, 5))

        self.btn_reset = ctk.CTkButton(
            self.frame_btn, 
            text="Reset Form", 
            command=self.reset_form, 
            fg_color="#ffffff", 
            hover_color="#fff1f2",
            text_color="#f43f5e",
            border_width=1,
            border_color="#fecdd3",
            corner_radius=10,
            font=ctk.CTkFont(family=self.FONT_MAIN, size=12, weight="bold"),
            height=40
        )
        self.btn_reset.pack(side="right", expand=True, fill="x", padx=(5, 0))

        self.lbl_hasil = ctk.CTkLabel(self.frame, text="", font=ctk.CTkFont(family=self.FONT_MAIN, size=12, weight="bold"), text_color="#0d9488")
        self.lbl_hasil.pack(pady=6)

        self._on_jenis_change("Pasien Umum")

    def _buat_input(self, label_text, placeholder):
        lbl = ctk.CTkLabel(
            self.frame, 
            text=label_text, 
            font=ctk.CTkFont(family=self.FONT_MAIN, size=12, weight="bold"), 
            text_color="#1e293b"
        )
        lbl.pack(anchor="w", padx=20, pady=(4, 2))
        
        entry = ctk.CTkEntry(
            self.frame, 
            placeholder_text=placeholder,
            font=ctk.CTkFont(family=self.FONT_MAIN, size=12),
            fg_color="#f8fafc",
            border_color="#cbd5e1",
            text_color="#1e293b",
            placeholder_text_color="#94a3b8",
            corner_radius=10
        )
        entry.pack(padx=20, pady=(0, 6), fill="x")
        return entry

    def cari_pasien(self):
        id_p = self.entry_id.get().strip()
        if not id_p:
            self.lbl_hasil.configure(text="Masukkan ID Pasien terlebih dahulu!", text_color="#f43f5e")
            return

        data = cari_pasien_by_id(id_p)
        if data:
            self.entry_nama.delete(0, "end")
            self.entry_nama.insert(0, data.get("nama_pasien", ""))

            jenis = data.get("jenis_pasien", "Pasien Umum")
            self.combo_jenis.set(jenis)
            self._on_jenis_change(jenis)

            self.entry_extra.delete(0, "end")
            if jenis == "Pasien BPJS" and data.get("no_bpjs"):
                self.entry_extra.insert(0, data["no_bpjs"])
            elif jenis == "Pasien Asuransi" and data.get("no_polis"):
                self.entry_extra.insert(0, data["no_polis"])

            self.lbl_hasil.configure(
                text=f"Data Pasien '{data['nama_pasien']}' ditemukan!",
                text_color="#0d9488"
            )
        else:
            self.lbl_hasil.configure(
                text="Pasien belum terdaftar. Silakan isi manual data pasien baru.",
                text_color="#e67e22"
            )

    def _on_jenis_change(self, choice):
        self.lbl_extra.pack_forget()
        self.entry_extra.pack_forget()

        if choice == "Pasien BPJS":
            self.frame_extra.pack(before=self.frame_btn, padx=20, pady=4, fill="x")
            self.lbl_extra.configure(text="Nomor Kartu BPJS:")
            self.entry_extra.configure(placeholder_text="Contoh: 000112233")
            self.lbl_extra.pack(anchor="w", pady=(4, 2))
            self.entry_extra.pack(fill="x")
        elif choice == "Pasien Asuransi":
            self.frame_extra.pack(before=self.frame_btn, padx=20, pady=4, fill="x")
            self.lbl_extra.configure(text="No. Polis:")
            self.entry_extra.configure(placeholder_text="Contoh: 00112233")
            self.lbl_extra.pack(anchor="w", pady=(4, 2))
            self.entry_extra.pack(fill="x")
        else:
            self.frame_extra.pack_forget()

    def reset_form(self):
        self.entry_id.delete(0, "end")
        self.entry_nama.delete(0, "end")
        self.entry_tindakan.delete(0, "end")
        self.entry_obat.delete(0, "end")
        self.entry_extra.delete(0, "end")
        self.combo_jenis.set("Pasien Umum")
        self._on_jenis_change("Pasien Umum")
        self.lbl_hasil.configure(text="")
        self.entry_id.focus()

    def proses_transaksi(self):
        try:
            id_p = self.entry_id.get().strip()
            nama = self.entry_nama.get().strip()
            tindakan = float(self.entry_tindakan.get().strip() or 0)
            obat = float(self.entry_obat.get().strip() or 0)
            jenis = self.combo_jenis.get()

            no_kartu = None
            diskon_pct = 20.0
            raw_extra = self.entry_extra.get().strip()

            if jenis == "Pasien BPJS":
                no_kartu = raw_extra
            elif jenis == "Pasien Asuransi":
                if "," in raw_extra:
                    no_kartu, pct_str = raw_extra.split(",", 1)
                    no_kartu = no_kartu.strip()
                    try:
                        diskon_pct = float(pct_str.strip())
                    except ValueError:
                        diskon_pct = 20.0
                else:
                    no_kartu = raw_extra

            if jenis in ["Pasien BPJS", "Pasien Asuransi"]:
                is_valid = verifikasi_pasien(id_p, jenis, no_kartu)
                if not is_valid:
                    self.lbl_hasil.configure(
                        text="Gagal Verifikasi: Data kartu/polis tidak terdaftar!",
                        text_color="#f43f5e"
                    )
                    return

            obj_pasien = None
            if jenis == "Pasien Umum":
                obj_pasien = PasienUmum(id_p, nama, tindakan, obat)
            elif jenis == "Pasien BPJS":
                obj_pasien = PasienBPJS(id_p, nama, tindakan, obat, no_kartu)
            elif jenis == "Pasien Asuransi":
                obj_pasien = PasienAsuransi(id_p, nama, tindakan, obat, no_kartu, diskon_pct)

            total = obj_pasien.hitung_tagihan()

            simpan_transaksi(id_p, tindakan, obat, total, nama_pasien=nama, jenis_pasien=jenis)

            self.lbl_hasil.configure(
                text=f"Terverifikasi & Tersimpan!\nTotal Tagihan: Rp {total:,.0f}",
                text_color="#0d9488"
            )
            buat_nota_html(obj_pasien)

        except ValueError:
            self.lbl_hasil.configure(text="Error: Format input angka tidak valid!", text_color="#f43f5e")

if __name__ == "__main__":
    app = AppKlinik()
    app.mainloop()