import pytest
import json


@pytest.mark.usefixtures('api_utils')
@pytest.mark.usefixtures('reqres_page')
@pytest.mark.usefixtures('driver')
class TestReqRes:

    def test_ui_vs_api(self):
        self.req_page.go_main_page()
        self.req_page.chose_action()
        self.req_page.get_endpoint('/api/unknown')
        resource_api = self.api_util.get("/api/unknown?id=2", parse=True)
        resource_ui = self.req_page.resource_ui_parser()
        assert resource_api['data'] == resource_ui, "Resources are not equal in UI and API response"

    @pytest.mark.parametrize("req, exp_code",
                             [("/api/unknown?id=2", 200), ("/api/unknown?id=10000000", 404),
                              ("/api/unknown?page=2", 200), ("/api/unknown?page=1000000000", 404)]
                             )
    def test_res_stcodes_correct(self, req, exp_code):
        response = self.api_util.get(req, parse=False)
        assert response.status_code == exp_code, \
            "Unexpected status code {} for request {}, " \
            "expected - {}".format(response.status_code, req, exp_code)
