FROM python:3.12

RUN adduser aoc
USER aoc

COPY requirements*.txt /tmp
RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements-devel.txt
