document.addEventListener("DOMContentLoaded", function () {
  iniciarLogin();
});

function iniciarLogin() {
  const tabLogin = document.getElementById("tabLogin");
  const tabRegistro = document.getElementById("tabRegistro");

  const formLogin = document.getElementById("formLogin");
  const formRegistro = document.getElementById("formRegistro");

  const btnLogin = document.getElementById("btnLogin");
  const btnRegistro = document.getElementById("btnRegistro");

  tabLogin.addEventListener("click", function () {
    formLogin.classList.add("activo");
    formRegistro.classList.remove("activo");

    tabLogin.classList.add("activo");
    tabRegistro.classList.remove("activo");
  });

  tabRegistro.addEventListener("click", function () {
    formRegistro.classList.add("activo");
    formLogin.classList.remove("activo");

    tabRegistro.classList.add("activo");
    tabLogin.classList.remove("activo");
  });

  btnRegistro.addEventListener("click", registrarse);
  btnLogin.addEventListener("click", iniciarSesion);
}


// ==========================
// ALERTAS
// ==========================

function alertaError(errores) {
  Swal.fire({
    icon: "error",
    title: "Datos inválidos",
    html: errores.join("<br>"),
    confirmButtonText: "Corregir"
  });
}

function alertaExito(titulo, mensaje) {
  Swal.fire({
    icon: "success",
    title: titulo,
    html: mensaje,
    confirmButtonText: "Aceptar"
  });
}


// ==========================
// VALIDACIONES LOGIN / REGISTRO
// ==========================

function validarCorreo(email) {
  const errores = [];

  if (!email) {
    errores.push("El correo no puede estar vacío.");
    return errores;
  }

  if (email.length > 150) {
    errores.push("El correo no debe superar 150 caracteres.");
  }

  const patron = /^[\w.-]+@[\w.-]+\.\w+$/;

  if (!patron.test(email)) {
    errores.push("El correo no tiene un formato válido.");
  }

  return errores;
}

function validarPasswordRegistro(password) {
  const errores = [];

  if (!password) {
    errores.push("La contraseña no puede estar vacía.");
    return errores;
  }

  if (password.length < 8) {
    errores.push("La contraseña debe tener mínimo 8 caracteres.");
  }

  if (new TextEncoder().encode(password).length > 72) {
    errores.push("La contraseña no debe superar 72 bytes.");
  }

  if (!/[A-Z]/.test(password)) {
    errores.push("La contraseña debe tener al menos una mayúscula.");
  }

  if (!/[a-z]/.test(password)) {
    errores.push("La contraseña debe tener al menos una minúscula.");
  }

  if (!/[0-9]/.test(password)) {
    errores.push("La contraseña debe tener al menos un número.");
  }

  return errores;
}

function validarPasswordLogin(password) {
  const errores = [];

  if (!password) {
    errores.push("La contraseña no puede estar vacía.");
  }

  if (new TextEncoder().encode(password).length > 72) {
    errores.push("La contraseña no debe superar 72 bytes.");
  }

  return errores;
}

function validarUsuarioOCorreo(valor) {
  const errores = [];

  if (!valor) {
    errores.push("Ingresa tu usuario o correo.");
    return errores;
  }

  if (valor.includes("@")) {
    errores.push(...validarCorreo(valor));
  } else {
    if (valor.length < 3) {
      errores.push("El usuario debe tener mínimo 3 caracteres.");
    }

    if (valor.length > 50) {
      errores.push("El usuario no debe superar 50 caracteres.");
    }

    if (!/^[a-zA-Z0-9]+$/.test(valor)) {
      errores.push("El usuario solo puede contener letras y números.");
    }
  }

  return errores;
}


// ==========================
// GENERAR USUARIO ALFANUMÉRICO
// ==========================

function generarCodigo(longitud = 4) {
  const caracteres = "abcdefghijklmnopqrstuvwxyz0123456789";
  let codigo = "";

  for (let i = 0; i < longitud; i++) {
    const indice = Math.floor(Math.random() * caracteres.length);
    codigo += caracteres[indice];
  }

  return codigo;
}

