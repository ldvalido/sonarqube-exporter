import requests
import json
import sys

print(sys.argv[1])
print(sys.argv[2])
print(sys.argv[3])
print(sys.argv[4])


# Configuración
#SONAR_URL = "http://localhost:9000"
#PROJECT_KEY = "Sonar-Qube-Exporter"
#SONAR_TOKEN = "squ_0cdd9defa99004c6940bc2d16e6997f966ba5984"

SONAR_URL = sys.argv[1]
PROJECT_KEY = sys.argv[2]
SONAR_TOKEN = sys.argv[3]
OUTPUT_FILE = sys.argv[4]
# Encabezados para la autenticación en SonarQube
headers_sonar = {
    'Authorization': f'Bearer {SONAR_TOKEN}'
}
params = {"componentKey":PROJECT_KEY}
headers = {"Authorization": f"Bearer {SONAR_TOKEN}"}
metrics_url = f"{SONAR_URL}/api/measures/component?component={PROJECT_KEY}&metricKeys=coverage,bugs,code_smells,vulnerabilities"

response = requests.get(metrics_url, auth=(SONAR_TOKEN,""))
# Obtener métricas del proyecto
metrics_data = response.json()

# Obtener incidencias del proyecto
issues_url = f"{SONAR_URL}/api/issues/search?componentKeys={PROJECT_KEY}&resolved=false"
response = requests.get(issues_url, auth=(SONAR_TOKEN,""))
issues_data = response.json()

# Obtener estado del Quality Gate
quality_gate_url = f"{SONAR_URL}/api/qualitygates/project_status?projectKey={PROJECT_KEY}"
response = requests.get(quality_gate_url, auth=(SONAR_TOKEN,""))
quality_gate_data = response.json()

# Preparar datos para el informe
data = {
    "metrics": metrics_data,
    "issues": issues_data,
    "quality_gate": quality_gate_data
}

extract_data = json.dumps(data, indent=2)

with open(OUTPUT_FILE, 'w') as f:
    json.dump(data, f, ensure_ascii=False)