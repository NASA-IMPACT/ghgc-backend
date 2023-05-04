FROM public.ecr.aws/sam/build-python3.9:latest

ARG PGSTAC_VERSION
RUN echo "Using PGSTAC Version ${PGSTAC_VERSION}"

WORKDIR /tmp

RUN pip install requests==2.30.0 psycopg[binary,pool] pypgstac==${PGSTAC_VERSION} -t /asset

COPY database/runtime/handler.py /asset/handler.py

# https://stackoverflow.com/a/61746719
# Tip from eoAPI: turns out, asyncio is part of python
RUN rm -rf /asset/asyncio*

CMD ["echo", "hello world database"]