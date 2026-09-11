/**
 * Crea el Google Form "Evaluación del Equipo · ETC 88" (formato ABIERTO) y su hoja de respuestas.
 *
 * CÓMO USARLO (una sola vez, desde tu cuenta de Google):
 *   1. Entra a https://script.google.com  →  "Nuevo proyecto".
 *   2. Borra lo que trae, pega este archivo completo y guarda (Ctrl+S).
 *   3. Arriba, elige la función  crearFormEvaluacionETC88  y pulsa ▶ Ejecutar.
 *   4. La primera vez te pide permisos (Forms, Sheets, Drive) → Permitir.
 *   5. Abre "Registro de ejecución" (abajo): ahí salen el ENLACE PARA COMPARTIR,
 *      el enlace de edición y la hoja de respuestas.
 *
 * Fuente del contenido: preparacion/EVALUACION_EQUIPO_ETC88.md (decisión del director, 11-sep-2026).
 */
function crearFormEvaluacionETC88() {
  var form = FormApp.create('Evaluación del Equipo · ETC 88');

  form.setDescription(
    '¡Paz y bien! El ETC 88 ya pasó y queremos escucharte. Este formulario es para el equipo que sirvió. ' +
    'No hay respuestas correctas ni incorrectas: cuéntanos con libertad lo que viste y lo que viviste. ' +
    'Lo que escribas es lo que usamos para preparar mejor el ETC 89. ¡Gracias por tu servicio!'
  );

  // ---- ABIERTO: sin login, sin correo, sin límite de una respuesta por persona ----
  form.setCollectEmail(false);
  form.setLimitOneResponsePerUser(false);   // si se limita a 1, Google obliga a iniciar sesión
  try { form.setRequireLogin(false); } catch (e) { /* en cuentas Gmail ya es abierto; ignorar */ }
  form.setAllowResponseEdits(false);
  form.setShowLinkToRespondAgain(false);
  form.setConfirmationMessage('¡Gracias por tu servicio y por tu sinceridad! Lo que escribiste nos ayuda a preparar el ETC 89.');

  // 1. Nombre (opcional)
  form.addTextItem()
    .setTitle('Tu nombre')
    .setHelpText('Opcional — puedes responder de forma anónima.')
    .setRequired(false);

  // 2. Área
  form.addMultipleChoiceItem()
    .setTitle('¿En qué área serviste?')
    .setChoiceValues([
      'Dirección', 'Asesores', 'Asesores Espirituales', 'Guías',
      'Cocina', 'Música', 'Asesoras de Cocina', 'Asesores de comunidad'
    ])
    .setRequired(true);

  // 3. Mejoras / observaciones
  form.addParagraphTextItem()
    .setTitle('Oportunidades de mejora y observaciones')
    .setHelpText('¿Qué viste que se puede hacer mejor en el próximo ETC? Cuéntanos lo que observaste — organización, logística, comunicación, lo que sea que te haya llamado la atención.')
    .setRequired(true);

  // 4. Buenas prácticas
  form.addParagraphTextItem()
    .setTitle('Buenas prácticas')
    .setHelpText('¿Qué funcionó bien y debemos seguir haciendo?')
    .setRequired(true);

  // 5. Experiencia espiritual
  form.addParagraphTextItem()
    .setTitle('Tu experiencia espiritual')
    .setHelpText('¿Cómo te sentiste sirviendo en este ETC? ¿Sentiste a Dios en tu servicio? ¿Qué fruto te llevas?')
    .setRequired(true);

  // ---- Hoja de respuestas vinculada (igual que los otros forms del ETC 88) ----
  var ss = SpreadsheetApp.create('Evaluación del Equipo · ETC 88 (Respuestas)');
  form.setDestination(FormApp.DestinationType.SPREADSHEET, ss.getId());

  // ---- (Opcional) mover Form y hoja a la carpeta donde viven los otros forms del ETC 88 ----
  // Es la carpeta de "Formulario pre-formación · Equipo ETC 88" y "Perfil del Participante - ETC 88".
  // Si no quieres moverlos, comenta o borra este bloque.
  try {
    var carpeta = DriveApp.getFolderById('1Ik0_IY9WK3EplSZhSQjokJn2826FGayt');
    DriveApp.getFileById(form.getId()).moveTo(carpeta);
    DriveApp.getFileById(ss.getId()).moveTo(carpeta);
  } catch (e) {
    Logger.log('No se movió a la carpeta (no pasa nada): ' + e);
  }

  Logger.log('ENLACE PARA COMPARTIR (equipo):  ' + form.getPublishedUrl());
  Logger.log('Enlace de edición (tú):          ' + form.getEditUrl());
  Logger.log('Hoja de respuestas:              ' + ss.getUrl());
}
