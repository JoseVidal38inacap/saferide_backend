# SafeRide – Backend de Monitoreo de Viajes  
Proyecto desarrollado en Django REST Framework con arquitectura basada en microservicios, comunicación mediante eventos (Kafka simulado) y servidor HTTPS local con certificado digital.

---

## 🚀 Descripción del Proyecto
SafeRide es una plataforma de backend destinada al monitoreo de viajes de transporte seguro.  
Incluye:
- API REST completa con modelos CRUD de Pasajeros, Conductores, Vehículos, Viajes y Pagos.
- Arquitectura basada en microservicios independientes (Route, Notifier, Billing).
- Simulación de mensajería tipo Kafka para el disparo de eventos.
- Documentación automática con Swagger (OpenAPI 3).
- Servidor HTTPS local con certificado autofirmado.

---

## 📂 Estructura del Proyecto
saferide_backend/
│
├── accounts/ # Usuarios (Django)
├── common/ # Funciones compartidas
├── microservices/ # Servicios simulados (route, notifier, billing)
├── payments/ # CRUD de pagos
├── trips/ # CRUD de viajes
├── passengers/ # CRUD de pasajeros
├── vehicles/ # CRUD de vehículos
│
├── templates/common/ # Landing page
├── certs/ # Certificados locales (no incluidos en el repo)
│
├── db.sqlite3 # Base de datos local (ignorada en Git)
├── manage.py
└── generate_cert.py # Script para crear certificados

---

## 🧰 Requisitos Previos

### Software necesario
- Python 3.11+
- pip
- virtualenv (opcional)
- Navegador compatible con HTTPS local

---

## 🔧 Instalación

### 1️⃣ Clonar el repositorio
git clone https://github.com/Usuario/saferide_backend.git

cd saferide_backend

### 2️⃣ Crear entorno virtual
python -m venv venv
venv\Scripts\activate # Windows

### 3️⃣ Instalar dependencias
pip install -r requirements.txt

### 4️⃣ Ejecutar migraciones
python manage.py migrate

### 5️⃣ Crear superusuario
python manage.py createsuperuser

---

## 🔐 HTTPS — Certificado Digital

El servidor corre en **https://localhost:8443**.

Para generarlo nuevamente:
python generate_cert.py

Archivos generados:
- `certs/saferide.crt`
- `certs/saferide.key`

**Importante:** estos archivos NO se suben a GitHub.

Para iniciar el servidor HTTPS:
python manage.py runsslserver 0.0.0.0:8443 --certificate certs/saferide.crt --key certs/saferide.key

---

## 🧩 Microservicios SafeRide

Los microservicios se ejecutan individualmente:

### Route Service (Puerto 8001)
python microservices/route_service.py

### Notifier Service (Puerto 8002)
python microservices/notifier_service.py

### Billing Service (Puerto 8003)
python microservices/billing_service.py

Cada servicio tiene un endpoint:
http://localhost:8001/health

http://localhost:8002/health

http://localhost:8003/health

---

## 📘 Documentación: Swagger (OpenAPI 3)

Disponible en:
https://localhost:8443/api/docs/

Incluye rutas completas de:
- Passengers
- Drivers
- Vehicles
- Trips
- Payments

---

## 🔄 Endpoints Principales

Ejemplos:

### Pasajeros
GET /api/passengers/
POST /api/passengers/

### Conductores
GET /api/drivers/
POST /api/drivers/

### Viajes
GET /api/trips/
POST /api/trips/

---

## 🧪 Pruebas Realizadas

- Pruebas manuales con la interfaz de Django REST Framework.
- Pruebas en Swagger.
- Verificación de HTTPS activo.
- Creación de registros por POST.
- Confirmación de almacenamiento via GET después del POST.
- Disparo de evento Kafka simulado al crear un viaje.
- Microservicios respondiendo estado saludable vía health check.


