def python_wheel(name, url, sha256):
    native.http_file(
        name = name + '_http',
        urls = [url],
        sha256 = sha256,
    )

    native.prebuilt_python_library(
        name = name,
        binary_src = ':' + name + '_http',
        visibility = [
            'PUBLIC'
        ],
    )
