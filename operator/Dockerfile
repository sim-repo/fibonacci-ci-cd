FROM python:3.7
COPY templates ./templates
COPY operator.py ./operator.py
RUN pip install kopf kubernetes pyyaml jinja2
CMD kopf run /operator.py