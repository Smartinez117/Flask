from flask import Flask, render_template, request, jsonify
import psycopg2
import time

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        dbname='presentacion1',
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
            edad INTEGER NOT NULL,
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
    carrera_id = int(data['carrera_id'])
    
    conn = get_db_connection()
    
    cur = conn.cursor()
    
    # Verificar que la carrera existe
    cur.execute("SELECT id FROM carreras WHERE id=%s", (carrera_id,))
    
    if cur.fetchone() is None:
        return jsonify({'message': 'Carrera no válida.'}), 400
    
    cur.execute("INSERT INTO tablaprueba1 (nombre, edad, carrera_id) VALUES (%s, %s, %s)", (nombre, edad, carrera_id))
    
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

@app.route('/read/<int:record_id>', methods=['GET'])
def read_record(record_id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT t.id, t.nombre, t.edad, c.nombre 
        FROM tablaprueba1 t 
        JOIN carreras c ON t.carrera_id = c.id
        WHERE t.id = %s
    """, (record_id,))
    
    resultado = cur.fetchone()
    
    if resultado is None:
        return jsonify({'message': 'Registro no encontrado.'}), 404
    
    registro = {
        'id': resultado[0],
        'nombre': resultado[1],
        'edad': resultado[2],
        'carrera': resultado[3]
    }

    cur.close()
    conn.close()

    return jsonify(registro)

@app.route('/update/<int:record_id>', methods=['PUT'])
def update_record(record_id):
   data = request.get_json()
   
   nombre = data['nombre']
   edad = data['edad']
   carrera_id = int(data['carrera_id'])  # Cambiado a ID de carrera
   transaction_level = data['transactionLevel']  # Obtener el nivel de aislamiento
   
   conn = get_db_connection()
   
   try:
       if transaction_level == "NO TRANSACTION":
           with conn:
               with conn.cursor() as cur:
                   cur.execute("UPDATE tablaprueba1 SET nombre=%s, edad=%s, carrera_id=%s WHERE id=%s", (nombre, edad, carrera_id, record_id))
                   if cur.rowcount == 0:
                       return jsonify({'message': 'Registro no encontrado.'}), 404
           return jsonify({'message': 'Registro actualizado exitosamente sin transacción.'})

       # Iniciar una transacción y establecer el nivel de aislamiento
       with conn:
           with conn.cursor() as cur:
               if transaction_level == "SERIALIZABLE":
                   cur.execute("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;")
               elif transaction_level == "READ COMMITTED":
                   cur.execute("SET TRANSACTION ISOLATION LEVEL READ COMMITTED;")
               
               # Simulación de una operación que podría ser afectada por el nivel de aislamiento
               time.sleep(5)  # Simula un retraso en la operación
               
               # Actualizar el registro
               cur.execute("UPDATE tablaprueba1 SET nombre=%s, edad=%s, carrera_id=%s WHERE id=%s", (nombre, edad, carrera_id, record_id))
               
               if cur.rowcount == 0:
                   return jsonify({'message': 'Registro no encontrado.'}), 404

       return jsonify({'message': 'Registro actualizado exitosamente con transacción.'})
   
   except Exception as e:
       return jsonify({'message': str(e)}), 500
   
   finally:
       conn.close()

@app.route('/test_transactions', methods=['POST'])
def test_transactions():
    transaction_level = request.json.get('transactionLevel')
    
    conn = get_db_connection()
    
    try:
        with conn:
            with conn.cursor() as cur:
                if transaction_level == "SERIALIZABLE":
                    cur.execute("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;")
                elif transaction_level == "READ COMMITTED":
                    cur.execute("SET TRANSACTION ISOLATION LEVEL READ COMMITTED;")

                time.sleep(5)  # Simula un retraso en la operación
                
                # Realizar una consulta para ver cómo se comporta el nivel de aislamiento
                cur.execute("SELECT * FROM tablaprueba1;")
                results = cur.fetchall()
                
                return jsonify({'message': 'Transacción completada.', 'results': results})
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    
    finally:
        conn.close()

@app.route('/delete/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
   conn = get_db_connection()
   
   with conn:
       with conn.cursor() as cur:
           cur.execute("DELETE FROM tablaprueba1 WHERE id=%s", (record_id,))
           
           if cur.rowcount == 0:
               return jsonify({'message': 'Registro no encontrado.'}), 404

   return jsonify({'message': 'Registro eliminado exitosamente.'})

if __name__ == '__main__':
   app.run(debug=True)