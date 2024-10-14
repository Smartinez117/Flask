// Manejo del formulario para crear un nuevo registro
document.getElementById('create-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const nombre = document.getElementById('nombre').value;
    const edad = document.getElementById('edad').value;
    const carrera_id = document.getElementById('carrera_id').value;

    const response = await fetch('/create', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ nombre, edad, carrera_id })
    });

    const result = await response.json();

    // Mostrar alert basado en la respuesta del servidor
    alert(result.message); // Mostrar mensaje de éxito o error
});

// Manejo del formulario para actualizar un registro existente
document.getElementById('update-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const recordId = document.getElementById('update-id').value;
    const nombre = document.getElementById('update-nombre').value;
    const edad = document.getElementById('update-edad').value;
    const carrera_id = document.getElementById('update-carrera_id').value;

    const response = await fetch(`/update/${recordId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ nombre, edad, carrera_id })
    });

    const result = await response.json();

    // Mostrar alert basado en la respuesta del servidor
    alert(result.message); // Mostrar mensaje de éxito o error
});

// Manejo del formulario para eliminar un registro
document.getElementById('delete-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const recordId = document.getElementById('delete-id').value;

    const response = await fetch(`/delete/${recordId}`, {
        method: 'DELETE'
    });

    const result = await response.json();
    
    // Mostrar alert basado en la respuesta del servidor
    alert(result.message); // Mostrar mensaje de éxito o error
});

// Función para mostrar todos los registros
async function fetchRecords() {
   const response = await fetch('/read');
   const records = await response.json();

   const recordsDiv = document.getElementById('records');
   recordsDiv.innerHTML = '';
   
   records.forEach(record => {
       recordsDiv.innerHTML += `<p>ID: ${record.id}, Nombre: ${record.nombre}, Edad: ${record.edad}, Carrera: ${record.carrera}</p>`;
   });
}

// Manejo del formulario para buscar un registro por ID
document.getElementById('search-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const recordId = document.getElementById('search-id').value;

    const response = await fetch(`/read/${recordId}`);
    
    if (response.ok) {
        const record = await response.json();
        document.getElementById('record-details').innerHTML =
            `<p>ID: ${record.id}, Nombre: ${record.nombre}, Edad: ${record.edad}, Carrera: ${record.carrera}</p>`;
    } else {
        const result = await response.json();
        alert(result.message); // Mostrar mensaje de error si el registro no se encuentra
        document.getElementById('record-details').innerHTML = '';
    }
});