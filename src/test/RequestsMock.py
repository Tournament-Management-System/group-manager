import requests
import requests_mock

@requests_mock.Mocker()
def test_function(m):
    m.get('http://test.com', text='resp')
    return requests.get('http://test.com').text

print(test_function())