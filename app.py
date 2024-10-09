from flask import Flask, render_template, request, jsonify
import psycopg2

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        dbname='baseDeDatos',
        user='postgres',
        password='basededatos',
        host='localhost',
        port='5432'
    )
    return conn

def create_table_if_not_exists():
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS carreras (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(50) UNIQUE NOT NULL
        )
    """)
    
    for carrera in ['mecanica', 'quimica', 'sistemas', 'electrica']:
        cur.execute("INSERT INTO carreras (nombre) VALUES (%s) ON CONFLICT (nombre) DO NOTHING;", (carrera,))
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tablaprueba1 (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            edad INTEGER NOT NULL CHECK (edad >= 18),
            carrera_id INTEGER REFERENCES carreras(id) ON DELETE CASCADE
        )
    """)
    
    conn.commit()
    cur.close()
    conn.close()

create_table_if_not_exists()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['POST'])
def create_record():
    data = request.get_json()
    
    nombre = data['nombre']
    edad = int(data['edad'])
    
    # Validar que la edad sea mayor o igual a 18
    if edad < 18:
        return jsonify({'message': 'La edad debe ser mayor o igual a 18.'}), 400
    
    carrera_nombre = data['carrera']
    
    conn = get_db_connection()
    
    cur = conn.cursor()
    
    cur.execute("SELECT id FROM carreras WHERE nombre=%s", (carrera_nombre,))
    
    carrera_id = cur.fetchone()
    
    if not carrera_id:
        return jsonify({'message': 'Carrera no válida.'}), 400
    
    cur.execute("INSERT INTO tablaprueba1 (nombre, edad, carrera_id) VALUES (%s, %s, %s)", (nombre, edad, carrera_id[0]))
    
    conn.commit()
    
    cur.close()
    conn.close()

    return jsonify({'message': 'Registro creado exitosamente.'}), 201

@app.route('/read', methods=['GET'])
def read_records():
   conn = get_db_connection()
   cur = conn.cursor()
   
   cur.execute("""
       SELECT t.id, t.nombre, t.edad, c.nombre 
       FROM tablaprueba1 t 
       JOIN carreras c ON t.carrera_id = c.id
   """)
   
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
   
   if edad < 18:
       return jsonify({'message': 'La edad debe ser mayor o igual a 18.'}), 400
   
   carrera_nombre = data['carrera']
   
   conn = get_db_connection()
   
   cur = conn.cursor()
   
   cur.execute("SELECT id FROM carreras WHERE nombre=%s", (carrera_nombre,))
   
   carrera_id = cur.fetchone()
   
   if not carrera_id:
       return jsonify({'message': 'Carrera no válida.'}), 400
   
   cur.execute("UPDATE tablaprueba1 SET nombre=%s, edad=%s, carrera_id=%s WHERE id=%s", (nombre, edad, carrera_id[0], record_id))
   
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