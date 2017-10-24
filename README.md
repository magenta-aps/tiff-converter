Basic usage
===========
# Converting files to TIFF
The tool is capable of using two types of sources of files to batch convert 
into TIFF. The first option is to use any given folder that contains files 
(and subfolders) to convert - let's call this *normal* conversion. 
The other option is to use *in-place* conversion 
where an already existing archival version (except that the files in the 
`Documents` folders are not yet converted into TIFF) as the source of files 
for the conversion.

## Normal conversion
"Normal" conversion can be done by
````
$ python siarddktool.py --target path/to/target --name AVID.MAG.1000 convert --source path/to/source 
````
It is also possible to append more files to an already existing archival version 
by using the `--append` flag:
```
$ python siarddktool.py --target path/to/target --name AVID.MAG.1000 convert --source path/to/more/sources --append
```

## In-place conversion
Use this command to perform an in-place conversion:
````
$ python siarddktool.py --name AVID.MAG.1000 convert --inplace --source path/to/source
````
In this case the source folder must be the folder that contains the e.g. 
`AVID.MAG.1000.n` folders. 

# Creating and manipulating fileIndex.xml
## Removing files
Assuming we have an existing archival version. Use this command to remove all 
files from fileIndex.xml except for those in the `Tables` folder:
```
$ python siarddktool.py --target path/to/target --name AVID.MAG.1000 fileindex --remove
```
The target folder must be the folder that contains the e.g. 
`AVID.MAG.1000.n` folders.

## Adding files
To add more files to `fileIndex.xml` use a command similar to
```
$ python siarddktool.py --target path/to/target --name AVID.MAG.1000 fileindex /
--add path/to/AVID.MAG.1000.1/Documents --add path/to/AVID.MAG.1000.1/Documents/docCollection1/3/1.tif
``` 

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