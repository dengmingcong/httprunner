# Release History

<!--next-version-placeholder-->

## v3.47.0 (2024-12-03)

### Feature

* Types inherited from dict or list are valid JSON data type now ([`5db9c5e`](https://fangcun.vesync.cn/testTeam/httprunner/-/commit/5db9c5ee53f5c4b37ed442d6af2e5ac2ce4163b4))

## v3.46.0 (2024-12-02)

### Feature

* Add validator for subset and superset ([`72e52c1`](https://fangcun.vesync.cn/testTeam/httprunner/-/commit/72e52c1732b8f0de9f2e81110bea4ce73791001d))
* Delay reason can be set now ([`e0acd50`](https://fangcun.vesync.cn/testTeam/httprunner/-/commit/e0acd5005a05382b6558f9672c1e7a5eccd42c87))
* Display request timestamp too ([`fe0035b`](https://fangcun.vesync.cn/testTeam/httprunner/-/commit/fe0035b1f5911cecc00b45b72894370534b70ec4))
* Add configurable request timezones ([`3021195`](https://fangcun.vesync.cn/testTeam/httprunner/-/commit/3021195e41f2afe5604819d12f7be5a17fbca457))
* Set Date in request header to UTC datetime and show microseconds ([`8fc2974`](https://fangcun.vesync.cn/testTeam/httprunner/-/commit/8fc2974d8ad443a014b86b01c017ad4afa6f9d89))
* Assert_json_contains_with_java call json_contains_v2 internally now ([`399d54c`](https://fangcun.vesync.cn/testTeam/httprunner/-/commit/399d54cec6f1f769b69c1146c5451ac48373199a))

### Fix

* DotWiz was considered as valid JSON type but cause error while comparing with dict ([`a54e83f`](https://fangcun.vesync.cn/testTeam/httprunner/-/commit/a54e83f074c77080f35d2028fbc92706f4ff5dc2))
* DotWiz was considered as valid JSON type but cause error while comparing with dict ([`78d1d07`](https://fangcun.vesync.cn/testTeam/httprunner/-/commit/78d1d0706b6700f22355aa3a07cf723a93dbac6b))
* Convert dotwiz to dict before comparing ([`f19134a`](https://fangcun.vesync.cn/testTeam/httprunner/-/commit/f19134a158d1f4a99f27b1eeda765bc49615a7cb))

### Documentation

* Java-version JSONAssert will be used by default ([`810b286`](https://fangcun.vesync.cn/testTeam/httprunner/-/commit/810b286586ea7a19207f944e5bb6c52dcbe9865d))

### Performance

* Change if other_deepdiff_kwargs not empty before set operation ([`d190650`](https://fangcun.vesync.cn/testTeam/httprunner/-/commit/d19065057757b8caeb71672a388b9a59cb130f0e))
* Replace for loop with set intersection ([`744993f`](https://fangcun.vesync.cn/testTeam/httprunner/-/commit/744993f3215a35873d20a286b24c32723412bbdf))

## v3.45.0 (2024-09-24)

### Feature

* PyProjectTomlKey can set default value ([`4195b8a`](https://fangcun.vesync.cn/testTeam/httprunner/-/commit/4195b8af3c6489346874653661f70bcb1791ed74))

### Documentation

* Arguments of PyProjectTomlKey constructor ([`4980ad7`](https://fangcun.vesync.cn/testTeam/httprunner/-/commit/4980ad7bfb9c413ba25ffed87ef7838aa12f09b2))

## v3.44.1 (2024-06-28)

### Fix

* Pydantic model validation failed when response is null ([`c45a991`](https://fangcun.vesync.cn/testTeam/httprunner/-/commit/c45a991056bc4bf69fee76a25e8c95ec3d414d3e))

## v3.44.0 (2024-04-08)

### Feature

* Add expression ${pyexec()} to enable setting object's attributes ([`c325bac`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/c325bace5a32c652082612eff0a7c984e8dc6d35))

### Fix

* Value in with_pre_delay() will not be resolved when skip condition was set ([`23660b6`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/23660b6745fd273dcd7cd8da31d2a1af7065c847))

## v3.43.0 (2024-03-28)

### Feature

* 参数化与export同时使用时，在export变量后添加标号导出 ([`9339ee7`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/9339ee7c5fc4629943255eff5e299cad0f8bfa7a))

### Fix

* 修改文档描述 ([`8aa9fcb`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/8aa9fcbed0136a4b49aa1966c3192c56f256ba10))
* 修改参数化导出变量的后缀标号 ([`75e0774`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/75e077448e0e42b33eedf28cbdd916cdb416bfad))
* 修改参数化导出变量的后缀标号 ([`a66e15a`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/a66e15a79050f26bc59bb643b88d8b9620c1933e))

## v3.42.0 (2024-03-19)

### Feature

* Update headers for every request with environment variable GLOBAL_HTTP_HEADERS ([`50c2a9e`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/50c2a9e812099dcb6ba16f2f9e5457a569d1a8ab))

## v3.41.5 (2024-03-19)

### Fix

* Status code 4xx and 5xx will cause ValidationFailure ([`d47cacf`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/d47cacf3571452ec075a59286bf6725581b03e7c))

### Documentation

* The difference between bad status code and ConnectTimeout exception ([`2e25153`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/2e251537847726e03f709debe0fc5d2d99f740f5))

## v3.41.4 (2024-03-14)

### Fix

* 请求的时候判断解析出来的 content 是否为None，为None就请求真实服务 ([`6d8bdc1`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/6d8bdc16810ad28e1494ed73426e0e0334f85ca6))
* 请求的时候判断解析出来的 content 是否为None，为None就请求真实服务 ([`b3caeef`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/b3caeef4750bf3126a27b13c14494358dafe947f))

## v3.41.3 (2024-03-14)

### Fix

* .mock 方法修改为如果 content 为 None，请求真实服务 ([`aa0a7f5`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/aa0a7f57e321d2928c04dee9dcc42c00f58ade4a))
* Content 添加判空 ([`a2418e5`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/a2418e5d27ffebf1f04518b62cab062fc004c82e))
* Content 添加判空 ([`12d82c2`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/12d82c2143993a241d8a232049fb014ecf5c414f))

## v3.41.2 (2024-03-11)

### Fix

* Poetry lock no update ([`453931f`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/453931f77b83f13b68c5a2c64fb833eba42c5f9b))
* 引入 mock.js 使响应能够按照模版生成随机数据 ([`41520df`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/41520df0b44b3108f46fdf9397eb6d42cf1ffdcb))

## v3.41.1 (2024-03-11)

### Fix

* 解决 mock 模式下 request 的 body，headers 为空的问题 ([`1867606`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/1867606f582a2844caeffa06f4e065e72a776e5e))

## v3.41.0 (2024-03-08)

### Feature

* Mock 功能V0.1 ([`187519e`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/187519ec304b166c9327c88384c99c5dc61da304))

### Fix

* 修改注释 ([`2b508ab`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/2b508ab4be0bc433c91398b55502dba3319668d9))
* Issue 问题整改 ([`b2e899e`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/b2e899e47fea6f4aae18e71537483f6ed46046fa))
* Mock_body 添加类型声明 ([`7a5289b`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/7a5289bd76c9f15252ab7430de1e49d003f04f99))
* 解决冒烟报错的问题 ([`986d025`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/986d02533d5770939f2fd38ef0c02da33003af31))
* Mock 冒烟用例添加环境变量配置 ([`be06ac5`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/be06ac50875d1ea1731d3eb037b14bdbac0b333d))
* 添加 mock_body 判断条件 ([`70f4309`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/70f4309421923749a4dce594c72601737606a636))
* 删除空格 ([`fa46777`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/fa467773834461cd5c683c359384d71dff72b285))
* 删除 MockFailedError 异常类 ([`29f309c`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/29f309cce94a68b452bd169bbbd9e910373a5a6b))
* 添加环境变量 mock_mode 配置 ([`35b56a9`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/35b56a9d5f9fc2fef4e31cb911710bd64d096e4e))
* 去掉 httprunner 中去判断 api 默认mock配置的代码 ([`e5efeed`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/e5efeed99abdf3baf17a52cee56d7e653bc291f7))
* 删除 get_sub_dict 函数 ([`b4eca85`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/b4eca85bd94413f23ef19c158ebf71bd9f8eb71b))
* 添加 --mock-mode 配置 ([`c287c8b`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/c287c8bf5f4c667fad49695844e556f2b33917be))
* 解决flake8报错 ([`eda5490`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/eda5490660c6a61333faf4a900a4f5c302e65766))

## v3.40.0 (2024-03-06)

### Feature

* Sleep before and after step ([`88aac9d`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/88aac9dd3ce5fb562da33a4b7dfb644c372c572b))
* Add function to parse and display delay info in step name ([`a5efa10`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/a5efa10150fe3fe1aa91b03479ee1d48bd05b033))
* Add function to parse and display delay info in step name ([`3d5ca5d`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/3d5ca5d9a9fa5f6ee578b51315ebb3738af9bdf7))
* (deprecated) remove TimerMixin from RunTestCase ([`5ebe009`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/5ebe009d97b64af982044532e5b904d48926d74f))
* Add TimerMixin to RunTestCase ([`f1c01a4`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/f1c01a48cff5dc09cf9be69bb58db0484bc40456))
* Add TimerMixin to RunRequest and HttpRunnerRequest ([`338468d`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/338468dd67abfbd0ddf55c85d7d105f16eaf8888))
* Add fields for timer ([`a394cbd`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/a394cbdef3a34483fcc9f3ab9ef3fb7011df51a8))
* Add TimerMixin ([`5096fc8`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/5096fc8ce3750de2bf8328e86fe51de0312faea2))

### Documentation

* Unit is second ([`2c307d1`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/2c307d1c6ebc960384661277a7ebde197fbf597f))

## v3.39.1 (2024-03-04)

### Performance

* Change poetry source to speed up dependency resolving ([`dc8f8bb`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/dc8f8bbc14b5471c67e1017b9bfe52ef5206cab0))

## v3.39.0 (2024-02-29)

### Feature

* Add validator `assert_each_equal` ([`de5907c`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/de5907c718a556ce8f1b40a5a24233d400e918b4))
* Add config to support asserting each item of list equals to the expected value ([`c3ff285`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/c3ff285ccc1bc54b8e331f2445c67a870a15cac8))

### Fix

* Deepdiff kwargs specified in tuple should have higher priority than those specified in function keyword arguments ([`5a07e25`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/5a07e25ce894900f5bdee8ad909d42f77fac448a))
* Pass None to extend() raise error ([`376b67e`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/376b67eaa2866129100be1146f50e071d8529bd7))

### Documentation

* Denote deprecated functions ([`29a8a24`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/29a8a245d09b4fb4b555b57cbfc8890b1f385329))
* Add docs for fields ([`b6e213a`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/b6e213a31c17fa4a63df34c18c532b90e6ec612d))

## v3.38.1 (2024-02-20)

### Fix

* Plain string cannot be posted together with file in one multipart body ([`833ad33`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/833ad3397d19e73981451d3ec84223e01e6cac1e))

## v3.38.0 (2024-02-01)

### Feature

* Evaluate multiple resources ([`057a60b`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/057a60ba89344cd0f31011855d99bf7d3346bb43))
* Multiple resources can be specified by calling `with_resource()` multiple times ([`c8d0a19`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/c8d0a19282379706846fa8ca538fb392639852a5))
* Raise MultiValidationFailure when all exceptions are instance of ValidationFailure ([`68f9c68`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/68f9c68b5a87ec212e65b2f1af2e28ecbeff3896))
* Add function `evaluate_with_api()` ([`abc8052`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/abc80520de874472bc6593968ad9825e8def4a4d))
* Add method RequestConfig.with_api() to specify api docs ([`254a812`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/254a812307eb93a477f5169dbe50ceb0bd99c569))

### Fix

* Step.request_config has no property `extractor` ([`ffdb77d`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/ffdb77dc40a4dbc425139cbe401522329c5043d3))

### Performance

* Reduce one parsing process if no private variables found ([`07b9a27`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/07b9a273821e7060b9ff6c8e216aa3c9c08d87bb))

## v3.37.0 (2024-01-09)

### Feature

* Print failing reason in log between the beginning of the step and the end of the step ([`85f64b6`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/85f64b68174d88b5d0faf16cbe9d064d2929ef74))
* Add new argument `is_create_new_mapping` to enable returning the same object as the one specified by the first argument ([`8f0bf87`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/8f0bf871a6f5d170c3291a45beea128d74577afd))

### Fix

* Teardown hooks cannot use variables exported by nested testcase ([`7f1e69c`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/7f1e69c46955ffb3705883ef7333b0e336460e33))
* Steps were missing in allure report when exception occurred while parsing step name ([`51c1854`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/51c185483153a99bfaa4cb286d1e4e9901ff5fbb))
* Step.variables containing self-referenced variables cause VariableNotFound ([`1b7fe85`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/1b7fe8550ab3ff380b44bb39bde227f14a592d2e))
* Update step.variables with hook variables, otherwise next hooks may not use them ([`5d8c940`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/5d8c9403c3003237d3254573a0f9cff3a58a4b43))
* Update session variables of nested testcase with the ones added by teardown hooks ([`dc28b95`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/dc28b95d16bbd964d6029596f5604c0504ad89ea))
* Is_relay_export did not take effect ([`c7e3065`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/c7e30656e27a701c4319453e43904f272c7e9a93))
* Vars added by parametrized steps override context vars ([`80e785d`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/80e785d88fb78fcd81ed8a92b7859427e783f12d))

### Performance

* Increase the performance of merging variables ([`9867d65`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/9867d656dbee396c3e5c1246203e1ce2bb48e00a))

## v3.36.1 (2024-01-05)

### Fix

* No sleep between two retries ([`08087db`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/08087dbfff0feb667d5ce00544df1063c51ed2c0))

## v3.36.0 (2023-12-29)

### Feature

* Add validator assert_lambda to support validating with custom validators ([`8e4bc84`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/8e4bc84d1c835f03f4f521fdd5116225839ae987))

### Fix

* TypeError: cannot pickle 'module' object ([`681833b`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/681833b69c30f34848a653b5373cbaee581e36c2))

## v3.35.0 (2023-12-28)

### Feature

* Failed steps will not export vars ([`b2987b7`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/b2987b764fc602104c5144bf4382eb8933a9deda))
* Support exporting variables relay when retrying ([`0e4eac7`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/0e4eac77481ea837016ea6c19d73ecfac0ebb117))

### Fix

* Variables in class attribute are changed unexpectedly ([`0d422a4`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/0d422a47f8c954f79322f59c84dac209991edfd1))
* Deepcopy cause changes applied on compound data lost ([`ba22b19`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/ba22b19544384112150b0f00280ba3cfa9be5760))
* Variables added by teardown hooks cannot be exported ([`627e8d5`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/627e8d5d6399c451ecc875334a91956c1397e4df))
* Make exported variables show in allure the same with that were actually exported ([`0737377`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/073737740e17cab32d7b52d742ff4838d17cb6d4))
* Variables exported by intermediate requests when retrying cause surprise ([`ba43758`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/ba43758045554dc216576bb2999700529f2492a7))
* Variables in step name were not parsed ([`8498b31`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/8498b31a28754a037459acb45c978bf8b43d772e))

## v3.34.1 (2023-12-27)

### Fix

* Cannot import name 'RequestWithOptionalArgs' from 'httprunner.testcase' ([`0db06fa`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/0db06fa59378b73dc3d8314c4cf675b5eb6ba757))

## v3.34.0 (2023-12-27)

### Feature

* Add validator is_truthy and is_falsy ([`1b30491`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/1b304911235b0e3bd8a66a0e84e1b8fdc87af9de))
* No longer print client and server ip in logs ([`32e6e54`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/32e6e546b75688fd7cdff8378af193ed130d5a77))
* Save exported variables to allure report for RunTestCase step ([`9d9dd11`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/9d9dd116e9ff84afa337e3665ada53ed61b4a424))
* Continue on JMESPathError ([`1f88731`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/1f887315403fa555d0940db3b6a68792779bee28))
* Add new exception MultiStepsFailedError for continue_on_failure ([`3033e5b`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/3033e5bd2cfb8f01e19c140383355f2a020aff8e))
* Support continue_on_failure again ([`6725c97`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/6725c976e2f4124d7ec7e011d48fc998d9f14b2a))
* Do not export variables if validation failed ([`8fca2b5`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/8fca2b5cd036de292f53ee1e758feb225bd4dc30))

### Fix

* Last retry was always marked success even exception was raised ([`d88e598`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/d88e59810f2a7ce117c81841fe89871135a39ee4))
* The reason of why testcase failed is misunderstanding when RequestException occurs ([`cdd5d09`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/cdd5d095ebdfabf28ab386c4cd7aae4394fbc84d))
* Request headers and body was not displayed appropriate in log ([`d114f33`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/d114f3351603382055ed0f347599a0447ea6a97d))
* RunTestCase step show as success even some steps failed when __continue_on_failure was set to True ([`9bc894f`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/9bc894fbff7bc11ec8bf6bded3db07699a9ff2d6))
* Dictionary keys changed during iteration ([`9bf8e40`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/9bf8e407a330fb6088d74785acddd2bffce68588))
* F401 'typing.Union' imported but unused ([`1b8c25b`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/1b8c25b2892152b453429f212fc4a096e0e1d9c0))

### Performance

* Print variable names only when VariableNotFound raised ([`df01360`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/df01360887d11901dd163db27a60e149c6dcd871))

## v3.33.2 (2023-12-15)

### Fix

* Replace model.model_dump() with dict() to retain file content ([`30cb72e`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/30cb72ecee957ac944b4640c1a0ea43b64f4cc58))

## v3.33.1 (2023-12-15)

### Fix

* AttributeError: 'tuple' object has no attribute 'extend' ([`0dfed66`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/0dfed66795adb4ae304797beb4b1148aa668780d))

## v3.33.0 (2023-12-08)

### Feature

* Add comparators for schema validators ([`5b11076`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/5b1107664c6e08c719c073baa84e2e69e942aa53))
* Add two assert method for validating data schema ([`c9d54fc`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/c9d54fc3ca8107bcc976175618084530cf0ddeba))
* Remove deprecated assertion ([`9381049`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/9381049fdd8bcb7e1f1b2cc5f4eed6e4e474cd9f))
* Add fallback for BaseModel.model_dump_json() ([`4f3a4b0`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/4f3a4b026c287534cbe78825d3b662e3280af32b))
* Display response content-length at the end of title when retrying is required ([`a66b7fc`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/a66b7fcb904018cf680b1e6e0e435853463c6bc1))

### Fix

* Type hint for BaseModel ([`b6b7b86`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/b6b7b8633c8c40733b88dc39b5299675db8ed1b1))
* Assert on error message instead of `assert model_validate()` ([`4103df8`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/4103df8a3215af54f3e7a5b2f1ad2d12f9e569a7))
* Assert on error message instead of `assert validate()` ([`042176b`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/042176b18d4945d0d8887d4dca6010bbf97b3548))
* `dumps_kwargs` keyword arguments are no longer supported ([`d3d1c4f`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/d3d1c4ff6994343a575b1576064b627cc1139f87))
* Copy step when instantiating HttpRunnerRequest ([`3534516`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/353451614d1bbf2a3d9ffd2092fe357d219f213f))
* Replace method `model_dump_json` with function `pydantic_model_dump_json` ([`ba1f3a6`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/ba1f3a6b091c8b8ff9d67c7f5612316c64ff7bb0))
* Add excepted TypeError ([`2bb5e59`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/2bb5e593adfda56939b08c8b2e060bff97f65b6f))
* Pydantic do not know type `Exception` ([`09eeb5b`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/09eeb5b0acc93417199848aea9d8fcf80d29bc44))
* Substitute deprecated methods with new methods ([`262d0f2`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/262d0f26985a9ee2b42d7a44844cc4181045b459))
* Substitute deprecated methods with new methods ([`f270194`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/f270194f6f42270a12d5c49c1ea5d95996997498))
* Substitute deprecated methods with new methods ([`35f7a2a`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/35f7a2a014ba17a50139f0993787340982382ac5))
* Parametrized testcase always use the first parameter set after upgrading pydantic ([`9a0938d`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/9a0938dd1f40b1729da89335ef803c711b73e5eb))

### Performance

* Fail fast when decoding to json ([`aa64e19`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/aa64e191a860ffbf01fe1a7cc0ae4f2f1229c840))
* Annotate specific fields combining Annotated and PlainSerializer to decrease looping times ([`ecc5f96`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/ecc5f967d31e8868dc1312e077d5910e1e519ceb))

## v3.32.2 (2023-11-27)

### Fix

* Retry parsing on NameError when parsing expression `pyexp` ([`fee0eac`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/fee0eac3516d55765e5b688662089631b458c922))

## v3.32.1 (2023-11-17)

### Fix

* Bad reference ([`6776f26`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/6776f26912e460ebd1af11bbba0c74b88cd3b26d))
* Make priority of custom content-type higher than that guess via file content ([`7d93675`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/7d93675c107184aa9e352f97e0e8b09a9fee202e))

## v3.32.0 (2023-10-31)

### Feature

* Add parameter `is_skip_empty_parameter` (default: True) to enable skipping steps when argvalues are empty ([`d69207a`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/d69207a0421793611a8bc57610bfc4151a037c9f))

### Fix

* Clear step's variables if the step was supposed to be skipped ([`8e8bbf6`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/8e8bbf60fca86a28b54c59971691390e50ecb63e))

### Documentation

* Change the description of why step was skipped ([`b71c3de`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/b71c3de69b7108ad6bc1afba81f827d6b6092cb6))

## v3.31.1 (2023-10-30)

### Fix

* Do not parse step.variables before expanding parametrized step ([`2f92b80`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/2f92b8005b5f75981a3ba9a0201888ffaeba2d81))

## v3.31.0 (2023-09-13)

### Feature

* Enable validator `all` adding additional keyword arguments ([`f9be706`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/f9be7066ba407a79484bac4cab54a11eb11f020c))

## v3.30.0 (2023-09-13)

### Feature

* Add validator `assert_all` to assert all elements are true ([`d32fe6b`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/d32fe6b2b4fc32b65481b495f4bc296f4d0231b2))

## v3.29.5 (2023-09-07)

### Fix

* Display class docstring as `Description` in allure report ([`02fe084`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/02fe084c9024cde63cd0fbd69a97b7f38e1caba6))

### Documentation

* Simplify test_start docstring to make it look better in allure report ([`9bfc303`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/9bfc3035354430c278dd410cb72b2f984a87903a))

## v3.29.4 (2023-09-02)

### Fix

* Debugtalk functions not found even functions are imported into debugtalk.py ([`90e16f2`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/90e16f24529e693eb3a68a3d5d4cb1f237fe88d6))

## v3.29.3 (2023-09-01)

### Fix

* Debugtalk functions not found when collecting fixtures from dependencies ([`1107119`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/11071191c2f36912088a30c02ab3b1affd3668ce))

## v3.29.2 (2023-08-29)

### Fix

* Functions imported into debugtalk.py will not be recognized as debugtalk functions in some conditions ([`8b1415d`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/8b1415de0248246f20a82c1ce6f745e0c5bd2967))

### Documentation

* Add warning for operation `chdir` ([`beb8c67`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/beb8c67e8e70b726a57b9f0090ce5bea80b305ae))
* Add warning for function `load_project_meta` ([`88f1728`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/88f172853d2948aef63c86b40ac4348be4ea480c))

## v3.29.1 (2023-08-25)

### Fix

* Raise exception when failed to get value from nested dict to avoid introducing new class Hasher ([`7ec3fb7`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/7ec3fb762f82b7ab952844eb8d6c805a1c0a71c4))

## v3.29.0 (2023-08-24)

### Feature

* Add entry point `httprunner.debugtalk` to enable loading debugtalk functions from entry points ([`242ba2f`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/242ba2f27d0b9266fa4125400711dc718939287b))

### Fix

* KeyError if entry point not set ([`99a7759`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/99a775950db38ea34f9f3c7ec3ecf76fc30964bd))

## v3.28.2 (2023-08-18)

### Performance

* Group dependencies to enable ignoring specific group ([`ee40681`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/ee40681421cbcf977373fc9870d8b26559765964))

## v3.28.1 (2023-08-17)

### Fix

* Flake8 error while comparing types with "==" ([`b4a6ffc`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/b4a6ffc84ecbf2c9c52e073f97259e2aeb913244))

### Performance

* Constraint packages narrowly to speed up dependency resolution process ([`0da75e1`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/0da75e115c16438ee3c8d5e3988fb3e3a4f59ff6))

## v3.28.0 (2023-08-15)

### Feature

* Add validators to enable additional validation on toml key ([`8e11bdc`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/8e11bdc55ee9f36df835bc3205dd9786f4a97fea))

## v3.27.1 (2023-08-15)

### Performance

* Add descriptor to implement lazy-load meta ([`78eb4ca`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/78eb4ca2d5b0d6bb50ae16217479812749287ee8))

## v3.27.0 (2023-08-10)

### Feature

* Add http headers for every http request if `http-headers` configured in pyproject.toml ([`02b52b1`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/02b52b1744cc60e254df84421f12fdf268c8d3e7))
* Add module `pyproject` to load and parse pyproject.toml ([`2514b0c`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/2514b0c58f16a7aaaf1452cf29c79b44fc196bcb))
* Add module `dictionary` for nested dict ([`4c889f5`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/4c889f59028d08aaf4917c5d8c5be1dc32d515d3))
* Add plugin for pytest to support 'continue on failure' ([`e8d84b9`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/e8d84b91a5cc4d1047edb60babc4645d43eeb277))

### Fix

* Key error raised if first key exists but remaining keys do not exist ([`4ff3f4e`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/4ff3f4e3a24a030130957b3d3f01dc3048095685))

### Documentation

* Make docstring consistent ([`ef0ac24`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/ef0ac249082a242fe90f9f8c40c78b1863145518))
* Add examples ([`b2ec8fe`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/b2ec8fe08dade37bb0eb7b526ede8787868951de))

## v3.26.0 (2023-07-25)

### Feature

* Add argument `sub_extractor` to enable extracting on the result of jmespath querying ([`8c9533a`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/8c9533a96b7a26073dd159bf210e115448c87606))

## v3.25.2 (2023-07-20)

### Fix

* Add config env_prefix to avoid breaking allure report ([`6ee6f78`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/6ee6f785ecfee5a0b139a01ce3020f10d35e091e))

## v3.25.1 (2023-07-18)

### Fix

* **build:** Bump pyyaml to 6.0.1 to resolve pep517 error ([`09f8f61`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/09f8f619b7e79de8974446988aa57e484c7848ee))

## v3.25.0 (2023-06-26)

### Feature

* Add argument `stop_retry_if` to method `retry_on_failure` to support stopping retrying before max retries reached ([`431ae82`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/431ae8293838d63a1ba86ad2bdb4807abbd906a8))

## v3.24.5 (2023-06-21)

### Fix

* Append variables dumped to step name cause VariableNotFound error ([`93e5897`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/93e58978d0f4dd6ed25922ed03fc50556e501fa4))

## v3.24.4 (2023-06-20)

### Fix

* Type `set` and `tuple` will be converted to list after parsing ([`1d4dd51`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/1d4dd513cea9573ca19efe42dea99040e0f466b0))

### Documentation

* How to pass in an tuple as expected value in JSONassert methods ([`0ca4e62`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/0ca4e620b62e5c4aa9b7a3bfc957050b7d66fc66))

## v3.24.3 (2023-06-19)

### Fix

* Reformat allure failure message to make it more readable ([`6c37550`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/6c37550069349104ec19c34ef9cb82a1b0b9b116))

## v3.24.2 (2023-06-15)

### Fix

* Set req_json/data to blank dict if current value is None ([`e296ceb`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/e296ceb68d1911356bb8f2d046dada3ad0f3931d))

## v3.24.1 (2023-06-15)

### Fix

* F-string is missing placeholders ([`8da8b55`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/8da8b556607ef69c281bb71d1afeca1d19b0ab9e))
* Request got unexpected argument `req_json_update` ([`ba366d7`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/ba366d700c42042b68b55465821b40ea8b00af22))
* Calling `update_json_object()` again overwrites the value set by the first time ([`cbfa079`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/cbfa07961d1fd9afc26c3aa52594aac33288380c))

## v3.24.0 (2023-06-13)
### Feature
* Add method `with_variables_raw` to support expanding variables with that parsing from string ([`be8e8d1`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/be8e8d184c6b957e7f05f70bc56faad8d7790db9))

### Fix
* Parametrize failed to parse variables extracted from previous steps ([`66dcd4e`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/66dcd4e37467356f1b7b516c8a95817c850a99b7))

## v3.23.1 (2023-05-16)
### Fix
* Replace DotMap with DotWiz to resolve `json.dumps()` bad results (empty dict) ([`c0f564d`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/c0f564d572835101ca39c6c7ba422137f490c4b6))

## v3.23.0 (2023-05-06)
### Feature
* Parameter 添加使用正交生成用例集 ([`a90f8a3`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/a90f8a3d552ce6eb8f481771a2787429980054e4))

## v3.22.0 (2023-04-28)
### Feature
* Substitute `DotDict` with lib `dotmap` ([`4b91a2f`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/4b91a2f3a8ade5dfb9d29c5a2f2e32658ebfd4ac))

## v3.21.0 (2023-04-28)
### Feature
* Skip DotDict and return it as is when parsing ([`df7985a`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/df7985a72b0e43c528c16f3fcb429e33d6ea19b3))

## v3.20.3 (2023-04-27)
### Fix
* Signature of method does not match signature of base method in class ([`1646fb7`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/1646fb7616794f7e5776d65f1532d0c47ef411db))

## v3.20.2 (2023-04-13)
### Fix
* Set parsing timeout to 15s ([`c108220`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/c108220366ecd24901ece9647edc571659251793))

## v3.20.1 (2023-03-30)
### Fix
* Mark variables whose name starting with '_r_' as parsed and keep the value as is to avoid parsing extracted string containing dollar ([`373091e`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/373091ea77ed95b77038bca037dafed2415edae3))

## v3.20.0 (2023-03-29)
### Feature
* Implement parametrizing one step ([`959c79e`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/959c79e4df6eebf1bb17fbde55fc5e79c7b487f3))
* Add method 'parametrize()' to enable parametrizing one step ([`3abf781`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/3abf781f58b4d39cdeb9d7634f9bbef3a834298f))

### Fix
* F-string is missing placeholders ([`b1abc35`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/b1abc35540a96957f247eac05117edd57c0a3e92))
* Ids can be an empty list ([`b999cbb`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/b999cbbfca3935269289b9178b9e41826ee81cea))
* Raise exception if argvalues is an empty list ([`e67b67e`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/e67b67e834156d3d014ebc023cd37104561a5150))
* == should be != ([`6b7ec0b`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/6b7ec0b9a68538d284a0c8c48112e762ddec6076))
* Recover variable priority to make private variables got the highest priority ([`f5bbd70`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/f5bbd70f2607c5db27c8d58d2ba676cd9ec8e688))

## v3.19.2 (2023-03-23)
### Fix
* Adjust HttpRunnerRequest variable priority to comply with RunTestCase ([`a3b4246`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/a3b4246e2f334306a7b26967d2eed51bbb159a8d))

### Documentation
* Change the meaning of field builtin_variables ([`c721bfe`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/c721bfe85d37008bf58d45abecf03e70f824c221))
* Adjust priority ([`4d7ddf7`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/4d7ddf7851515912307782daee72aa6bdfd562f8))
* How builtin_variables was set ([`ca073dd`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/ca073dd20afe366fae2f3c45b06401aff00f15ed))

## v3.19.1 (2023-03-22)
### Fix
* Set config.path when subclassing HttpRunner to eliminate the bad affect on performance introduced by inspect.stack() ([`40dd4e9`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/40dd4e97741cceb558a4182c9d0a6c37e0d54145))

### Documentation
* Denote how the project root directory was searched ([`87cd09d`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/87cd09d27fadcd3979f0a949ee2c380acb7941a5))
* Denote that project meta was determined by the first testcase ([`ac67d56`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/ac67d56461db42fe38a165da3a2d25711356a63b))

## v3.19.0 (2023-03-21)
### Feature
* Disable validating jmespath expression before running test steps ([`5ea1365`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/5ea1365cceaa8fa41e0af4c243361d2771aa2b7d))

## v3.18.0 (2023-03-17)
### Feature
* Validate jmespath expression before running test steps ([`4846aa2`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/4846aa2294e411bb530884bfaf6825f74542f224))

### Fix
* Operator 'in' will cause exception if check item is not str ([`2d40167`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/2d40167ea71a509df29d2ff385febed202b343bc))

### Documentation
* Replace word 'duplicate' with 'copy' ([`771bf5e`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/771bf5ea9975ef8a9dac35e3422b33681ffefe8a))

## v3.17.1 (2023-03-10)
### Fix
* Cannot reference emoji settings from validation settings ([`08c1866`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/08c18667aa9f28b08de93c7ec5907c930760bfe2))

## v3.17.0 (2023-03-08)
### Feature
* Add expression "${pyexp()}" to enhance parsing ability ([`213d4bb`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/213d4bbc93d5a0cadc5d279eff032a7c907b7598))
* Add __init_subclass__ to validate subclass and fail fast ([`bdc7b5f`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/bdc7b5fab196270029f069c554ba8b4eb2aed959))
* Add validation method assert_is_close() ([`b8bbe60`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/b8bbe6015c9cdace139d921f8a70e660ad94aff9))
* Replace words 'PASS', 'FAIL' with emoji to increase readability of allure report ([`c4b8900`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/c4b890046967ebcb328dc00692529b7a7b889b97))
* Extract 'Date' from request headers and display it in attachment title ([`9d0ddfd`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/9d0ddfdb9b19378af8568231eb6841a90bb59adc))
* Set request header 'Date' to represent request timestamp ([`283cb89`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/283cb8917004b686b3663e7e7b72731abcbe1f95))

### Fix
* Json dumps error when functions exist in validation result ([`1257ddf`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/1257ddf003075195eaf86da40b4fe58c5ccc1496))
* Add custom JSONEncoder for validation results to fix JSON serializing error ([`b4a66f4`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/b4a66f4553e93f57726a4dc6db34ee4012533781))

## v3.16.11 (2023-02-09)
### Fix
* Variables cannot be identified when parsing eval_var and VariableNotFound exception raised ([`06b8de9`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/06b8de98a0a2d0d9ea52b744ea8d46a07ae463c3))
* String comparison failure when blank spaces exist at end/start of line ([`5ede49e`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/5ede49e7ca7332fae449da95d1b9c9ce6b06b836))

## v3.16.10 (2023-02-01)
### Fix
* Class instance is not JSON serializable ([`5d4a2c3`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/5d4a2c3e5c59a935ea50797125b24061debffbb7))

## v3.16.9 (2023-01-29)
### Fix
* Eval_var cannot parse a dict (only str is supported) ([`e49c767`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/e49c767f758768423dc52f0970741c701084b2a0))

## v3.16.8 (2022-12-23)
### Fix
* Add BytesEncoder to fix 'Object of type bytes is not JSON serializable' ([`feb53a5`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/feb53a5ce866d23b79c4985a221b2f945028bd4c))

## v3.16.7 (2022-12-19)
### Fix
* Variable not found when update_json_object not applied first ([`9b204da`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/9b204da33d38c96cb32af3229692175e54e0bb1b))

## v3.16.6 (2022-12-18)
### Fix
* Update request when running testcase to support debugtalk and variables ([`282157a`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/282157a31c5db076743b6459ea85ce56bdc6caa6))

## v3.16.5 (2022-12-16)
### Fix
* Swap the priority order between step variables and step builtin variables ([`a2cfb56`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/a2cfb565dca896be2f85de359d44ddf5fe68d672))

### Documentation
* Add comment on variable priority ([`20461da`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/20461da4da4ecf2bbbc78bc1a82e20186a5057bc))

## v3.16.4 (2022-12-14)
### Fix
* Variables parsing loop forever for request config variables are merged into step variables before parsed ([`ab5a1ba`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/ab5a1bae78b931d94e16395cb90e5c084a6b5d0a))

### Documentation
* Document variables priority in test ([`fcde34f`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/fcde34fc157ee1cb3f7b2f7273aaafbe04488a25))

## v3.16.3 (2022-12-01)
### Fix
* Add type 'str' into type hint to support debugtalk or httprunner variable string ([`94680a0`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/94680a0bddfb8e024e47516454bf6a8c5f1b404e))

## v3.16.2 (2022-11-11)
### Fix
* Replace $ with $$ to make sure parse_variables_mapping works fine ([`f0879d4`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/f0879d4483293a110abc636d44b8cc7fe9b24805))

## v3.16.1 (2022-11-02)
### Fix
* Allure attachments were not saved when exception is not ValidationFailure ([`ac801da`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/ac801dab5aab6761f0687d4778fff88331b625ee))

## v3.16.0 (2022-10-30)
### Feature
* Add support to parsing specific class instances ([`ef90726`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/ef90726950be63f4284b390d5e254113e9e11c3c))

## v3.15.0 (2022-10-26)
### Feature
* Add method clear() to clear validators and extract ([`73ec22b`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/73ec22bbf7463211e17b5fc87f905d2b077b2480))

### Fix
* Add 'return self' to enable chain call ([`2d2f4aa`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/2d2f4aa9427f62aef092faa84b351791c455f23e))
* Union StepRequestExport to ignore warning when export was called last ([`c5a6b47`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/c5a6b47c8b7fdb50016d2e9955b0dd1760bc9d1d))

## v3.14.1 (2022-10-25)
### Fix
* Testcase config vars overwritten by step request config vars ([`9f3b5ff`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/9f3b5ff4b8a59f430588effc80af4289fb105423))

## v3.14.0 (2022-10-24)
### Feature
* Add class HttpRunnerRequest to support adding extra setup, validate, export, and extract ([`07cd647`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/07cd647e733b6373223315af5f5a86df21663aaf))

### Fix
* Import merge_variables with absolute import statement ([`9aed34b`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/9aed34b48bab54a0d02db82389ae821825ea4a57))
* Make a duplication of TStep to prevent side effect ([`7ecc697`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/7ecc69752e486da0365e25989fb072a8d34422f7))
* Assign the result of variables merging back to instance attribute to fix merging not worked ([`e480ce8`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/e480ce8ba9c3f6a31ec223b33f374e38ce2da865))
* Rename private attributes to make them protected and accessible when subclassing ([`e9441ca`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/e9441ca7999423afc6f811cdba9ed7abf5c24147))

## v3.13.1 (2022-10-21)
### Fix
* Call set_use_allure() in nested testcase-like steps ([`f88d242`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/f88d242bc13a93da2ab3342a42324de8bfe24c84))

## v3.13.0 (2022-10-21)
### Feature
* Add attribute __use_allure to control allure data saving in testcase-specific scope ([`fe7d32c`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/fe7d32cc5a0f50b85ec83103de84d88d5f77cf88))

## v3.12.1 (2022-10-18)
### Fix
* Set field TStep.export as None by default and initiate an object when calling method export() ([`fe0d710`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/fe0d71070368af4c123629e3334bfc1c6ca6d93a))

## v3.12.0 (2022-10-17)
### Feature
* Add support to export variables from testcase referenced with specified names ([`4a55baf`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/4a55bafcf5c3b9560e9f436d810ef648a8b464d7))

### Fix
* Pop keys outside for loop to avoid 'dictionary changed size during iteration' ([`58a1250`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/58a1250e4c7ea4d4aefb6fa8de2b82e4cdc708c2))
* Replace ConfigExport with list to fix "Subscripted generics cannot be used with class and instance checks" ([`f9cd093`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/f9cd0933faa8a8fdd0c752b56496e6041911ea7a))

### Documentation
* Add docs for method export() ([`ec567ff`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/ec567ff0d52003b26af62ad9b993a58efe729826))

## v3.11.2 (2022-09-13)
### Fix
* Make the data type of skip condition as Any ([`7ee8e14`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/7ee8e14a1c17bb1a7b9d7a5e8af643262d0eb911))

## v3.11.1 (2022-08-23)
### Fix
* Eval condition only when result parsed by httprunner was str to fix unexpected eval result ([`061ad38`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/061ad385f9eb9d00db5793f571eca7c455453b7e))

## v3.11.0 (2022-08-22)
### Feature
* 添加java版本json_contain断言入口 ([`7b2e95c`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/7b2e95c01959626ea44a6f32ff6ccae2e2573c6e))

## v3.10.0 (2022-08-19)
### Feature
* Add skip_unless to run step only when condition was met ([`a169291`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/a1692918f8d40b7c12367fb2ad6672015402c470))

## v3.9.2 (2022-08-17)
### Fix
* Omit long data to increase allure report readability ([`af50726`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/af50726a052a69cdcd9e07e79f2976c572b7fda6))

## v3.9.1 (2022-08-04)
### Fix
* Do not save logging messages to log files to free disk space ([`21f9f89`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/21f9f89e8ca57edfe6795eb8ace59b642e0a9a46))

## v3.9.0 (2022-07-22)
### Feature
* Add Config.continue_on_failure() to continue running next steps when one step failed ([`5ef0cf3`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/5ef0cf3955276ee81be6d12ef36628ba79bd9175))

### Fix
* AttributeError when run debug_test ([`4e89c6a`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/4e89c6af23d7b473c6b88d377ba180dab7106fca))
* 'NoneType' object has no attribute 'exception' when step was skipped ([`f18945d`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/f18945d03ddf6abb87d02626150fbca396e9f927))
* Session_success incorrect when retrying steps ([`b4722a0`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/b4722a06aa4849c5931856905073ad7b8db52cb4))

### Documentation
* Add comment to explain field SessionData.success ([`e4530fe`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/e4530fec2c1a39aea470c5dfcf4ee7bba324678b))
* Add comment to indicate that data of each request is isolated ([`1a4301f`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/1a4301fd9351970683d1d4c299fea3db92b93469))

## v3.8.0 (2022-07-11)
### Feature
* Add method 'with_origin' to enable substituting url origin before sending requests ([`5188c0c`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/5188c0c3acfc920078edb4fdd2e0605a4f797a76))

### Performance
* Call black to format files before pre-commit ([`fa242d0`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/fa242d03d748a3b7ccdc7da349895f84d97080da))

## v3.7.3 (2022-06-24)
### Fix
* **parser:** Loop forever when key contains '$' ([`09dbdf4`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/09dbdf4513507d04334568b4660783e27a365519))

## v3.7.2 (2022-06-24)
### Fix
* **parser:** Include leading variable of expression when extracting variables from raw_string to fix loop forever ([`5194268`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/5194268ddba8c8331cca9d84a67e2f44ad47b6e8))

## v3.7.1 (2022-06-09)
### Fix
* Save statistics of session data to allure ([`f3c7c2b`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/f3c7c2b154c906173bfbdcea8cdb560a79b7fe7d))

## v3.7.0 (2022-06-08)
### Feature
* **deprecated:** Remove the functionality of collection statistics, implement it in client ([`7d3cd4c`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/7d3cd4c31837a8cc5a6230ab35a5d90f60baa664))

## v3.6.0 (2022-06-08)
### Feature
* Add module statistics to enable retrieving statistics info of testcases ([`a23790b`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/a23790ba6e1170a4eb895eac7fea1897d3a4d9dd))

### Fix
* Type hint error ([`3ab81a5`](https://fangcun.vesync.cn/raigordeng/httprunner/-/commit/3ab81a5a1320d52f98b150ba5beca0b6aadf5ac9))

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
