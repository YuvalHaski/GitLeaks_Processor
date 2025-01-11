# **Gitleaks Processor**

### **Overview**
This project is a Docker-based solution that wraps **Gitleaks**, an open-source secret-detection tool, with a Python script to process its output into a structured JSON format. The goal is to simplify secret detection by providing clear, actionable, and well-formatted results.

---

### **Features**
- **Secret Detection**: Utilizes Gitleaks to scan repositories for potential secrets.
- **Output Transformation**: Converts Gitleaks raw JSON output into a structured format.
- **Error Handling**: Outputs structured error messages when issues occur.
- **Dockerized Workflow**: Enables seamless usage through a Docker container that integrates Gitleaks and Python.
- **Log Management:** Maintains detailed logs for debugging and audit purposes.

---

### **Prerequisites**
- [Docker](https://docs.docker.com/get-docker/) installed on your system.

---

## **Setup Instructions**

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Build the Docker Image
   ```bash
    docker build -t gitleaks-python .
   ```

---

## **Running the Docker Container**

To scan the current directory and process the results:
   ```bash
   docker run --rm -v "$(pwd):/code" gitleaks-python gitleaks detect --no-git --report-path /code/<name-of-output-file>.json /code
   ```



