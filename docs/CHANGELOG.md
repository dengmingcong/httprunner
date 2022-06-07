# Release History

<!--next-version-placeholder-->

## v3.5.2 (2022-06-07)
### Fix
* Loop forever when expression exists in 'with_variables()' ([`510635d`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/510635d0b4a67419651c836a40a813a2beec0453))

## v3.5.1 (2022-06-07)
### Fix
* Unexpected result when parsing format like '${foo}.bar' ([`512133f`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/512133f8d686dd531a1b5fa8fb658bd7bd450b90))

## v3.5.0 (2022-06-06)
### Feature
* Add support to parse expression with format as ${var.attr[0]['key']} ([`e85cddd`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/e85cddd540d1d899af68b1a190164e8f00c4a224))

### Fix
* Improper function naming for functionality evaluation ([`0e79b75`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/0e79b754ff44a45ee3e584bfec418f0ae63cd2c1))

## v3.4.1 (2022-06-01)
### Fix
* File not exist when variables exist in upload dict ([`12ccdb3`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/12ccdb3a47f2a699c6d27b4cdf438a3d98961b78))

## v3.4.0 (2022-06-01)
### Feature
* Add support to upload file with discrete mime types ([`b209d61`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/b209d61cac86b8154e79e9e69182aab08f2e36d3))

### Fix
* Too many arguments to unpack ([`2d64dcb`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/2d64dcbfeb133dccc3f056cc2bb0e6794f951420))

### Documentation
* Denote condition 'discrete' ([`4f1ad47`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/4f1ad47121169b0a7ec8d319e18e147045e2bdcb))

## v3.3.5 (2022-05-27)
### Fix
* **ci:** File or directory not found: examples/postman_echo/request_methods ([`1970b05`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/1970b054b8d456a92542e722d70c3972503b798b))

### Documentation
* **ci:** Add placeholder for semantic-release ([`0155095`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/0155095241e270e6944d664fa89e02caba493fd0))

## 3.1.4 (2020-07-30)

**Changed**

- change: override variables strategy, step variables > extracted variables from previous steps

**Fixed**

- fix: parameters feature with custom functions
- fix: request json field with variable reference
- fix: pickle BufferedReader TypeError in upload feature

## 3.1.3 (2020-07-06)

**Added**

- feat: implement `parameters` feature

**Fixed**

- fix: validate with variable or function whose evaluation result is "" or not text
- fix: raise TestCaseFormatError if teststep validate invalid
- fix: raise TestCaseFormatError if ref testcase is invalid

## 3.1.2 (2020-06-29)

**Fixed**

- fix: missing setup/teardown hooks for referenced testcase
- fix: compatibility for `black` on Android termux that does not support multiprocessing well
- fix: mishandling of request header `Content-Length` for GET method
- fix: validate with jmespath containing variable or function, e.g. `body.locations[$index].name`

**Changed**

- change: import locust at beginning to monkey patch all modules
- change: open file in binary mode

## 3.1.1 (2020-06-23)

**Added**

- feat: add optional message for assertion

**Fixed**

- fix: ValueError when type_match None
- fix: override referenced testcase export in teststep
- fix: avoid duplicate import
- fix: override locust weight

## 3.1.0 (2020-06-21)

**Added**

