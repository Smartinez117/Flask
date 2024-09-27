document.getElementById('create-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const nombre = document.getElementById('nombre').value;
    const edad = document.getElementById('edad').value;
    const carrera = document.getElementById('carrera').value;

    const response = await fetch('/create', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ nombre, edad, carrera })
    });

    const result = await response.json();
    alert(result.message);
});

document.getElementById('update-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const recordId = document.getElementById('update-id').value;
    const nombre = document.getElementById('update-nombre').value;
    const edad = document.getElementById('update-edad').value;
    const carrera = document.getElementById('update-carrera').value;

    const response = await fetch(`/update/${recordId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ nombre, edad, carrera })
    });

    const result = await response.json();
    alert(result.message);
});

document.getElementById('delete-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const recordId = document.getElementById('delete-id').value;

    const response = await fetch(`/delete/${recordId}`, {
        method: 'DELETE'
    });

    const result = await response.json();
    alert(result.message);
});

async function fetchRecords() {
   const response = await fetch('/read');
   const records = await response.json();

   const recordsDiv = document.getElementById('records');
   recordsDiv.innerHTML = '';
   
   records.forEach(record => {
       recordsDiv.innerHTML += `<p>ID: ${record.id}, Nombre: ${record.nombre}, Edad: ${record.edad}, Carrera: ${record.carrera}</p>`;
   });
}