Testing
=======
### Running the tests
The test suite can be executed by running this command from the
command line:
```
$ python -m unittest test/*.py
```
Note that not all tests are run on a Linux platform since the
MS Office suite is not present here.

### Coverage

The code coverage can be measured by
```
$ coverage run --source=siarddk,tiff,util -m unittest test/*.py
$ coverage report
```
The latter command can be substituted by
```
$ coverage html
```
which will provide a nice HTML coverage report in the folder `htmlcov`.