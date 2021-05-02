# ProcessAWSbucket

### Task description
Can be found here: https://github.com/MacPaw/msi2021-data-engineering

### Approach description

The main program for processing bucket was written in a fully asynchronous manner. The main idea of such approach is that in such a setup (constant http requests for files in bucket
and requests to database), the program is almost completely IO-bound, meaning it spends almost all the time waiting, not really doing processing.
Therefore, there is a 
point in making asynchronous web and db requests. Actually, below you can see a plot of time measurement of three approaches: fully synchronous(1), asynchronous web requests and sequential
db requests(2) and fully asynchronous(3). The conclusion is that asynchronous solution is approximately 10 times faster than (1) approach and 4 times faster than (2) approach. 

![Speed measurement](https://github.com/psemchyshyn/ProcessAWSbucket/blob/master/benchmarking/results.png)

The idea of processing files in different processes was also considered, however, due to the very small file sizes there wasn't much profit in doing that.

### Tools used

The program was written in python. For a RDBMS Postgres was chosen. The python libraries that were used can be found in requirements.txt file (some of them aren't
actually needed for a main program to run, they were used for benchmarking(comparing with synchronous solutions and plotting time required for processing all files available at the moment 
the program was launched)).

### General structure
* <a href="https://github.com/psemchyshyn/ProcessAWSbucket/tree/master/db">/db</a>
  * <a href="https://github.com/psemchyshyn/ProcessAWSbucket/blob/master/db/schema.sql">schema.sql</a> - defines a schema for database - tables, functions and triggers(the last are used for filling the columns original_title_normalized in movies and is_awesome in apps tables)
  * <a href="https://github.com/psemchyshyn/ProcessAWSbucket/blob/master/db/init.py">init.py</a> - contains python function to init the db schema
  * <a href="https://github.com/psemchyshyn/ProcessAWSbucket/blob/master/db/inserts.py">inserts.py</a> - contains python functions for performing insertions into different tables
  * <a href="https://github.com/psemchyshyn/ProcessAWSbucket/blob/master/db/Dockerfile">Dockerfile</a> - for creating an image of postgres and running it in a container
* <a href="https://github.com/psemchyshyn/ProcessAWSbucket/tree/master/benchmarking">/benchmarking</a>
  * <a href="https://github.com/psemchyshyn/ProcessAWSbucket/blob/master/benchmarking/plot.py">plot.py</a> - defines function used to obtain a plot
  * <a href="https://github.com/psemchyshyn/ProcessAWSbucket/tree/master/benchmarking/additional_scripts">/additional_scripts</a> - scripts for testing synchronous versions of the program
  * csv files containing data presented in the given above plot and the plot itself
* <a href="https://github.com/psemchyshyn/ProcessAWSbucket/blob/master/main.py">main.py</a>. Contains main logic of the program - entry point
* <a href="https://github.com/psemchyshyn/ProcessAWSbucket/blob/master/Dockerfile">Dockerfile</a> - for creating an image of the main program
* <a href="https://github.com/psemchyshyn/ProcessAWSbucket/blob/master/requirements.txt">requirements.txt</a> for installing python libraries used in the program
* <a href="https://github.com/psemchyshyn/ProcessAWSbucket/blob/master/docker-compose.yml">docker-compose.yml</a> - for setting up the whole program

### Running the program:

*Via docker*
```
git clone https://github.com/psemchyshyn/ProcessAWSbucket.git
cd ProcessAWSbucket
docker compose run
```

*Manually*(database is expected to be initalized and running. In main.py change variable DSN of the db if needed)
```
git clone https://github.com/psemchyshyn/ProcessAWSbucket.git
cd ProcessAWSbucket
pip install -r requirements.txt
python main.py
```