function generarUsuarioDesdeCorreo(email) {
  let base = email.trim().toLowerCase().split("@")[0];

  base = base.replace(/[^a-z0-9]/g, "");

  if (base.length < 3) {
    base = "usuario";
  }

  base = base.slice(0, 12);

  return base + generarCodigo(4);
}


// ==========================
// LOCALSTORAGE USUARIOS
// ==========================

function obtenerUsuarios() {
  return JSON.parse(localStorage.getItem("usuarios")) || [];
}

function guardarUsuarios(usuarios) {
  localStorage.setItem("usuarios", JSON.stringify(usuarios));
}

function correoExiste(email) {
  const usuarios = obtenerUsuarios();

  return usuarios.some(function (usuario) {
    return usuario.email === email;
  });
}

function usuarioGeneradoExiste(usuarioGenerado) {
  const usuarios = obtenerUsuarios();

  return usuarios.some(function (usuario) {
    return usuario.usuarioGenerado === usuarioGenerado;
  });
}

function generarUsuarioUnico(email) {
  let usuarioGenerado;

  do {
    usuarioGenerado = generarUsuarioDesdeCorreo(email);
  } while (usuarioGeneradoExiste(usuarioGenerado));

  return usuarioGenerado;
}


// ==========================
// REGISTRO
// ==========================

function registrarse() {
  const email = document.getElementById("emailRegistro").value.trim().toLowerCase();
  const password = document.getElementById("passwordRegistro").value;
  const confirmarPassword = document.getElementById("confirmarPassword").value;

  let errores = [];

  errores.push(...validarCorreo(email));
  errores.push(...validarPasswordRegistro(password));

  if (password !== confirmarPassword) {
    errores.push("Las contraseñas no coinciden.");
  }

  if (correoExiste(email)) {
    errores.push("Ese correo ya está registrado.");
  }

  if (errores.length > 0) {
    alertaError(errores);
    return;
  }

  const usuarioGenerado = generarUsuarioUnico(email);

  const usuarios = obtenerUsuarios();

  usuarios.push({
    email: email,
    password: password,
    usuarioGenerado: usuarioGenerado
  });

  guardarUsuarios(usuarios);

  alertaExito(
    "Cuenta creada",
    `
      Cuenta creada correctamente.<br><br>
      Tu usuario generado es:<br>
      <strong>${usuarioGenerado}</strong><br><br>
      Simulación: el usuario fue enviado al correo registrado.
    `
  );

  document.getElementById("emailRegistro").value = "";
  document.getElementById("passwordRegistro").value = "";
  document.getElementById("confirmarPassword").value = "";

  document.getElementById("formLogin").classList.add("activo");
  document.getElementById("formRegistro").classList.remove("activo");

  document.getElementById("tabLogin").classList.add("activo");
  document.getElementById("tabRegistro").classList.remove("activo");
}


// ==========================
// LOGIN
// ==========================

function iniciarSesion() {
  const usuarioOCorreo = document.getElementById("usuarioOCorreo").value.trim().toLowerCase();
  const password = document.getElementById("passwordLogin").value;

  let errores = [];

  errores.push(...validarUsuarioOCorreo(usuarioOCorreo));
  errores.push(...validarPasswordLogin(password));

  if (errores.length > 0) {
    alertaError(errores);
    return;
  }

  const usuarios = obtenerUsuarios();

  const usuarioEncontrado = usuarios.find(function (usuario) {
    return (
      (usuario.email === usuarioOCorreo || usuario.usuarioGenerado === usuarioOCorreo) &&
      usuario.password === password
    );
  });

  if (!usuarioEncontrado) {
    alertaError(["Usuario, correo o contraseña incorrectos."]);
    return;
  }

  Swal.fire({
    icon: "success",
    title: "Inicio de sesión correcto",
    text: "Entrando a pacientes...",
    timer: 1200,
    showConfirmButton: false
  }).then(function () {
    window.location.href =
      "pacientes.html?email=" +
      encodeURIComponent(usuarioEncontrado.email) +
      "&usuario=" +
      encodeURIComponent(usuarioEncontrado.usuarioGenerado);
  });
}