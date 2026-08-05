from locust import HttpUser, task, between


class SauceDemoUser(HttpUser):
    """
    Load test for saucedemo.com's static page delivery.

    saucedemo.com is a client-side-routed SPA: only "/" is a real server
    endpoint (verified with curl -- "/inventory.html" and other routes
    return 404 on a direct GET, since routing happens in the browser after
    JS loads). There's no real backend to exercise (login is validated
    against hardcoded credentials in client-side JS), so this measures
    page-load latency/throughput under concurrent load, not business logic.
    """

    wait_time = between(1, 3)

    @task
    def load_home_page(self):
        self.client.get("/")
