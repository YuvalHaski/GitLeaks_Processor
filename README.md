
# **Gitleaks Processor**

A Dockerized Python application that integrates [Gitleaks](https://github.com/zricethezav/gitleaks), a secret-detection tool, with advanced error handling and result transformation capabilities. This project allows you to scan Git repositories for secrets and outputs the findings in a structured JSON format.

---

## **Features**
- **Flexible Command Support:** Pass Gitleaks-compatible commands to customize scanning behavior.
- **Error Handling:** Comprehensive error detection and logging for runtime issues.
- **Result Transformation:** Converts Gitleaks raw JSON output into a structured format.
- **Dockerized Environment:** Ensures reproducibility and easy setup.
- **Log Management:** Maintains detailed logs for debugging and audit purposes.

---

## **Getting Started**

### **Prerequisites**
- [Docker](https://docs.docker.com/get-docker/) installed on your system.
- A Git repository to scan, either locally cloned or accessible via URL.

---

### **Installation**
1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>

### **Build the Docker Image**
   ```bash
    docker build -t gitleaks-python .
