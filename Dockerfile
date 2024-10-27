FROM python:3.8.19-alpine

WORKDIR /sonarqube_exporter/
COPY requirements.txt .
RUN /usr/local/bin/python3 -m pip install --upgrade pip && \
pip3 install -r requirements.txt --no-cache-dir && \
rm -rf /root/.cache/pip/

COPY . .
RUN chmod a+x entrypoint.sh \
&& mkdir -p ./logs
EXPOSE 8198
ENTRYPOINT [ "/bin/sh",  "entrypoint.sh" ]