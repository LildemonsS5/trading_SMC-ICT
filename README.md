
SMC Trading App

Aplicación para análisis de trading basado en Smart Money Concepts (SMC) e Inner Circle Trader (ICT). El proyecto consta de un backend en Python (FastAPI) y un frontend en React, desplegados en Render.com.

Estructura del Proyecto

smc-trading-app/
├── backend/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── models.py
│   │   ├── strategy.py
│   │   └── utils.py
│   ├── main.py
│   ├── requirements.txt
│   └── README.md
├── frontend/
│   ├── public/
│   │   ├── index.html
│   │   └── favicon.ico
│   ├── src/
│   │   ├── components/
│   │   │   ├── AnalysisForm.jsx
│   │   │   ├── AnalysisResults.jsx
│   │   │   └── Header.jsx
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── index.js
│   ├── package.json
│   └── README.md
├── README.md
└── .gitignore

Requisitos





Backend: Python 3.8+, FastAPI, Uvicorn, pandas, numpy, requests, python-dateutil, pytz, python-multipart



Frontend: Node.js 16+, React, Tailwind CSS



Render.com: Cuenta para desplegar el backend (Web Service) y el frontend (Static Site)



GitHub: Repositorio para alojar el código

Configuración Local

Backend





Navega al directorio backend/:

cd backend



Instala las dependencias:

pip install -r requirements.txt



Configura la variable de entorno API_KEY con tu clave de Financial Modeling Prep.



Ejecuta el servidor:

uvicorn main:app --host 0.0.0.0 --port 8000 --reload



Prueba la API en http://localhost:8000/docs.

Frontend





Navega al directorio frontend/:

cd frontend



Instala las dependencias:

npm install



Configura la variable de entorno REACT_APP_API_URL en un archivo .env (por ejemplo, REACT_APP_API_URL=http://localhost:8000).



Ejecuta el frontend:

npm start



Abre http://localhost:3000 en tu navegador.

Despliegue en Render.com

Backend (Web Service)





Crea un nuevo Web Service en Render.com.



Conecta tu repositorio de GitHub y selecciona la rama main.



Configura:





Root Directory: backend



Runtime: Python



Build Command: pip install -r requirements.txt



Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT



Agrega la variable de entorno:





Key: API_KEY



Value: Tu clave de Financial Modeling Prep



Despliega y anota la URL generada (por ejemplo, https://smc-trading-backend.onrender.com).

Frontend (Static Site)





Crea un nuevo Static Site en Render.com.



Conecta el mismo repositorio de GitHub y selecciona la rama main.



Configura:





Root Directory: frontend



Build Command: npm install && npm run build



Publish Directory: frontend/build



Agrega la variable de entorno:





Key: REACT_APP_API_URL



Value: La URL del backend (por ejemplo, https://smc-trading-backend.onrender.com)



Despliega y accede a la URL del frontend (por ejemplo, https://smc-trading-frontend.onrender.com).

Configuración de CORS

El backend incluye soporte para CORS, configurado para permitir solicitudes desde la URL del frontend. Asegúrate de actualizar la configuración de CORS en backend/main.py con la URL del frontend desplegado.

Notas





La API key debe mantenerse segura y configurarse como variable de entorno en Render.



En el plan gratuito de Render, el backend puede "dormirse" tras un período de inactividad, lo que puede causar demoras iniciales.



Asegúrate de que el repositorio en GitHub esté configurado como público o que Render tenga acceso si es privado.
