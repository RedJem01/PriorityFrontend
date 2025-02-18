FROM python:latest
WORKDIR /PriorityFrontend
COPY . /PriorityFrontend
RUN pip3 install -r requirements.txt
ENV FLASK_APP=main
ENV P1_QUEUE=''
ENV P2_QUEUE=''
ENV P3_QUEUE=''
ENV AWS_REGION=''
ENV ACCESS_KEY=''
ENV SECRET_ACCESS_KEY=''
EXPOSE 8000
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "8000"]