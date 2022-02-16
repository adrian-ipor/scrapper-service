FROM d21d3q/python-poetry@sha256:dc9c45574bdc370d9a48e9ee1384f8ae8fcafe8a12a35209aa30434a4b88fb03

RUN apt-get update && apt-get install -y \
  build-essential \
  && rm -rf /var/lib/apt/lists/*


WORKDIR /usr/local/scrapper-aave-v1

COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml

RUN poetry config virtualenvs.create false
RUN poetry install

COPY . /usr/local/ipor-scrapper-aave-v1

RUN ["chmod", "+x", "/usr/local/scrapper-aave-v1/scrapper.sh"]

CMD /usr/local/scrapper-aave-v1/scrapper.sh