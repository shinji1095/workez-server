import nox

@nox.session
def unit(session):
    session.install("-r", "requirements/local.txt")
    session.env.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
    session.run("pytest", "-q", "apps", external=True)

@nox.session
def integration(session):
    session.install("-r", "requirements/local.txt")
    session.env.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
    session.run("pytest", "-q", "tests", external=True)

@nox.session
def e2e_local(session):
    session.install("-r", "requirements/local.txt")
    session.env.setdefault("BASE_URL", "http://127.0.0.1:8000")
    session.run("python", "e2e/run_curl_suite.py", "e2e/suites/local.json", external=True)

@nox.session
def e2e_prod(session):
    session.install("-r", "requirements/local.txt")
    session.run("python", "e2e/run_curl_suite.py", "e2e/suites/production.json", external=True)
