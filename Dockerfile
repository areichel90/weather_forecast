FROM python:3.10

#WORKDIR ..

COPY ./../src/ /src/

WORKDIR src

RUN pip install requests && \
    pip install pandas && \
    pip install numpy && \
    pip install plotly && \
    pip install dash && \
    pip install ipywidgets && \
    pip install dash_bootstrap_components && \
    pip install dash_bootstrap_templates

EXPOSE 8085

CMD ["python3", "weather_dash_app.py"]
