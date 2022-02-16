FROM python:3.9
COPY main.py main.py
RUN apt-get update
RUN apt-get install -y texlive graphviz graphviz-dev python3-pygraphviz
RUN pip install networkx
RUN pip install pygraphviz
RUN pip install -i https://test.pypi.org/simple/ ExampleGeneratorOfAST==0.0.1
RUN mkdir artifacts
RUN python3.9 main.py
RUN pdflatex artifacts/medium_task.tex