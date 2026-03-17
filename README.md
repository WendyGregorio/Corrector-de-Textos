# Corrector de Textos IA - Gemini 2.5 Flash

Esta es una aplicación web completa desarrollada para procesar y mejorar textos en español utilizando Inteligencia Artificial (Google Gemini 2.5 Flash). Permite a los usuarios seleccionar diferentes niveles de corrección (ortografía, estilo, tono formal o informal) y proporciona el texto corregido junto con una explicación de los cambios realizados.

## 🚀 Tecnologías Utilizadas

- **Backend:** Python con Flask.
- **IA:** Google Gemini API (`google-genai` con `gemini-2.5-flash`).
- **Frontend:** HTML5, CSS3 (Vanilla, Dark Mode, Glassmorphism), JavaScript (Vanilla, Fetch API).

---

## 🛠️ Parámetros de la Aplicación

La comunicación entre el Frontend y el Backend se realiza mediante JSON a través de una petición `POST` al endpoint `/api/corregir`.

### 1. Parámetros de Entrada (Frontend -> Backend)

| Nombre | Tipo de Dato | Descripción | Validaciones | Uso en el Prompt |
| :--- | :--- | :--- | :--- | :--- |
| `texto` | String | El texto original escrito por el usuario. | No debe estar vacío ni ser nulo. | Se inserta directamente en el bloque "Texto original" del prompt. |
| `nivel_correccion` | String | El nivel de mejora deseado. | Debe ser uno de: `ortografia`, `estilo`, `formal`, `informal`. | Se le indica a la IA como la instrucción principal de qué aspecto mejorar. |

### 2. Parámetros de Salida (Backend -> Frontend)

| Formato de Respuesta | Campos Devueltos | Visualización en la Interfaz | Manejo de Errores |
| :--- | :--- | :--- | :--- |
| **JSON** | `texto_corregido` (String): El texto final mejorado. <br> `explicacion` (String): Detalle de por qué se hicieron los cambios. | Se inyectan dinámicamente en visualizadores de texto (`<div>` o `<p>`) en la "Sección de Resultados". | Si ocurre un error, en lugar de estas claves, el backend devuelve un JSON con la clave `{"error": "mensaje"}` con status 400 o 500. El frontend lo captura y muestra una "Sección de Error" roja. |

---

## 🧠 Estructura del Prompt

El prompt se divide en dos partes: Instrucciones de Sistema (System Instruction) y el Prompt del Usuario. Se envía forzando el formato `response_mime_type="application/json"` para garantizar una respuesta parseable en el backend.

### Construcción:

**System Instruction:**
Define el rol de la IA y el esquema estricto de la respuesta JSON esperada.

```text
Eres un experto editor y corrector de textos en español. Tu tarea es corregir el texto provisto por el usuario basándote en el nivel de corrección solicitado. Devuelve la respuesta estrictamente en formato JSON válido con las siguientes claves: 'texto_corregido' (string con la versión final) y 'explicacion' (string detallando los cambios importantes realizados).
```

**Prompt del Usuario:**
Aquí es donde se insertan los parámetros de entrada de forma dinámica (usando `f-strings` en Python).

```text
Texto original:
"{texto_original}"

Nivel de corrección deseado: {nivel_correccion}.
Aplica las correcciones necesarias según el nivel solicitado.
```

### Ejemplo Real Enviado a Gemini

**Datos del Usuario:**
- Texto: `"ola komo estas llo muy bn espero k tu tb"`
- Nivel de corrección: `"ortografia"`

**Prompt resultante evaluado:**
```text
Texto original:
"ola komo estas llo muy bn espero k tu tb"

Nivel de corrección deseado: ortografia.
Aplica las correcciones necesarias según el nivel solicitado.
```

---

## 📂 Estructura del Proyecto

El proyecto está organizado de la siguiente manera:

```text
corrector-textos/
│
├── .env                # Archivo oculto con las variables de entorno (API Key)
├── app.py              # Script principal del servidor backend (Flask)
├── requirements.txt    # Dependencias del proyecto Python
│
├── static/
│   ├── script.js       # Lógica del cliente, fetch API, DOM manipulation
│   └── styles.css      # Estilos visuales modernos, animaciones, dark mode
│
└── templates/
    └── index.html      # Estructura de la aplicación web
```

---

## ⚙️ Instrucciones de Ejecución Paso a Paso

Sigue estos pasos para ejecutar la aplicación de forma local.

### 1. Preparación del Entorno
Es una buena práctica utilizar un entorno virtual de Python.
```bash
# Navegar a la carpeta del proyecto
cd c:\Users\wendy\.gemini\antigravity\playground\harmonic-flare\corrector-textos

# Crear un entorno virtual (opcional pero recomendado)
python -m venv venv

# Activar el entorno (En Windows):
venv\Scripts\activate

# (En Mac/Linux usa: source venv/bin/activate)
```

### 2. Instalación de Dependencias
Instala las librerías necesarias con `pip`.
```bash
pip install -r requirements.txt
```

### 3. Configuración de la API Key (.env)
El proyecto ya cuenta con un archivo `.env` configurado.
La clave de la API se almacena en este archivo y es leída automáticamente gracias a `python-dotenv`.
El archivo `corrector-textos/.env` tiene la estructura:
```env
GEMINI_API_KEY=tu_api_key_aqui
```
*(Nota: Ya he insertado la Key proporcionada por ti en el archivo .env del proyecto).*

### 4. Iniciar el Servidor Flask
Para arrancar el backend y que empiece a escuchar peticiones:
```bash
python app.py
```
Verás un mensaje en la consola indicando que el servidor se está ejecutando, generalmente en: `http://127.0.0.1:5000`

### 5. Probar la Aplicación
Abre tu navegador de preferencia y visita: [http://127.0.0.1:5000](http://127.0.0.1:5000).
¡La interfaz estará lista para usarse! Pega un texto, selecciona el nivel de corrección y presiona "Corregir Texto".
