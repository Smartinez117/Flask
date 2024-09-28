from flask import Flask, render_template, request, jsonify
import psycopg2

app = Flask(__name__)

# Configuración de la conexión a la base de datos
def get_db_connection():
    conn = psycopg2.connect(
        dbname="baseDeDatos",  # Cambia esto por el nombre de tu base de datos
        user="postgres",        # Cambia esto por tu usuario de PostgreSQL
        password="basededatos", # Cambia esto por tu contraseña
        host="localhost",
        port="5432"
    )
    return conn

# Función para crear la tabla si no existe
def create_table_if_not_exists():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tablaprueba1 (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            edad INTEGER NOT NULL,
            carrera VARCHAR(50) NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

# Llama a la función para crear la tabla al iniciar la aplicación
create_table_if_not_exists()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['POST'])
def create_record():
    data = request.get_json()
    nombre = data['nombre']
    edad = data['edad']
    carrera = data['carrera']

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO tablaprueba1 (nombre, edad, carrera) VALUES (%s, %s, %s)", (nombre, edad, carrera))
    conn.commit()
    
    cur.close()
    conn.close()

    return jsonify({'message': 'Registro creado exitosamente.'}), 201

@app.route('/read', methods=['GET'])
def read_records():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tablaprueba1")
    resultados = cur.fetchall()
    
    registros = [{'id': fila[0], 'nombre': fila[1], 'edad': fila[2], 'carrera': fila[3]} for fila in resultados]

    cur.close()
    conn.close()

    return jsonify(registros)

@app.route('/update/<int:record_id>', methods=['PUT'])
def update_record(record_id):
    data = request.get_json()
    nombre = data['nombre']
    edad = data['edad']
    carrera = data['carrera']

    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("UPDATE tablaprueba1 SET nombre=%s, edad=%s, carrera=%s WHERE id=%s", (nombre, edad, carrera, record_id))
    conn.commit()

    if cur.rowcount == 0:
        return jsonify({'message': 'Registro no encontrado.'}), 404

    cur.close()
    conn.close()

    return jsonify({'message': 'Registro actualizado exitosamente.'})

@app.route('/delete/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("DELETE FROM tablaprueba1 WHERE id=%s", (record_id,))
    conn.commit()

    if cur.rowcount == 0:
        return jsonify({'message': 'Registro no encontrado.'}), 404

    cur.close()
    conn.close()

    return jsonify({'message': 'Registro eliminado exitosamente.'})

if __name__ == '__main__':
    app.run(debug=True)