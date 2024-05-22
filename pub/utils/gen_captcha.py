import math
import os
import random
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont, ImageFilter
from flask import make_response


def gen_captcha():
    image, code = VieCode().get_code_image()
    code = ''.join(code).lower()
    out = BytesIO()
    image.save(out, 'png')
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    return resp, code


class VieCode:
    __fontSize = 20  # 字体大小
    __width = 120  # 画布宽度
    __height = 45  # 画布高度
    __length = 4  # 验证码长度
    __draw = None  # 画布
    __img = None  # 图片资源
    __code = None  # 验证码字符
    __str = None  # 自定义验证码字符集
    __inCurve = True  # 是否画干扰线
    __inNoise = True  # 是否画干扰点
    __type = 2  # 验证码类型 1、纯字母  2、数字字母混合
    __font_patn = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts', '1.ttf'))  # 字体

    def get_code_image(self, size: int = 80, length: int = 4):
        """
        获取验证码图片
        @param size 验证码大小
        @param length 验证码长度
        """
        # 准备基础数据
        self.__length = length
        self.__fontSize = size
        self.__width = self.__fontSize * self.__length
        self.__height = int(self.__fontSize * 1.5)

        # 生成验证码图片
        self.__create_code()
        self.__create_image()
        self.__create_noise()
        self.__printString()
        self.__create_filter()

        return self.__img, self.__code

    def __create_filter(self):
        """模糊处理"""
        self.__img = self.__img.filter(ImageFilter.BLUR)
        filter = ImageFilter.ModeFilter(8)
        self.__img = self.__img.filter(filter)

    def __create_code(self):
        """创建验证码字符"""
        # 是否自定义字符集合
        if not self.__str:
            # 源文本
            number = "3456789"
            srcLetter = "qwertyuipasdfghjkzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
            srcUpper = srcLetter.upper()
            if self.__type == 1:
                self.__str = number
            else:
                self.__str = srcLetter + srcUpper + number

        # 构造验证码
        self.__code = random.sample(self.__str, self.__length)

    def __create_image(self):
        """创建画布"""
        bgColor = (random.randint(200, 255), random.randint(200, 255), random.randint(200, 255))
        self.__img = Image.new('RGB', (self.__width, self.__height), bgColor)
        self.__draw = ImageDraw.Draw(self.__img)

    def __create_noise(self):
        """画干扰点"""
        if not self.__inNoise:
            return
        font = ImageFont.truetype(self.__font_patn, int(self.__fontSize / 1.5))
        for i in range(5):
            # 杂点颜色
            noiseColor = (random.randint(150, 200), random.randint(150, 200), random.randint(150, 200))
            putStr = random.sample(self.__str, 2)
            for j in range(2):
                # 绘杂点
                size = (random.randint(-10, self.__width), random.randint(-10, self.__height))
                self.__draw.text(size, putStr[j], font=font, fill=noiseColor)
        pass

    def __create_curve(self):
        """画干扰线"""
        if not self.__inCurve:
            return
        x = y = 0

        # 计算曲线系数
        a = random.uniform(1, self.__height / 2)
        b = random.uniform(-self.__width / 4, self.__height / 4)
        f = random.uniform(-self.__height / 4, self.__height / 4)
        t = random.uniform(self.__height, self.__width * 2)
        xend = random.randint(self.__width / 2, self.__width * 2)
        w = (2 * math.pi) / t

        # 画曲线
        color = (random.randint(30, 150), random.randint(30, 150), random.randint(30, 150))
        for x in range(xend):
            if w != 0:
                for k in range(int(self.__height / 10)):
                    y = a * math.sin(w * x + f) + b + self.__height / 2
                    i = int(self.__fontSize / 5)
                    while i > 0:
                        px = x + i
                        py = y + i + k
                        self.__draw.point((px, py), color)
                        i -= i

    def __printString(self):
        '''打印验证码字符串'''
        font = ImageFont.truetype(self.__font_patn, self.__fontSize)
        x = 0
        # 打印字符到画板
        for i in range(self.__length):
            # 设置字体随机颜色
            color = (random.randint(30, 150), random.randint(30, 150), random.randint(30, 150))
            # 计算座标
            x = random.uniform(self.__fontSize * i * 0.95, self.__fontSize * i * 1.1)
            y = self.__fontSize * random.uniform(0.3, 0.5)
            # 打印字符
            self.__draw.text((x, y), self.__code[i], font=font, fill=color)
