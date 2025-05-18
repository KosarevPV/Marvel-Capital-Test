# Log Analysis Service README

## Overview

This project provides a log analysis service that processes application logs, stores incident data, and visualizes summaries through a Grafana dashboard. The system is designed for one-time processing of a log file, inserting detected incidents into a PostgreSQL database, which Grafana then visualizes.

Currently, the setup includes:
- **PostgreSQL**: stores incident records.
- **Grafana**: visualizes the data from PostgreSQL.
- **Processing Script**: processes a downloaded log file, detects incidents, and inserts them into PostgreSQL.


---

## How to Run

### Prerequisites
- Docker and Docker Compose installed on your system.
- A log file downloaded manually or via the script.

### Step-by-step Instructions

1. **Clone the repository (if applicable):**
```bash
git clone <repository_url>
cd <repository_directory>
```

2. **Build and start the environment:**
```bash
docker compose up -d
```

3. **Grafana:**
- Open your browser and go to `http://localhost:3000`.
- Follow the link http://localhost:3000/dashboards to view the dashboard.

---

## Potential Improvements and Future Features
### 1. Live Log Monitoring
- Implement real-time or near-real-time log ingestion:
  - Continuously tail the log file.
  - Incrementally process new entries.
  - Update the PostgreSQL database and dashboards dynamically.
- Possible tools:
  - Log shippers (e.g., Filebeat).
  - Stream processing (e.g., Kafka, Logstash).

### 2. Automated Incident Detection
- Integrate ML-based anomaly detection models.
- Use LLMs for summarization and insight generation.
- Set up alerting mechanisms based on detected critical events.

### 3. Enhanced Dashboard Features
- Add interactive filters and drill-down capabilities.
- Visualize trends over time.
- Highlight anomalies or critical incidents automatically.