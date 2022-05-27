import allure


def test_try_and_break():
    for i in range(10):
        try:
            print("hello")
            break
        finally:
            print("final action")


def do_nothing():
    pass


def nested_allure():
    with allure.step("level 2"):
        do_nothing()


def nested_nested_allure():
    with allure.step("level 3"):
        do_nothing()
        nested_allure()


@allure.title("测试 with allure 嵌套")
def test_nested_with_allure():
    with allure.step("level 1"):
        do_nothing()
        nested_allure()
        nested_nested_allure()
