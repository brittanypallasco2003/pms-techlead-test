# Informe de entrega

## URLs y ejecución

Dashboard Render:
API Render:

### Comandos locales, build y pruebas:

- Backend, desde la raíz: `.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000`.
- Suite backend: ``.
- Comprobación del cambio de listado: `.\.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider tests/test_api.py -k "health or list"`.
- Frontend, desde `frontend/`: `npm start`; build: `npm run build`.
- Pruebas frontend, desde `frontend/`: `npm test` (Angular CLI + Vitest, sin modo watch).

La arquitectura se está separando por módulos funcionales: `projects` y `activities`.
En el listado, el dominio define `Project` como dataclass y el contrato
`ProjectRepository`; `ListProjects` depende de ese contrato. El adaptador MongoDB
selecciona los campos necesarios y transforma documentos en entidades. El adaptador
HTTP construye `ProjectResponse`, con `budget: float`, y declara `response_model`.
`main.py` configura la aplicación y registra routers; las funciones heredadas sin
ruta se conservan en `app/legacy.py` para revisión.

Si desea cargar la fixture de demostración del repositorio en su base de prueba,
ejecute `.\.venv\Scripts\python.exe -m scripts.seed` desde la raíz. SAT debe
mostrar `3`, `2`, `35` y `66.7%`; Chatbots debe mostrar `0`, `0`, `0` y `0%`.
Cambiar de proyecto debe retirar las tarjetas mientras carga y seleccionar la
opción vacía debe limpiarlas. Detener la API y seleccionar otro proyecto permite
comprobar el error de resumen; recargar la página con la API detenida permite
comprobar el error de lista.

Las secciones siguientes conservan los hallazgos y resultados de la revisión
anterior; los resultados del frontend y del contrato HTTP actuales son los de esta
actualización.

## Hasta tres problemas prioritarios

Ubicación, evidencia, consecuencia y solución. Señale al menos una corrección
realizada y cómo la verificó.

1. **Listado sin protección del contrato de salida — corregido.** Ubicación
   original: `app/main.py:list_projects`, `app/models.py:ProjectResponse` y
   `tests/test_api.py:test_list`. El listado devolvía documentos de MongoDB tras
   cambiar únicamente `_id` por `id`, por lo que también publicaba `metadata`,
   `created_by` y cualquier campo adicional. La prueba solo comprobaba HTTP 200 y
   cantidad de proyectos. Además, el DTO de respuesta, sin utilizar, declaraba
   `budget` como cadena. Se reprodujo la exposición mediante documentos con campos
   internos. Consecuencia: incumplimiento del contrato público y prueba incapaz de
   detectar esa regresión. Solución: proyección de campos en
   `app/projects/infrastructure/persistence/mongo_project_repository.py`, entidad
   independiente y esquema de respuesta explícito en
   `app/projects/infrastructure/http/schemas.py`. La prueba reforzada compara los
   campos exactos, los datos de la fixture y el tipo numérico del presupuesto.

2. **Configuración que ignora el entorno — pendiente.** Ubicación:
   `app/config.py`. Al establecer `MONGO_URL` y `DATABASE` en un proceso temporal y
   recargar el módulo, se conservaron los valores escritos en el archivo.
   Consecuencia: configurar Atlas mediante variables en Render no cambia la
   conexión, que sigue apuntando a localhost. Solución propuesta: leer las variables
   del entorno y verificar que sus valores se respetan.

3. **Prueba heredada que solo verifica su propio mock — pendiente.** Ubicación:
   `review_examples/test_legacy_mock.py:test_repository_failure`. Configura un mock
   para devolver un diccionario con `status_code: 503` y comprueba ese mismo valor,
   sin ejecutar código productivo ni una petición HTTP. Consecuencia: no verifica
   el manejo de fallos de persistencia. Solución propuesta: provocar un fallo en la
   dependencia de persistencia y comprobar la respuesta HTTP de una ruta real.

## Despliegue y configuración


## Herramientas y pendientes

Se utilizó Codex/ChatGPT separar el listado en capas y fortalecer sus pruebas.
La modificación se verificó ejecutando pytest y consultando la API local.