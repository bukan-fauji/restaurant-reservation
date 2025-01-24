from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.db import connect_db
import json

reservation_bp = Blueprint('reservation_bp', __name__)

# Ambil daftar meja yang tersedia
@reservation_bp.route('/tables', methods=['GET'])
def get_available_tables():
    """
    Get available tables
    ---
    tags:
      - Reservation
    responses:
      200:
        description: Daftar meja berhasil diambil
        schema:
          type: object
          properties:
            tables:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  name:
                    type: string
                    example: Table 1
                  available:
                    type: boolean
                    example: true
"""
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM table_restaurant WHERE available = TRUE")
    tables = cursor.fetchall()

    return jsonify({'tables': tables}), 200

# Buat reservasi
@reservation_bp.route('/reserve', methods=['POST'])
@jwt_required()
def make_reservation():
    """
    Make a table reservation
    ---
    tags:
      - Reservation
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            table_id:
              type: integer
              example: 1
            date:
              type: string
              example: 2025-01-25
            time:
              type: string
              example: 18:00
    responses:
      201:
        description: Reservasi berhasil!
      400:
        description: Meja tidak tersedia, data tidak lengkap, atau sudah dipesan!
"""
    current_user = json.loads(get_jwt_identity())  # Konversi dari string ke dictionary
    print("Current User:", current_user)  # Debugging

    data = request.json
    table_id = data.get('table_id')
    date = data.get('date')
    time = data.get('time')

    if not table_id or not date or not time:
        return jsonify({'message': 'Semua data harus diisi!'}), 400

    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    # Cek apakah meja tersedia
    cursor.execute("SELECT * FROM table_restaurant WHERE id = %s AND available = TRUE", (table_id,))
    table = cursor.fetchone()

    if not table:
        return jsonify({'message': 'Meja tidak tersedia atau sudah dipesan!'}), 400

    # Simpan reservasi
    cursor.execute("""
        INSERT INTO reservation (user_id, table_id, date, time, status) 
        VALUES (%s, %s, %s, %s, 'pending')
    """, (current_user['id'], table_id, date, time))
    conn.commit()

    # Update status meja jadi tidak tersedia
    cursor.execute("UPDATE table_restaurant SET available = FALSE WHERE id = %s", (table_id,))
    conn.commit()

    return jsonify({'message': 'Reservasi berhasil!'}), 201


# Lihat daftar reservasi pengguna
@reservation_bp.route('/my-reservations', methods=['GET'])
@jwt_required()
def get_my_reservations():
    """
    Get my reservations
    ---
    tags:
      - Reservation
    responses:
      200:
        description: Daftar reservasi berhasil diambil
        schema:
          type: object
          properties:
            reservations:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  user_id:
                    type: integer
                    example: 2
                  table_id:
                    type: integer
                    example: 1
                  date:
                    type: string
                    example: 2025-01-25
                  time:
                    type: string
                    example: 18:00
                  status:
                    type: string
                    example: pending
"""
    current_user = get_jwt_identity()
    
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM reservation WHERE user_id = %s", (current_user['id'],))
    reservations = cursor.fetchall()
    
    return jsonify({'reservations': reservations}), 200

# Batalkan reservasi
@reservation_bp.route('/cancel/<int:reservation_id>', methods=['DELETE'])
@jwt_required()
def cancel_reservation(reservation_id):
    """
    Cancel a reservation
    ---
    tags:
      - Reservation
    parameters:
      - name: reservation_id
        in: path
        required: true
        type: integer
        example: 1
    responses:
      200:
        description: Reservasi berhasil dibatalkan!
      404:
        description: Reservasi tidak ditemukan atau bukan milik pengguna!
"""
    current_user = get_jwt_identity()
    conn = connect_db()
    cursor = conn.cursor()

    # Ambil reservasi
    cursor.execute("SELECT * FROM reservation WHERE id = %s AND user_id = %s", 
                   (reservation_id, current_user['id']))
    reservation = cursor.fetchone()

    if not reservation:
        return jsonify({'message': 'Reservasi tidak ditemukan atau bukan milik Anda!'}), 404

    # Batalkan reservasi dan buat meja tersedia lagi
    cursor.execute("UPDATE table_restaurant SET available = TRUE WHERE id = %s", (reservation[2],))
    cursor.execute("DELETE FROM reservation WHERE id = %s", (reservation_id,))
    conn.commit()

    return jsonify({'message': 'Reservasi berhasil dibatalkan!'}), 200


