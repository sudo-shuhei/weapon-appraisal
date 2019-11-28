FROM python:3.6

ARG project_dir=/app/

WORKDIR $project_dir

RUN pip install flask
RUN pip install gunicorn
RUN pip install schedule
RUN pip install requests

CMD ["python", "main.py"]
