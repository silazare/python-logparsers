## Logparsers scripts

[![Build status](https://travis-ci.org/silazare/python-logparsers.svg?master)](https://travis-ci.org/silazare)

### Tool for parsing application logs by transaction ID and save filtered result. 

- Features:
  - Parsing complex application log structures where we need to capture rows not only by ID in the string 
    but capture all other related/needed rows which we have in between and without ID.
  - Ability to parse huge text and gzip files.
  - Some enhancements to reduce output of not needed rows.
  - Prepared for Python 2.7: 

- Clone this repository to your folder:
```sh
$ git clone https://github.com/silazare/python-logparsers.git
$ cd python-logparsers
$ chmod +x app_logparser.py
```

- Execute for target log file:
```sh
$ python app_logparser.py <file> <ID>
Where: 
      <file> - target log file (txt or gzip)
      <ID> - needed app transaction ID search criteria
```

### Tool for parsing nginx access logs. 

- Features:
   - Count of HTTP codes
   - Group by IP address
   - Sort by ascending (TBD)
   - Prepared for Python 2.7: 

- Clone this repository to your folder:
```sh
$ git clone https://github.com/silazare/python-logparsers.git
$ cd python-logparsers
$ chmod +x nginx_logparser.py
```

- Execute for target log file:
```sh
$ python app_logparser.py -log <file_path> -f <filter_criteria>  
Where: 
      <file_path> - target access log file
      <filter_criteria> - general/error
Examples:
python nginx_logparser.py -log access.log -f general
python nginx_logparser.py -log access.log -f error
```
