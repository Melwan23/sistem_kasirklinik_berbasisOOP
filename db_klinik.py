import mysql.connector

def get_db_connector():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='db_klinik'
    )

def verifikasi_pasien(id_pasien, jenis_pasien, no_kartu=None):
    try:
        conn = get_db_connector()
        cursor = conn.cursor(dictionary=True)

        query = 'SELECT * FROM pasien WHERE id_pasien = %s AND jenis_pasien = %s'
        params = [id_pasien, jenis_pasien]

        if jenis_pasien == 'Pasien BPJS':
            query += ' AND no_bpjs = %s'
            params.append(no_kartu)
        elif jenis_pasien == 'Pasien Asuransi':
            query += ' AND no_polis = %s'
            params.append(no_kartu)

        # POSISI BENAR: Eksekusi ditaruh DI LUAR if/elif agar semua jenis pasien bisa dicek
        cursor.execute(query, tuple(params))
        data = cursor.fetchone()

        cursor.close()
        conn.close()

        return data is not None
    except Exception as err:
        print(f'Database Error: {err}')
        return False

def simpan_transaksi(id_pasien, biaya_tindakan, biaya_obat, total_bayar, nama_pasien=None, jenis_pasien='Pasien Umum'):
    try:
        conn = get_db_connector()
        cursor = conn.cursor()

        cursor.execute("SELECT id_pasien FROM pasien WHERE id_pasien = %s", (id_pasien,))
        ada = cursor.fetchone()

        if not ada and nama_pasien:
            cursor.execute(
                "INSERT INTO pasien (id_pasien, nama_pasien, jenis_pasien) VALUES (%s, %s, %s)",
                (id_pasien, nama_pasien, jenis_pasien)
            )

        query = '''
            INSERT INTO transaksi (id_pasien, biaya_tindakan, biaya_obat, total_bayar)
            VALUES (%s, %s, %s, %s)
        '''
        cursor.execute(query, (id_pasien, biaya_tindakan, biaya_obat, total_bayar))
        conn.commit()

        cursor.close()
        conn.close()
        return True
    except Exception as err:
        print(f'Error Simpan Transaksi: {err}')
        return False