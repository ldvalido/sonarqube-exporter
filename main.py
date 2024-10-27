import os
import time

import prometheus_client as prom
from prometheus_client import start_http_server
from scan_metrics import common_metrics, event_metrics, get_stat, rule_metrics
from system_metrics import system_metric

from sonarqube import SonarQubeClient

sonarqube_server = os.environ.get('SONARQUBE_SERVER', 'http://sonarqube:9000')
sonarqube_token = os.environ.get('SONARQUBE_TOKEN', 'squ_eec3ed62b74368f72cd1ffdff2f69f4ac0a5b93a')
sonar = SonarQubeClient(sonarqube_url=sonarqube_server, token=sonarqube_token)
exporter_listen_host = os.environ.get('EXPORTER_LISTEN_HOST', '0.0.0.0')
exporter_listen_port = os.environ.get('EXPORTER_LISTEN_PORT', 8198)

def schedule(minutes, task):
    while True:
        try:
            tic = time.time()
            task()
            duration = time.time() - tic
            sleep_time = max(60 * minutes - int(duration), 1)
            print("sleeping %d seconds" % sleep_time)
            time.sleep(max(sleep_time, 0))
        except (KeyboardInterrupt, SystemExit) as e:
            raise e
        except Exception as e:
            print(e)

def exporter_start():

    print('starting server http://{}:{}/metrics'.format(
    exporter_listen_host, exporter_listen_port))

    '''
    Stop scraping of default metric
    '''
    prom.REGISTRY.unregister(prom.PROCESS_COLLECTOR)
    prom.REGISTRY.unregister(prom.PLATFORM_COLLECTOR)
    prom.REGISTRY.unregister(prom.GC_COLLECTOR)
    
    metrics = list(sonar.metrics.search_metrics())
    stats = get_stat(metrics)
    
    def metrics_task():
        system_metric(sonarqube_server, sonarqube_token)
        for s in stats:
            common_metrics(sonar, s)
            
        rule_metrics(sonar)
        event_metrics(sonar)
    try:
        start_http_server(exporter_listen_port, addr=exporter_listen_host)
        schedule(minutes=1, task=metrics_task)
    except (KeyboardInterrupt, SystemExit) as e:
        print(e)


if __name__ == "__main__":
    exporter_start()

    