- feat: integrate [locust](https://locust.io/) v1.0

**Changed**

- change: make converted referenced pytest files always relative to ProjectRootDir
- change: log function details when call function failed
- change: do not raise error if failed to get client/server address info

**Fixed**

- fix: path handling error when har2case har file and cwd != ProjectRootDir
- fix: missing list type for request body

## 3.0.13 (2020-06-17)

**Added**

- feat: log client/server IP and port

**Fixed**

- fix: avoid '.csv' been converted to '_csv'
- fix: convert har to JSON format testcase
- fix: missing ${var} handling in overriding config variables
- fix: SyntaxError caused by quote in case of headers."Set-Cookie"
- fix: FileExistsError when specified project name conflicts with existed file
- fix: testcase path handling error when path startswith "./" or ".\\"

## 3.0.12 (2020-06-14)

**Fixed**

- fix: compatibility with different path separators of Linux and Windows
- fix: IndexError in ensure_file_path_valid when file_path=os.getcwd()
- fix: ensure step referenced api, convert to v3 testcase
- fix: several other compatibility issues

**Changed**

- change: skip reporting sentry for errors occurred in debugtalk.py

## 3.0.11 (2020-06-08)

**Changed**

- change: override variables
    (1) testcase: session variables > step variables > config variables
    (2) testsuite: testcase variables > config variables
    (3) testsuite testcase variables > testcase config variables

**Fixed**

- fix: incorrect summary success when testcase failed
- fix: reload to refresh previously loaded debugtalk module
- fix: escape $$ in variable value

## 3.0.10 (2020-06-07)

**Added**

- feat: implement step setup/teardown hooks
- feat: support alter response in teardown hooks

**Fixed**

- fix: ensure upload ready
- fix: add ExtendJSONEncoder to safely dump json data with python object, such as MultipartEncoder

## 3.0.9 (2020-06-07)

**Fixed**

- fix: miss formatting referenced testcase
- fix: handle cases when parent directory name includes dot/hyphen/space

**Changed**

- change: add `export` keyword in TStep to export session variables from referenced testcase
- change: rename TestCaseInOut field, config_vars and export_vars
- change: rename StepData field, export_vars
- change: add `--tb=short` for `hrun` command to use shorter traceback format by default
- change: search debugtalk.py upward recursively until system root dir

## 3.0.8 (2020-06-04)

**Added**

- feat: add sentry sdk
- feat: extract session variable from referenced testcase step

**Fixed**

- fix: missing request json
- fix: override testsuite/testcase config verify
- fix: only strip whitespaces and tabs, \n\r are left because they maybe used in changeset
- fix: log testcase duration before raise ValidationFailure

**Changed**

- change: add httprunner version in generated pytest file

## 3.0.7 (2020-06-03)

**Added**

- feat: make pytest files in chain style
- feat: `hrun` supports run pytest files
- feat: get raw testcase model from pytest file

**Fixed**

- fix: convert jmespath.search result to int/float unintentionally
- fix: referenced testcase should not be run duplicately
- fix: requests.cookies.CookieConflictError, multiple cookies with name
- fix: missing exit code from pytest
- fix: skip invalid testcase/testsuite yaml/json file

**Changed**

- change: `har2case` generate pytest file by default
- docs: update sponsor info

## 3.0.6 (2020-05-29)

**Added**

- feat: make referenced testcase as pytest class

**Fixed**

- fix: ensure converted python file in utf-8 encoding
- fix: duplicate running referenced testcase
- fix: ensure compatibility issues between testcase format v2 and v3
- fix: ensure compatibility with deprecated cli args in v2, include --failfast/--report-file/--save-tests
- fix: UnicodeDecodeError when request body in protobuf

**Changed**

- change: make `allure-pytest`, `requests-toolbelt`, `filetype` as optional dependencies
- change: move all unittests to tests folder
- change: save testcase log in PWD/logs/ directory

## 3.0.5 (2020-05-22)

**Added**

- feat: each testcase has an unique id in uuid4 format
- feat: add default header `HRUN-Request-ID` for each testcase #721
- feat: builtin allure report
- feat: dump log for each testcase

**Fixed**

- fix: ensure referenced testcase share the same session

**Changed**

- change: remove default added `-s` option for hrun

## 3.0.4 (2020-05-19)

**Added**

- feat: make testsuite and run testsuite
- feat: testcase/testsuite config support getting variables by function
- feat: har2case with request cookies
- feat: log request/response headers and body with indent

**Fixed**

- fix: extract response cookies
- fix: handle errors when no valid testcases generated

**Changed**

- change: har2case do not ignore request headers, except for header startswith :

## 3.0.3 (2020-05-17)

**Fixed**

- fix: compatibility with testcase file path includes dots, space and minus sign
- fix: testcase generator, validate content.xxx => body.xxx
- fix: scaffold for v3

## 3.0.2 (2020-05-16)

**Added**

- feat: add `make` sub-command to generate python testcases from YAML/JSON  
- feat: format generated python testcases with [`black`](https://github.com/psf/black)
- test: add postman echo & httpbin as testcase examples

**Changed**

- refactor all
- replace jsonschema validation with pydantic
- remove compatibility with testcase/testsuite format v1
- replace unittest with pytest
- remove builtin html report, allure will be used with pytest later
- remove locust support temporarily
- update command line interface

## 3.0.1 (2020-03-24)

**Changed**

- remove sentry sdk

## 3.0.0 (2020-03-10)

**Added**

- feat: dump log for each testcase
- feat: add default header `HRUN-Request-ID` for each testcase #721

**Changed**

- remove support for Python 2.7
- replace logging with [loguru](https://github.com/Delgan/loguru)
- replace string format with f-string
- remove dependency colorama and colorlog
- generate reports/logs folder in current working directory
- remove cli `--validate`
- remove cli `--pretty`
