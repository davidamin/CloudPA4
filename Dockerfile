FROM tp33/django-docker:1.3

RUN git clone https://github.com/davidamin/CloudPA4.git . 
RUN mkdir uploads

CMD python manage.py runserver 0.0.0.0:80

