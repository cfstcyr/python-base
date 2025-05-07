from app.main import main


def test_main(settings):
    main(settings=settings)
    assert True
