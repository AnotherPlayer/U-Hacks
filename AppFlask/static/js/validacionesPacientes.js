document.addEventListener("DOMContentLoaded", function () {
  iniciarPaginaPacientes();
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

function iniciarPaginaPacientes() {
  const sesion = obtenerSesionDesdeURL();

  if (!sesion.email || !sesion.usuarioGenerado) {
    window.location.href = "login.html";
    return;
  }

  cargarDatosUsuario();
  cargarPacienteEnFormulario();

  const btnGuardarPaciente = document.getElementById("btnGuardarPaciente");
  const btnCerrarSesion = document.getElementById("btnCerrarSesion");
  const btnIrAlimentos = document.getElementById("btnIrAlimentos");

  btnGuardarPaciente.addEventListener("click", guardarDatosPaciente);

  btnCerrarSesion.addEventListener("click", function () {
    window.location.href = "login.html";
  });

  btnIrAlimentos.addEventListener("click", function () {
    window.location.href = crearURLConSesion("alimentos.html");
  });
}


// ==========================
// DATOS DE USUARIO
// ==========================

function cargarDatosUsuario() {
  const sesion = obtenerSesionDesdeURL();

  document.getElementById("correoUsuario").textContent = sesion.email;
  document.getElementById("usuarioGenerado").textContent = sesion.usuarioGenerado;
  document.getElementById("pacienteId").value = sesion.usuarioGenerado;
}


// ==========================
// VALIDACIONES DE PACIENTE
// ==========================

function validarPacienteId(id) {
  const errores = [];

  if (!id) {
    errores.push("El ID del paciente no puede estar vacío.");
    return errores;
  }

  if (!/^[a-zA-Z0-9]+$/.test(id)) {
    errores.push("El ID del paciente solo puede contener letras y números.");
  }

  return errores;
}

function validarNombrePaciente(nombre) {
  const errores = [];

  if (!nombre) {
    errores.push("El nombre del paciente no puede estar vacío.");
    return errores;
  }

  if (nombre.length > 100) {
    errores.push("El nombre del paciente no debe superar 100 caracteres.");
  }

  if (!/^[a-zA-ZÁÉÍÓÚáéíóúÑñ\s]+$/.test(nombre)) {
    errores.push("El nombre solo debe contener letras y espacios.");
  }

  return errores;
}

function validarEdadPaciente(edad) {
  const errores = [];

  if (!edad) {
    errores.push("La edad no puede estar vacía.");
    return errores;
  }

  const edadNumero = Number(edad);

  if (!Number.isInteger(edadNumero)) {
    errores.push("La edad debe ser un número entero.");
  }

  if (edadNumero <= 0) {
    errores.push("La edad debe ser mayor que cero.");
  }

  if (edadNumero > 130) {
    errores.push("La edad no debe ser mayor a 130.");
  }

  return errores;
}

function validarPesoPaciente(peso) {
  const errores = [];

  if (!peso) {
    errores.push("El peso no puede estar vacío.");
    return errores;
  }

  const pesoNumero = Number(peso);

  if (isNaN(pesoNumero)) {
    errores.push("El peso debe ser un número válido.");
    return errores;
  }

  if (pesoNumero <= 0) {
    errores.push("El peso debe ser mayor que cero.");
  }

  if (pesoNumero > 999.99) {
    errores.push("El peso no debe superar 999.99 kg.");
  }

  const patron = /^\d{1,3}(\.\d{1,2})?$/;

  if (!patron.test(peso)) {
    errores.push("El peso debe tener máximo 3 dígitos enteros y 2 decimales.");
  }

  return errores;
}

function validarAlturaPaciente(altura) {
  const errores = [];

  if (!altura) {
    errores.push("La altura no puede estar vacía.");
    return errores;
  }

  const alturaNumero = Number(altura);

  if (!Number.isInteger(alturaNumero)) {
    errores.push("La altura debe ser un número entero.");
  }

  if (alturaNumero <= 0) {
    errores.push("La altura debe ser mayor que cero.");
  }

  if (alturaNumero > 300) {
    errores.push("La altura no debe ser mayor a 300 cm.");
  }

  return errores;
}

function validarNotasPaciente(notas) {
  const errores = [];

  if (notas.length > 500) {
    errores.push("Las notas no deben superar 500 caracteres.");
  }

  return errores;
}

function validarPaciente(paciente) {
  let errores = [];

  errores.push(...validarPacienteId(paciente.id));
  errores.push(...validarNombrePaciente(paciente.nombre));
  errores.push(...validarEdadPaciente(paciente.edad));
  errores.push(...validarPesoPaciente(paciente.peso_kg));
  errores.push(...validarAlturaPaciente(paciente.altura_cm));
  errores.push(...validarNotasPaciente(paciente.notas));

  return errores;
}


// ==========================
// LOCALSTORAGE PACIENTES
// ==========================

function obtenerPacientes() {
  return JSON.parse(localStorage.getItem("pacientes")) || [];
}

function guardarPacientes(pacientes) {
  localStorage.setItem("pacientes", JSON.stringify(pacientes));
}

function obtenerPacientePorId(id) {
  const pacientes = obtenerPacientes();

  return pacientes.find(function (paciente) {
    return paciente.id === id;
  });
}

function guardarPacienteLocalStorage(paciente) {
  const pacientes = obtenerPacientes();

  const indice = pacientes.findIndex(function (p) {
    return p.id === paciente.id;
  });

  if (indice === -1) {
    pacientes.push(paciente);
  } else {
    pacientes[indice] = paciente;
  }

  guardarPacientes(pacientes);
}


// ==========================
// FORMULARIO PACIENTE
// ==========================

function cargarPacienteEnFormulario() {
  const sesion = obtenerSesionDesdeURL();
  const paciente = obtenerPacientePorId(sesion.usuarioGenerado);

  if (!paciente) {
    return;
  }

  document.getElementById("nombrePaciente").value = paciente.nombre;
  document.getElementById("edadPaciente").value = paciente.edad;
  document.getElementById("pesoPaciente").value = paciente.peso_kg;
  document.getElementById("alturaPaciente").value = paciente.altura_cm;
  document.getElementById("notasPaciente").value = paciente.notas;

  mostrarPacienteGuardado(paciente);
}

function guardarDatosPaciente() {
  const paciente = {
    id: document.getElementById("pacienteId").value.trim(),
    nombre: document.getElementById("nombrePaciente").value.trim(),
    edad: document.getElementById("edadPaciente").value.trim(),
    peso_kg: document.getElementById("pesoPaciente").value.trim(),
    altura_cm: document.getElementById("alturaPaciente").value.trim(),
    notas: document.getElementById("notasPaciente").value.trim()
  };

  const errores = validarPaciente(paciente);

  if (errores.length > 0) {
    Swal.fire({
      icon: "error",
      title: "Datos inválidos",
      html: errores.join("<br>"),
      confirmButtonText: "Corregir"
    });

    return;
  }

  guardarPacienteLocalStorage(paciente);

  Swal.fire({
    icon: "success",
    title: "Paciente guardado",
    text: "Los datos del paciente fueron guardados correctamente.",
    confirmButtonText: "Aceptar"
  });

  mostrarPacienteGuardado(paciente);
}

function mostrarPacienteGuardado(paciente) {
  document.getElementById("datosPacienteGuardado").style.display = "block";

  document.getElementById("mostrarPacienteId").textContent = paciente.id;
  document.getElementById("mostrarNombrePaciente").textContent = paciente.nombre;
  document.getElementById("mostrarEdadPaciente").textContent = paciente.edad;
  document.getElementById("mostrarPesoPaciente").textContent = paciente.peso_kg;
  document.getElementById("mostrarAlturaPaciente").textContent = paciente.altura_cm;
  document.getElementById("mostrarNotasPaciente").textContent = paciente.notas || "Sin notas";
}