FROM python:3.8

RUN adduser aoc
USER aoc

COPY requirements*.txt /tmp
RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements-devel.txt
