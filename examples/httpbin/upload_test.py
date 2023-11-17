# NOTE: Generated By HttpRunner v3.1.4
# FROM: upload.yml


from httprunner import HttpRunner, Config, Step, RunRequest


class TestCaseUpload(HttpRunner):

    config = Config("test upload file with httpbin").base_url("${get_httpbin_server()}")

    teststeps = [
        Step(
            RunRequest("upload file")
            .with_variables(
                **{
                    "file_path": "test.env",
                    "m_encoder": "${multipart_encoder(file=$file_path)}",
                }
            )
            .post("/post")
            .with_headers(**{"Content-Type": "${multipart_content_type($m_encoder)}"})
            .with_data("$m_encoder")
            .validate()
            .assert_equal("status_code", 200)
            .assert_startswith("body.files.file", "UserName=test")
        ),
        Step(
            RunRequest("upload file with multipart/form")
            .post("/post")
            .upload(**{"file": "test.env"})
            .validate()
            .assert_equal("status_code", 200)
            .assert_startswith("body.files.file", "UserName=test")
        ),
        Step(
            RunRequest("upload file with discrete mime type")
            .post("/post")
            .upload(**{"img": "foo.png"})
            .with_headers(**{"X-Upload-File-As": "discrete"})
            .validate()
            .assert_equal("status_code", 200)
        ),
        Step(
            RunRequest("upload file with discrete mime type and custom content-type")
            .post("/post")
            .upload(**{"email": "foo.eml"})
            .with_headers(
                **{"X-Upload-File-As": "discrete", "Content-Type": "message/rfc822"}
            )
            .validate()
            .assert_equal("status_code", 200)
        ),
    ]


if __name__ == "__main__":
    TestCaseUpload().test_start()
