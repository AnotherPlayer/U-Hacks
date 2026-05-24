## Inspiración

MediByte nació al observar que muchas personas con diabetes tipo 2 tienen dificultades para interpretar la información nutrimental de los alimentos que consumen diariamente. Aunque existen aplicaciones para contar calorías o registrar comidas, muchas veces estas herramientas no explican de manera sencilla cómo ciertos alimentos pueden afectar el control de glucosa.

Creamos una solución accesible, clara y educativa que ayudara a las personas a tomar mejores decisiones alimentarias. La idea principal fue desarrollar un agente de inteligencia artificial capaz de traducir información nutrimental compleja en recomendaciones fáciles de entender, especialmente en temas como carbohidratos, azúcares, grasas, sodio e impacto glucémico.

## ¿Qué hace?

MediByte es un agente de inteligencia artificial de asistencia nutricional para personas con diabetes tipo 2. El usuario puede escribir los alimentos que consumió, por ejemplo: “Comí una torta de jamón y tomé un refresco”, y el agente genera una interpretación clara sobre el posible impacto nutrimental de esa comida.

El sistema puede emitir advertencias sobre consumo elevado de carbohidratos, azúcares, grasas o sodio, además de sugerir alternativas más adecuadas. También contempla el registro de un historial alimentario para identificar tendencias de consumo y apoyar al usuario en el seguimiento de sus hábitos.

MediByte no sustituye a un médico o nutriólogo, sino que funciona como una herramienta de acompañamiento educativo para facilitar la comprensión de la información nutrimental.

## ¿Cómo lo construimos?

Construimos MediByte utilizando Microsoft Copilot Studio, una plataforma que permite desarrollar agentes conversacionales de inteligencia artificial de forma visual y con bajo código.

El agente se apoya en una base de conocimiento construida a partir de información validada por instituciones públicas y organizaciones especializadas en diabetes, como la Federación Mexicana de Diabetes. Esta base permite que las respuestas sean más contextualizadas, confiables y útiles para personas con diabetes tipo 2.

También diseñamos una arquitectura donde el usuario interactúa con una interfaz web o aplicación, ingresa sus alimentos por texto, el agente interpreta la información y posteriormente genera advertencias, recomendaciones y registros dentro del historial alimentario.

## Retos a los que nos enfrentamos

Uno de los principales retos fue definir correctamente el enfoque del agente. Al inicio, la idea podía interpretarse como si el modelo hubiera sido entrenado directamente con documentos, pero después ajustamos el enfoque para explicarlo de forma más correcta: MediByte no se entrena desde cero, sino que consulta una base de conocimiento validada para generar respuestas más confiables.

Otro reto fue convertir información técnica sobre nutrición, diabetes, índice glucémico y conteo de carbohidratos en mensajes simples que cualquier usuario pudiera entender. También fue importante cuidar que las recomendaciones no sonaran como diagnóstico médico, sino como orientación educativa.

Además, tuvimos que pensar en cómo organizar el flujo del sistema para que no solo respondiera preguntas, sino que también pudiera guardar información del usuario y detectar patrones de consumo.

## Logros de los que estamos orgullosos

Estamos orgullosas de haber desarrollado una propuesta con impacto social, enfocada en una problemática real: la dificultad de muchas personas para interpretar alimentos y tomar decisiones informadas cuando viven con diabetes tipo 2.

También logramos construir un agente que no se limita a contar calorías, sino que interpreta la información nutrimental en lenguaje sencillo. Otro logro importante fue integrar una base de conocimiento validada, lo cual permite que las respuestas estén mejor orientadas y no dependan únicamente de información general.

Además, MediByte combina inteligencia artificial conversacional, educación alimentaria, historial de consumo y recomendaciones personalizadas en una sola solución.

## Lo que aprendimos

Durante el desarrollo aprendimos que una solución de salud digital debe ser clara, responsable y segura. No basta con generar respuestas automáticas; es necesario cuidar el lenguaje, aclarar las limitaciones del sistema y evitar que el usuario interprete las recomendaciones como un diagnóstico médico.

También aprendimos la importancia de usar fuentes confiables, especialmente cuando se trabaja con temas relacionados con salud. Además, comprendimos mejor cómo una herramienta de inteligencia artificial puede apoyar la educación del paciente si se diseña con un enfoque humano, accesible y preventivo.

## Que sigue para MediByte

Como siguientes pasos, nos gustaría mejorar el prototipo integrando una base de datos nutrimental más amplia y verificada, para estimar con mayor precisión valores como carbohidratos, azúcares, grasas y sodio.

También buscamos fortalecer el historial alimentario para que el usuario pueda visualizar tendencias de consumo a lo largo del tiempo. A futuro, el sistema podría generar reportes de seguimiento que el usuario pueda compartir con un profesional de la salud.

Otra mejora importante sería ampliar la interfaz para hacerla más intuitiva, visual y accesible, permitiendo que más personas puedan usar MediByte como apoyo en su educación alimentaria diaria.

## Integrantes
