import os
from enum import Enum
from typing import Any, Optional, IO
from typing import Dict, Text, Union, Callable
from typing import List

from pydantic import (
    BaseModel,
    Field,
    HttpUrl,
    ConfigDict,
)
from requests_toolbelt import MultipartEncoder

Name = Text
Url = Text
BaseUrl = Union[HttpUrl, Text]
VariablesMapping = Dict[Text, Any]
FunctionsMapping = Dict[Text, Callable]
Headers = Dict[Text, Text]
Cookies = Dict[Text, Text]
Verify = bool
Hooks = List[Union[Text, Dict[Text, Text]]]
GlobalVars = List[Union[Text, Dict[Text, Text]]]  # added by @deng at 2022.2.9
ConfigExport = List[Text]
Validators = List[Dict]
Env = Dict[Text, Any]


class MethodEnum(Text, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    PATCH = "PATCH"


class TConfig(BaseModel):
    name: Name
    verify: Verify = False
    base_url: BaseUrl = ""
    # Text: prepare variables in debugtalk.py, ${gen_variables()}
    variables: Union[VariablesMapping, Text] = {}
    parameters: Union[VariablesMapping, Text] = {}
    # setup_hooks: Hooks = []
    # teardown_hooks: Hooks = []
    export: ConfigExport = []
    path: Text = None
    weight: int = 1
    continue_on_failure: bool = False


class TRequestConfig(BaseModel):
    name: Name
    variables: Union[VariablesMapping, Text] = {}


class TRequest(BaseModel):
    """requests.Request model"""

    method: MethodEnum
    url: Url  # the origin part will be substituted by field origin if field origin is not None
    origin: str = None
    params: Dict[Text, Text] = {}
    headers: Headers = {}
    req_json: Union[Dict, List, Text] = Field(None, alias="json")
    req_json_update: list[tuple[Union[Dict, Text], bool]] = []
    data: Union[Text, Dict[Text, Any], MultipartEncoder, IO] = None
    data_update: list[tuple[Union[Dict, Text], bool]] = []
    cookies: Cookies = {}
    timeout: float = 120
    allow_redirects: bool = True
    verify: Verify = False
    upload: Dict = {}  # used for upload files
    model_config = ConfigDict(arbitrary_types_allowed=True)


class StepExport(BaseModel):
    # fix: AttributeError: 'tuple' object has no attribute 'extend'.
    # remove type hint `tuple`, retain `list` only, pydantic will coerce `tuple` to `list`
    var_names: list[str] = []
    var_alias_mapping: dict[str, str] = {}  # var will be renamed if in mapping


class JMESPathExtractor(BaseModel):
    """Used to extract value from JSON response using JMESPath query language."""

    variable_name: str
    expression: str
    sub_extractor: Optional[Callable] = None


class TStep(BaseModel):
    name: Name
    parametrize: tuple = None
    parsed_parametrize_vars: VariablesMapping = (
        {}
    )  # variables acquired after parsing parametrize
    remaining_retry_times: Union[int, str] = 0  # times remaining to retry
    max_retry_times: Union[int, str] = 0  # max retry times
    retry_interval: Union[int, float, str] = 0
    stop_retry_if: Any = None
    skip_if_condition: Any = None
    skip_unless_condition: Any = None
    skip_reason: Union[str, None] = None
    request: Union[TRequest, None] = None
    testcase: Union[Text, Callable, None] = None
    variables: VariablesMapping = {}
    raw_variables: str = None
    is_deep_parse_raw_variables: bool = None
    private_variables: VariablesMapping = (
        {}
    )  # variables set by HttRunnerRequest request
    setup_hooks: Hooks = []
    teardown_hooks: Hooks = []

    extract: list[
        Union[JMESPathExtractor]
    ] = []  # used to extract request's response field

    # used to export local step variables, steps next can use these variables then
    globalize: GlobalVars = []

    # used to export session variables from referenced testcase, only take effect for RunTestCase step
    export: StepExport = None

    validators: Validators = Field([], alias="validate")
    validate_script: List[Text] = []

    # HttpRunnerRequest config
    request_config: TRequestConfig = None


class TestCase(BaseModel):
    config: TConfig
    teststeps: List[TStep]


class ProjectMeta(BaseModel):
    debugtalk_py: Text = ""  # debugtalk.py file content
    debugtalk_path: Text = ""  # debugtalk.py file path
    dot_env_path: Text = ""  # .env file path
    functions: FunctionsMapping = {}  # functions defined in debugtalk.py
    env: Env = {}
    httprunner_root_path: Text = os.getcwd()  # the path debugtalk.py located


class TestsMapping(BaseModel):
    project_meta: ProjectMeta
    testcases: List[TestCase]


class TestCaseTime(BaseModel):
    start_at: float = 0
    start_at_iso_format: Text = ""
    duration: float = 0


class TestCaseInOut(BaseModel):
    config_vars: VariablesMapping = {}
    export_vars: Dict = {}


class RequestStat(BaseModel):
    content_size: float = 0
    response_time_ms: float = 0
    elapsed_ms: float = 0


class AddressData(BaseModel):
    client_ip: Text = "N/A"
    client_port: int = 0
    server_ip: Text = "N/A"
    server_port: int = 0


class RequestData(BaseModel):
    method: MethodEnum = MethodEnum.GET
    url: Url
    headers: Headers = {}
    cookies: Cookies = {}
    body: Union[Text, bytes, Dict, List, None] = {}


class ResponseData(BaseModel):
    status_code: int
    headers: Dict
    cookies: Cookies
    encoding: Union[Text, None] = None
    content_type: Text
    body: Union[Text, bytes, Dict, List]


class ReqRespData(BaseModel):
    request: RequestData
    response: ResponseData


class SessionData(BaseModel):
    """request session data, including request, response, validators and stat data"""

    success: bool = False  # represent the status (success or failure) of the latest HTTP request, default to False
    # in most cases, req_resps only contains one request & response,
    # while when 30X redirect occurs, req_resps will contain multiple request & response
    req_resps: List[ReqRespData] = []
    stat: RequestStat = RequestStat()
    address: AddressData = AddressData()
    validation_results: Dict = {}
    exception: Exception = None
    model_config = ConfigDict(arbitrary_types_allowed=True)


class StepData(BaseModel):
    """teststep data, each step maybe corresponding to one request or one testcase"""

    success: bool = False
    name: Text = ""  # teststep name
    data: Union[SessionData, List["StepData"]] = None
    export_vars: VariablesMapping = {}


class TestCaseSummary(BaseModel):
    name: Text
    success: bool
    case_id: Text
    time: TestCaseTime
    in_out: TestCaseInOut = {}
    log: Text = ""
    step_datas: List[StepData] = []


class PlatformInfo(BaseModel):
    httprunner_version: Text
    python_version: Text
    platform: Text


class TestCaseRef(BaseModel):
    name: Text
    base_url: Text = ""
    testcase: Text
    variables: VariablesMapping = {}


class TestSuite(BaseModel):
    config: TConfig
    testcases: List[TestCaseRef]


class Stat(BaseModel):
    total: int = 0
    success: int = 0
    fail: int = 0


class TestSuiteSummary(BaseModel):
    success: bool = False
    stat: Stat = Stat()
    time: TestCaseTime = TestCaseTime()
    platform: PlatformInfo
    testcases: List[TestCaseSummary]
