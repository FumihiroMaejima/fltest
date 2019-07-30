FROM python:3.7
ENV PYTHONUNBUFFERED 1

ARG project_dir=/code/
ADD src/requirements.txt $project_dir
WORKDIR $project_dir
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
