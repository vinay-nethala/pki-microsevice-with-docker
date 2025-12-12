\# PKI \& TOTP Two-Factor Authentication Service



!\[Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge\&logo=python\&logoColor=white)

!\[FastAPI](https://img.shields.io/badge/FastAPI-0.95+-009688?style=for-the-badge\&logo=fastapi\&logoColor=white)

!\[Docker](https://img.shields.io/badge/Docker-Container-2496ED?style=for-the-badge\&logo=docker\&logoColor=white)

!\[Security](https://img.shields.io/badge/RSA-4096-red?style=for-the-badge)



\## 📋 Project Overview



This project implements a secure, containerized microservice that demonstrates enterprise-grade security practices. It combines \*\*Public Key Infrastructure (PKI)\*\* for secure seed transmission and \*\*Time-based One-Time Password (TOTP)\*\* for user authentication.



The service is built with \*\*FastAPI\*\*, containerized with \*\*Docker\*\*, and includes an automated \*\*Cron\*\* job for background auditing.



\### Key Features

\* \*\*Asymmetric Encryption:\*\* Uses RSA 4096-bit encryption (OAEP padding) to securely receive TOTP seeds.

\* \*\*2FA Implementation:\*\* Generates and verifies standard 6-digit TOTP codes (SHA-1, 30s period).

\* \*\*Persistence:\*\* Docker volumes ensure seed data and logs survive container restarts.

\* \*\*Automated Logging:\*\* A background cron job generates and logs valid 2FA codes every minute.

\* \*\*Security:\*\* Implements input validation via Pydantic models and strict error handling.



---



\## 🛠️ Technology Stack



\* \*\*Language:\*\* Python 3.11

\* \*\*Framework:\*\* FastAPI + Uvicorn

\* \*\*Containerization:\*\* Docker \& Docker Compose

\* \*\*Cryptography:\*\* `cryptography` library (RSA-PSS, RSA-OAEP)

\* \*\*TOTP:\*\* `pyotp` library

\* \*\*Task Scheduling:\*\* Linux Cron



---



\## 📂 Project Structure



```text

PKI-2FA-Service/

├── app/

│   ├── main.py              # FastAPI application entry point

│   ├── models.py            # Pydantic data models

│   ├── crypto\_utils.py      # RSA decryption logic

│   └── totp\_utils.py        # TOTP generation \& verification logic

├── cron/

│   └── 2fa-cron             # Cron job definition (LF line endings)

├── scripts/

│   ├── generate\_keys.py     # Setup: Generates RSA keypair

│   ├── request\_seed.py      # Setup: Requests encrypted seed from API

│   ├── log\_2fa\_cron.py      # Runtime: Script executed by cron

│   └── generate\_proof.py    # Submission: Generates signed commit proof

├── Dockerfile               # Multi-stage Docker build

├── docker-compose.yml       # Service orchestration and volumes

├── requirements.txt         # Python dependencies

└── README.md                # Project documentation

