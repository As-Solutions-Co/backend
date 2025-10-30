* Microservicios a construir
* Casos de uso
* Entidades principales
* Orden lógico de desarrollo
* Sugerencias técnicas y prácticas

---

## 🧭 **Etapa 0 – Planeación y Setup inicial**

### 🎯 Objetivo

Definir base técnica, entorno y convenciones.

### 🔧 Tareas

1. Crear un monorepo:

   ```
   school-platform/
     ├── services/
     ├── infra/
     ├── docker-compose.yml
     └── .env
   ```
2. Configurar herramientas:

    * Go ≥ 1.22
    * Docker y Docker Compose
    * Postgres y RabbitMQ
3. Crear **plantilla base de microservicio**, con:

    * `cmd/api/main.go`
    * `internal/bootstrap`
    * `internal/domain`, `application`, `infrastructure`
    * `.env`, `Dockerfile`, `Makefile`
4. Configurar logs, manejo de errores y variables de entorno.

### ✅ Resultado

Una plantilla **reutilizable** para todos los servicios.

---

## 🧩 **Etapa 1 – Microservicio `students-service`**

### 🎯 Objetivo

Gestión básica de estudiantes y acudientes.

### 🧱 Entidades

| Entidad      | Descripción                         | Relaciones                  |
| ------------ | ----------------------------------- | --------------------------- |
| `Student`    | Datos básicos del estudiante        | N:1 `Guardian`              |
| `Guardian`   | Acudiente del estudiante            | 1:N `Student`               |
| `Enrollment` | Matrícula de estudiante en un curso | 1:1 `Student`, N:1 `Course` |

### ⚙️ Casos de uso

* Registrar estudiante nuevo
* Asociar acudiente
* Consultar lista de estudiantes
* Registrar matrícula

### 💬 Comunicación

* Expone API REST (`/students`, `/guardians`)
* Publica evento RabbitMQ:

  ```json
  { "event": "StudentRegistered", "data": { "student_id": "...", "email": "..." } }
  ```

### ✅ Resultado

Primer servicio funcional con API, PostgreSQL y emisión de eventos.

---

## 📘 **Etapa 2 – Microservicio `academics-service`**

### 🎯 Objetivo

Gestión de cursos y calificaciones.

### 🧱 Entidades

| Entidad   | Descripción                                     |
| --------- | ----------------------------------------------- |
| `Course`  | Curso (por ejemplo “Grado 10A”)                 |
| `Subject` | Asignatura (Matemáticas, Lengua, etc.)          |
| `Grade`   | Calificación de un estudiante en una asignatura |
| `Teacher` | Docente asignado a un curso                     |

### ⚙️ Casos de uso

* Crear curso y asignaturas
* Asignar docente a curso
* Registrar calificaciones
* Consultar calificaciones por estudiante

### 💬 Comunicación

* Expone API REST (`/courses`, `/grades`)
* Consume evento `StudentRegistered` (para crear registro académico en blanco).

---

## 📨 **Etapa 3 – Microservicio `communication-service`**

### 🎯 Objetivo

Enviar notificaciones internas o por correo.

### 🧱 Entidades

| Entidad        | Descripción                                           |
| -------------- | ----------------------------------------------------- |
| `Message`      | Mensaje interno entre usuarios                        |
| `Notification` | Evento para enviar correo o push                      |
| `Announcement` | Avisos globales (para todos los estudiantes o padres) |

### ⚙️ Casos de uso

* Enviar mensaje de bienvenida cuando se registre un estudiante
* Enviar aviso de nuevas calificaciones
* Consultar bandeja de notificaciones

### 💬 Comunicación

* No expone API inicial (solo RabbitMQ consumer)
* Escucha eventos:

    * `StudentRegistered`
    * `GradePublished`

### ✅ Resultado

Flujo completo asíncrono:
**StudentService → RabbitMQ → CommunicationService**

---

## 🧰 **Etapa 4 – Infraestructura y orquestación**

### 🎯 Objetivo

Preparar despliegue completo con Docker y observabilidad.

### 🔧 Tareas

1. Configurar `docker-compose.yml` con:

    * Postgres (con volumen persistente)
    * RabbitMQ (con interfaz web)
    * Los tres microservicios
2. Configurar logs (`stdout`)
3. Implementar migraciones (Flyway, Goose o simple script SQL)
4. Conectar servicios con variables `.env`
5. Opcional: añadir un `reverse-proxy` (Traefik o Nginx)

---

## 🚀 **Etapa 5 – Integración y mejora**

### 🎯 Objetivo

Refinar, probar e implementar buenas prácticas.

### 🔧 Tareas

* Pruebas unitarias en cada capa (`domain`, `application`)
* Monitoreo con Prometheus + Grafana
* Health checks y readiness endpoints
* Documentación con Swagger/OpenAPI
* Script Makefile para build/test/run

---

## 💡 **Sugerencias para desarrollar**

1. **Crea un microservicio por carpeta**
   Reutiliza la estructura base (`students-service` → copia → `academics-service`).

2. **No compartas código entre servicios**
   Si algo se repite (ej. logger, env loader), publícalo como módulo Go privado (ej: `github.com/tuusuario/shared`).

3. **Mantén servicios pequeños**
   Cada servicio debe tener un dominio claro (bounded context).

4. **Versiona las APIs**
   Ejemplo: `/api/v1/students`

5. **Evita dependencias circulares**
   Usa eventos o HTTP para comunicar, nunca llamadas directas de código.

6. **Configura todo con variables de entorno**, ej:

   ```
   DATABASE_URL=postgres://user:pass@postgres:5432/students
   RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672/
   ```

7. **Cada servicio tiene su propio Dockerfile**

   ```dockerfile
   FROM golang:1.22 AS builder
   WORKDIR /app
   COPY . .
   RUN go build -o main ./cmd/api

   FROM gcr.io/distroless/base
   COPY --from=builder /app/main /
   CMD ["/main"]
   ```

---

## 🧭 **Ruta sugerida de aprendizaje**

| Etapa | Microservicio   | Conceptos clave                    | Aprendizaje        |
| ----- | --------------- | ---------------------------------- | ------------------ |
| 0     | Base            | Configuración, 12 factores, Docker | Entorno base       |
| 1     | Students        | CRUD, capa hexagonal, eventos MQ   | Fundamentos        |
| 2     | Academics       | Comunicación síncrona/asíncrona    | Integración        |
| 3     | Communication   | Consumers, RabbitMQ                | Asincronía         |
| 4     | Infraestructura | Compose, monitoreo                 | Despliegue         |
| 5     | Mejora          | Pruebas, logs, métricas            | Profesionalización |

---
