FROM python:3

WORKDIR /to_do_list

COPY ./requirements.txt /to_do_list/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /to_do_list/requirements.txt

COPY . /to_do_list

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "55000"]