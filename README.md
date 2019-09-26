What is it
==========

It is a simple project written on python. It consists of two parts. First one
stored in `sender` directory and gets some json files given to it, convert it
to xml, does some simple encryption (I cannot name it an encryption though) and
then send encrypted data to second part. Second one (which as you could suppose
is stored in `receiver` directory) can recieve that encrypted data, decrypt it
and store in some directory as xml files.


How to use it
=============

I suppose you know how to use docker and has docker engine installed and
configured (`docker ps` command which is ran in your shell should return with
exit code 0). Also I suppose you have python 3 installed and configured.

If you have all prerequisites, there are steps you need to reproduce:


* Clone this repository

    ```
    git clone https://github.com/sorrowless/python-client-server-encryption
    cd python-client-server-encryption
    ```

* Create python virtualenv and install requirements:

    ```
    python3 -m venv venv
    . ./venv/bin/activate
    pip install -U pip
    pip install -r requirements.txt
    ```

* Build Docker containers:

    ```
    docker-compose build
    ```

* Run Docker containers:

    ```
    docker-compose up
    ```


What you'll get
===============

After running docker-compose up `sender` container will send all the data from
`json_data` directory and exit. Data in `json_data` directory is just an
examples. There are next files in it:

* colors.json - it is a file which looks like JSON but it is not, so it won't
  be converted

* fruits.json - small JSON example

* generated.json - biggest auto-generated JSON example

* planets.json - mid-size JSON with a bit non-standard data

Second container, `receiver` will continue running as task was to store data
**inside** the container. Data is stored inside container in `/tmp/xml_data`
directory. That directory is a volume mapped into container, so if you want
to look at it from host, you can just look into `xml_data` directory in repo.

Code itself is pretty much obvious, functions are documented. In case of any
questions feel free to ask me. There are no tests for the project as there
were no such requirements and I decided to provide a solution faster.

