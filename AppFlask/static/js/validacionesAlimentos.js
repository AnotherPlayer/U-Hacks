document.addEventListener("DOMContentLoaded", function () {
  iniciarPaginaAlimentos();
});

function obtenerSesionDesdeURL() {
  const parametros = new URLSearchParams(window.location.search);

  const email = parametros.get("email");
  const usuarioGenerado = parametros.get("usuario");

  return {
    email: email,
    usuarioGenerado: usuarioGenerado
  };
}

function crearURLConSesion(pagina) {
  const sesion = obtenerSesionDesdeURL();

  return (
    pagina +
    "?email=" +
    encodeURIComponent(sesion.email) +
    "&usuario=" +
    encodeURIComponent(sesion.usuarioGenerado)
  );
}

function iniciarPaginaAlimentos() {
  const sesion = obtenerSesionDesdeURL();

  if (!sesion.email || !sesion.usuarioGenerado) {
    window.location.href = "login.html";
    return;
  }

  cargarDatosUsuario();
  mostrarAlimentos();

  const btnGuardarAlimento = document.getElementById("btnGuardarAlimento");
  const btnCerrarSesion = document.getElementById("btnCerrarSesion");
  const btnIrPacientes = document.getElementById("btnIrPacientes");

  btnGuardarAlimento.addEventListener("click", guardarAlimento);

  btnCerrarSesion.addEventListener("click", function () {
    window.location.href = "login.html";
  });

  btnIrPacientes.addEventListener("click", function () {
    window.location.href = crearURLConSesion("pacientes.html");
  });
}


// ==========================
// DATOS DEL USUARIO
// ==========================

function cargarDatosUsuario() {
  const sesion = obtenerSesionDesdeURL();

  document.getElementById("correoUsuario").textContent = sesion.email || "Sin correo";
  document.getElementById("usuarioGenerado").textContent = sesion.usuarioGenerado || "Sin ID";
}


// ==========================
// VALIDACIÓN ALIMENTOS
// Solo valida nombre VARCHAR(100)
// ==========================

function validarNombreAlimento(nombre) {
  const errores = [];

  if (!nombre) {
    errores.push("El nombre del alimento no puede estar vacío.");
    return errores;
  }

  if (nombre.length > 100) {
    errores.push("El nombre del alimento no debe superar 100 caracteres.");
  }

  // Solo permite letras, acentos, ñ y espacios
  const patron = /^[a-zA-ZÁÉÍÓÚáéíóúÑñ\s]+$/;

  if (!patron.test(nombre)) {
    errores.push("El nombre del alimento solo puede contener letras y espacios. No se permiten números ni símbolos.");
  }

  return errores;
}


// ==========================
// LOCALSTORAGE ALIMENTOS
// ==========================

function obtenerAlimentos() {
  return JSON.parse(localStorage.getItem("alimentos")) || [];
}

function guardarAlimentos(alimentos) {
  localStorage.setItem("alimentos", JSON.stringify(alimentos));
}

function alimentoExiste(nombre) {
  const alimentos = obtenerAlimentos();

  return alimentos.some(function (alimento) {
    return alimento.nombre.toLowerCase() === nombre.toLowerCase();
  });
}

function generarIdAlimento() {
  const alimentos = obtenerAlimentos();

  if (alimentos.length === 0) {
    return 1;
  }

  const ultimoId = Math.max(...alimentos.map(function (alimento) {
    return alimento.id;
  }));

  return ultimoId + 1;
}


// ==========================
// GUARDAR ALIMENTO
// ==========================

function guardarAlimento() {
  const nombre = document.getElementById("nombreAlimento").value.trim();

  let errores = [];

  errores.push(...validarNombreAlimento(nombre));

  if (alimentoExiste(nombre)) {
    errores.push("Ese alimento ya está registrado.");
  }

  if (errores.length > 0) {
    Swal.fire({
      icon: "error",
      title: "Datos inválidos",
      html: errores.join("<br>"),
      confirmButtonText: "Corregir"
    });

    return;
  }

  const alimentos = obtenerAlimentos();

  const nuevoAlimento = {
    id: generarIdAlimento(),
    nombre: nombre
  };

  alimentos.push(nuevoAlimento);

  guardarAlimentos(alimentos);

  Swal.fire({
    icon: "success",
    title: "Alimento guardado",
    text: "El alimento fue registrado correctamente.",
    confirmButtonText: "Aceptar"
  });

  document.getElementById("nombreAlimento").value = "";

  mostrarAlimentos();
}


// ==========================
// MOSTRAR ALIMENTOS
// ==========================

function mostrarAlimentos() {
  const tablaAlimentos = document.getElementById("tablaAlimentos");
  const alimentos = obtenerAlimentos();

  tablaAlimentos.innerHTML = "";

  if (alimentos.length === 0) {
    tablaAlimentos.innerHTML = `
      <tr>
        <td colspan="2">No hay alimentos registrados.</td>
      </tr>
    `;
    return;
  }

  alimentos.forEach(function (alimento) {
    const fila = document.createElement("tr");

    fila.innerHTML = `
      <td>${alimento.id}</td>
      <td>${alimento.nombre}</td>
    `;

    tablaAlimentos.appendChild(fila);
  });
}