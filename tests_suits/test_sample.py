def func(x):
    return x + 1

def test_answer():
    assert func(3) == 4

def test_comfig(config):
    assert config["base_url"] == "https://m.twitch.tv/"