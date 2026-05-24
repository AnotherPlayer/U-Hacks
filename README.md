# U-HACKS: Asistente Virtual de Orientación Nutricional

## Reto seleccionado
**Reto 2 - Salud preventiva y bienestar**

### Objetivo
Diseñar un asistente de orientación y educación en salud, sin realizar diagnósticos médicos.

---

## Descripción del Proyecto
Este proyecto es una aplicación web interactiva desarrollada con **Streamlit** que integra un agente de Inteligencia Artificial (basado en Google Gemini). Actuando bajo la personalidad empática de una enfermera, el sistema asiste a los usuarios en la toma de decisiones sobre su alimentación, enfocándose específicamente en el **índice glucémico** y el control de porciones para el bienestar metabólico.

La arquitectura del modelo está estrictamente limitada por **reglas de seguridad clínica** (System Instructions) para prevenir la generación de diagnósticos, recetas o planes terapéuticos, derivando al usuario con profesionales de la salud cuando se detectan riesgos.

## Características Principales
1. **Asesoría Nutricional Basada en Evidencia:** Recomendaciones sobre alimentos centradas en su impacto glucémico y macronutrientes.
2. **Filtros de Seguridad Médica Constantes:** El modelo cuenta con instrucciones estrictas de rechazo seguro ("Guardrails") para evitar dar diagnósticos o indicaciones médicas operativas.
3. **Antialucinación y Transparencia:** El asistente declara su nivel de confianza y sugiere verificación con fuentes oficiales ante la incertidumbre.
4. **Extracción de Datos Estructurados (SQL):** Al finalizar cada asesoría, el agente genera automáticamente un query SQL (`INSERT INTO alimentos...`) estimando los macronutrientes (carbohidratos, proteínas, grasas y sodio) para registrar la consulta en la base de datos de la aplicación.

## 🛠️ Tecnologías y Herramientas Utilizadas
* **Frontend y Backend:** Python con el framework web **Streamlit**.
* **Inteligencia Artificial:** Google AI Studio (Modelo Gemini) con Prompt Engineering avanzado (estructuración mediante etiquetas XML).
* **Base de Datos:** SQL (Esquema relacional para la tabla `alimentos`).

## ⚙️ Instalación y Configuración (Entorno de Desarrollo)

1. Clona este repositorio:
   ```bash
   git clone [https://github.com/tu-usuario/u-hacks.git](https://github.com/tu-usuario/u-hacks.git)
   cd u-hacks