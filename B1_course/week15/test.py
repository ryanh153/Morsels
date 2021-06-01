from solution import speed_test


def test_blank_call():
    assert isinstance(speed_test([]), dict)


def test_single_url():
    url = 'https://google.com'
    result = speed_test([url])
    assert isinstance(result, dict)
    assert url in result
    assert len(result[url]) == 4


def test_number_of_checks():
    url = 'https://google.com'
    checks = 2
    result = speed_test([url], number_of_checks=checks)
    assert url in result
    assert len(result[url]) == checks


def test_multiple_urls():
    urls = ['https://google.com', 'https://reddit.com']
    result = speed_test(urls)
    for url in urls:
        assert url in result
        assert len(result[url]) == 4
