# AUTHOR: Marcos Winicyus Borges Lima
# DESCRIPTION: Basic Airflow with papermill container 
# SOURCE: https://github.com/MarcosWinicyus/prod-airflow-docker

FROM puckel/docker-airflow:1.10.9
LABEL maintainer="marcos.lima@simpleagro.com.br"

USER root

RUN pip install --upgrade pip apache-airflow \
    && pip install ipykernel \
    && pip install papermill \
    && pip install suds-jurko \
    && pip install xmltodict \
    && pip install Unidecode \
    && pip install kafka-python \
    && pip install openpyxl \
    && pip install HTMLParser\
    && pip install pyPdf \
    && pip install python-slugify \
    && pip install pymongo \
    && pip install pandas \
    && pip install numpy \
    && pip install PyPDF2 \
    && apt-get clean \
    && rm -rf \
        /var/lib/apt/lists/* \
        /tmp/* \
        /var/tmp/* \
        /usr/share/man \
        /usr/share/doc \
        /usr/share/doc-base

USER airflow
