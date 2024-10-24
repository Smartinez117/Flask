primera prueba de funcionamiento de Flask en una conexion a la base de datos de postgrets
inciar el entorno virtual:
venv\Scripts\activate #donde venv es el nombre del entorno

para correr flask usar:

flask --app app --debug run # done app es el nombre del scrip principal y debug sirve para corre el codigo, de forma que se actualice al realizar los cambios hechos en el codigo original.

para gitbash usar:
source env/Scripts/activate     #esto activara el entorno virtual
para correr el flask usar:
flask --app app --debug run


-------------------------------------------------------------------------------------------------
Escenario al Ejecutar al Revés
Ejecutar READ COMMITTED Primero:
Cuando ejecutas primero la transacción READ COMMITTED, puedes actualizar el registro sin problemas.
Esta operación se completa y se confirma (commit), lo que significa que los cambios son visibles para cualquier otra transacción.
Ejecutar SERIALIZABLE Después:
Al intentar ejecutar una transacción SERIALIZABLE después de READ COMMITTED, esta última puede acceder a los datos actualizados porque ya han sido confirmados.
Sin embargo, si el SERIALIZABLE intenta leer o modificar un registro que ha sido bloqueado por otra transacción (que aún no ha sido confirmada), esperará hasta que esa transacción se complete.

