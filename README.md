# QuickKart

A **self‑contained, laptop‑friendly micro‑commerce demo** built to satisfy the Seneca SOA course project.  Four tiny FastAPI services, wired together with Docker Compose (Part 1) and Kubernetes on Minikube (Part 2‑4), demonstrate modern container, CI/CD, and observability practices without heavyweight cloud dependencies.

---

## ✨ Features

| Capability       | How it’s delivered                                                  |
| ---------------- | ------------------------------------------------------------------- |
| **User auth**    | *User Service* — JWT sign‑up/login, bcrypt‑hashed passwords         |
| **Catalog**      | *Product Service* — CRUD products & categories                      |
| **Checkout**     | *Order Service* — cart ➜ order ➜ status, calls User & Product       |
| **Email notice** | *Notification Service* — fires confirmation e‑mails through MailHog |

Everything runs from a single `docker compose up` or `make dev` command.

---

## 🛠 Tech Stack

* **Python 3.11 / FastAPI** ‑ ultra‑light REST layer, auto‑docs via OpenAPI
* **SQLite** per service (swap‑ready for Postgres)
* **Docker & Compose** — local dev / grading
* **Kubernetes 1.30** on **Minikube** — orchestration, HPA, RBAC
* **GitHub Actions** — lint → test → build → push → `kubectl apply`
* **Prometheus + Grafana** — metrics; **Fluent Bit → Loki** — logs (Milestone 3)

---

## 🤝 Contributing

1. Fork ➜ feature branch ➜ PR
2. `pre‑commit install` to auto‑format with Black & Ruff
3. Every PR must keep `docker compose up` green & tests passing.

---

## 📜 License

MIT (see `LICENSE`).
