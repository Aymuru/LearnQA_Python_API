import pytest

class TestCheckhrase:
    new_phrase = input("Set a phrase: ")
    print("The length of your phrase - ", (len(new_phrase)), " symbols.")

    @pytest.mark.parametrize('phrase', [new_phrase])
    def test_check_len_phrase(self, phrase):
        a = (len(phrase))
        assert a < 15, f"The phrase in longer than 14 symbols."
