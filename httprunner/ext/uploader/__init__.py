""" upload test extension.

If you want to use this extension, you should install the following dependencies first.

- requests_toolbelt
- filetype

Then you can write upload test script as below:

    - test:
        name: upload file
        request:
            url: http://httpbin.org/upload
            method: POST
            headers:
                Cookie: session=AAA-BBB-CCC
            upload:
                file: "data/file_to_upload"
                field1: "value1"
                field2: "value2"
        validate:
            - eq: ["status_code", 200]

For compatibility, you can also write upload test script in old way:

    - test:
        name: upload file
        variables:
            file: "data/file_to_upload"
            field1: "value1"
            field2: "value2"
            m_encoder: ${multipart_encoder(file=$file, field1=$field1, field2=$field2)}
        request:
            url: http://httpbin.org/upload
            method: POST
            headers:
                Content-Type: ${multipart_content_type($m_encoder)}
                Cookie: session=AAA-BBB-CCC
            data: $m_encoder
        validate:
            - eq: ["status_code", 200]

"""

import os
import sys
from typing import Text, NoReturn

from loguru import logger

from httprunner.models import TStep, FunctionsMapping
from httprunner.parser import parse_variables_mapping, parse_data

try:
    import filetype  # noqa
    from requests_toolbelt import MultipartEncoder

    UPLOAD_READY = True
except ModuleNotFoundError:
    UPLOAD_READY = False


def ensure_upload_ready():
    if UPLOAD_READY:
        return

    msg = """
    uploader extension dependencies uninstalled, install first and try again.
    install with pip:
    $ pip install requests_toolbelt filetype

    or you can install httprunner with optional upload dependencies:
    $ pip install "httprunner[upload]"
    """
    logger.error(msg)
    sys.exit(1)


def get_filetype(file_path):
    file_type = filetype.guess(file_path)
    if file_type:
        return file_type.mime
    else:
        return "text/html"


def prepare_upload_step(step: TStep, functions: FunctionsMapping) -> "NoReturn":
    """preprocess for upload test
        replace `upload` info with MultipartEncoder

    Args:
        step: teststep
            {
                "variables": {},
                "request": {
                    "url": "http://httpbin.org/upload",
                    "method": "POST",
                    "headers": {
                        "Cookie": "session=AAA-BBB-CCC"
                    },
                    "upload": {
                        "file": "data/file_to_upload"
                        "md5": "123"
                    }
                }
            }
        functions: functions mapping

    """
    if not step.request.upload:
        return

    ensure_upload_ready()

    # convert keys to lowercase for keys of http headers are case-sensitive
    lowercase_headers = {k.lower(): v for k, v in step.request.headers.items()}

    # upload file as multipart/form by default
    upload_file_type = "multipart"

    # set upload_file_type with value extracted from header
    if "x-upload-file-as" in lowercase_headers:
        upload_file_type = lowercase_headers.get("x-upload-file-as")
        if upload_file_type not in ["multipart", "discrete"]:
            raise ValueError(
                f"Value for header 'X-Upload-File-As' can only be 'multipart' or 'discrete', "
                f"but got: {upload_file_type}"
            )

    # multipart
    if upload_file_type == "multipart":
        params_list = []
        for key, value in step.request.upload.items():
            step.variables[key] = value
            params_list.append(f"{key}=${key}")

        params_str = ", ".join(params_list)
        step.variables["m_encoder"] = "${multipart_encoder(" + params_str + ")}"

        # parse variables
        step.variables = parse_variables_mapping(step.variables, functions)

        # priority: custom content-type > guessed content-type
        if "content-type" not in lowercase_headers:
            step.request.headers[
                "Content-Type"
            ] = "${multipart_content_type($m_encoder)}"

        step.request.data = "$m_encoder"
    else:
        # discrete
        if (count := len(step.request.upload)) != 1:
            raise ValueError(
                f"one and only one file expected when uploading file as 'discrete', but got: {count}"
            )

        for key, value in step.request.upload.items():
            value = parse_data(value, step.variables, functions)

            if os.path.isabs(value):
                # value is absolute file path
                _file_path = value
                if not os.path.isfile(value):
                    raise FileNotFoundError(
                        f"file specified by absolute path {value} not exist"
                    )
            else:
                # value is not absolute file path, check if it is relative file path
                from httprunner.loader import load_project_meta

                project_meta = load_project_meta("")
                _file_path = os.path.join(project_meta.httprunner_root_path, value)
                if not os.path.isfile(_file_path):
                    raise FileNotFoundError(
                        f"no file '{value}' under '{project_meta.httprunner_root_path}' found"
                    )

            # priority: custom content-type > guessed content-type
            if "content-type" not in lowercase_headers:
                mime_type = get_filetype(_file_path)
                step.request.headers["Content-Type"] = mime_type

            # value is file path to upload
            file_handler = open(_file_path, "rb")
            step.request.data = file_handler


def multipart_encoder(**kwargs):
    """initialize MultipartEncoder with uploading fields.

    Returns:
        MultipartEncoder: initialized MultipartEncoder object
    """
    ensure_upload_ready()
    fields_dict = {}
    for key, value in kwargs.items():

        if os.path.isabs(value):
            # value is absolute file path
            _file_path = value
            is_exists_file = os.path.isfile(value)
        else:
            # value is not absolute file path, check if it is relative file path
            from httprunner.loader import load_project_meta

            project_meta = load_project_meta("")

            _file_path = os.path.join(project_meta.httprunner_root_path, value)
            is_exists_file = os.path.isfile(_file_path)

        if is_exists_file:
            # value is file path to upload
            filename = os.path.basename(_file_path)
            mime_type = get_filetype(_file_path)
            # TODO: fix ResourceWarning for unclosed file
            file_handler = open(_file_path, "rb")
            fields_dict[key] = (filename, file_handler, mime_type)
        else:
            fields_dict[key] = value

    return MultipartEncoder(fields=fields_dict)


def multipart_content_type(m_encoder) -> Text:
    """prepare Content-Type for request headers

    Args:
        m_encoder: MultipartEncoder object

    Returns:
        content type

    """
    ensure_upload_ready()
    return m_encoder.content_type
