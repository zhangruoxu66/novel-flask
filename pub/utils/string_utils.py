from nltk.tokenize import RegexpTokenizer


# 获取字符串英文单词数量
def get_english_word_count(orig_str, pattern: str = None):
    tokenizer = RegexpTokenizer('\\b\\w+\\b' if not pattern else pattern)
    tokens = tokenizer.tokenize(orig_str)
    return len(tokens)


# 获取字符串中文汉字数量
def get_chinese_word_count(orig_str):
    tokenizer = RegexpTokenizer('[\u4e00-\u9fa5]')
    tokens = tokenizer.tokenize(orig_str)
    return len(tokens)


# 获取字符串有效数字数量
def get_number_word_count(orig_str):
    tokenizer = RegexpTokenizer('\\d+')
    tokens = tokenizer.tokenize(orig_str)
    return len(tokens)


def get_str_valid_word_count(orig_str):
    return get_chinese_word_count(orig_str) + get_english_word_count(orig_str, pattern=r"\w+") + get_number_word_count(
        orig_str)


def protect_mobile(mobile: str) -> str:
    """
    手机号脱敏
    :param mobile: 手机号
    :return: 脱敏后的手机号，例子：16666661111 -> 166****1111
    """
    if len(mobile) != 11:
        return mobile
    return mobile[0:3] + '****' + mobile[7:]


def test_valid_word_count():
    orig_str = "Welcome to China. 你好呀！中国人，我是1123号程序员，     来给你服务23天. Hello Word"
    print(get_chinese_word_count(orig_str))
    print(get_english_word_count(orig_str))
    print(get_english_word_count(orig_str, pattern='[a-zA-Z]+'))
    print(get_english_word_count(orig_str, pattern=r"\w+"))
    print(get_number_word_count(orig_str))


def test_protect_mobile():
    print(protect_mobile('16666661111'))


if __name__ == '__main__':
    test_valid_word_count()
    # test_protect_mobile()
