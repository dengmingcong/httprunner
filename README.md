# HttpRunner

基于 [HttpRunner](https://httprunner.com/httprunner/) 3.1.4 二次开发。

## 新增特性

* 新增 `retry_on_failure()` 方法用于断言失败后重试；
* 新增 `skip_if()` 和 `skip_unless()` 方法根据条件决定是否跳过步骤；
* 新增 Python 版本 [JSONassert](https://github.com/skyscreamer/JSONassert) 断言方法 `assert_json_contains()` 和 `assert_json_equal()`；
* Allure 报告现在可以显示接口请求、响应、断言详情了，且多个断言会在多个文件中展示；
* Allure 报告的请求中会显示真实的实际请求时间；
* 新增支持通过 `with_headers(**{"X-Json-Control": "expand"})` 实现展开响应中嵌套 JSON 的功能；
* 新增支持对变量中类似于 Python 属性和元素访问的表达式（如 `${obj.attr[0]}`）的解析；
* 新增对表达式 `${pyexp()}` 和 `${pyexec()}` 的支持，表达式中可以包含任意的 Python 表达式，如 `${pyexp(a + b)}` `${pyexec(a.b = c)}`，其中 `a b c` 均为 HttpRunner 的变量；
* 新增方法 `with_origin()` 支持同一接口请求不同 origin；
* 新增 pytest 命令行参数 `--continue-on-failure` 支持断言失败后继续运行用例；
* 新增 `RunTestCase.call()` 调用其他用例时可以为导出变量设置别名的功能；
* 新增 `parametrize()` 方法支持对单一步骤参数化（想较于 pytest 对整个用例参数化）；
* 新增断言方法 `assert_is_close()` 断言两个值的差值；
* 新增断言方法 `assert_match_pydantic_model()` 和 `assert_match_json_schema()` 支持对响应的数据结构做断言；
* 新增断言方法 `assert_lambda()` 支持添加任意自定义断言；
* 新增断言方法 `assert_each_equal()` 检查列表中每一个元素的值；
* 新增断言方法 `is_truthy_and_subset()` 和 `is_truthy_and_superset()` 支持对集合断言；
* `with_jmespath()` 新增参数 `sub_extractor` 用于在提取结果上使用函数做二次提取；
* 新增支持在 pyproject.toml 中通过设置 `tool.httprunner.http-headers` 为每一个接口设置公共请求头的功能；
* 新增 `with_pre_delay()` 和 `with_post_delay()` 支持在请求前/后等待。

## Fix

* 解决 HttpRunner 默认以 `multipart/form` 形式上传文件导致无法使用 PUT 单独上传一个文件的问题。