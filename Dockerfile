FROM public.ecr.aws/lambda/python:3.9 as build

RUN yum install gzip -y
COPY requirements.txt  .
COPY model_downloader.py  .

RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"
RUN python3 model_downloader.py




FROM public.ecr.aws/lambda/python:3.9
RUN yum install gzip -y
COPY  --from=build /root/gensim-data/glove-wiki-gigaword-300/glove-wiki-gigaword-300.gz /var/task/glove-wiki-gigaword-300.gz
COPY mock_event.json ./
COPY requirements.txt  .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"
RUN gzip -d /var/task/glove-wiki-gigaword-300.gz

COPY inference.py ./
CMD [ "inference.lambda_handler" ]



