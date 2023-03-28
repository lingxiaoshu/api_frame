# !/usr/bin python3                                 
# encoding: utf-8 -*-                            
# @author:   夭夭 QQ：3512937625
# @Time:   2021-04-26
# @Copyright：北京码同学网络科技有限公司
import hashlib
import base64
import hashlib

from Crypto import Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 as PKCS1_signature
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher, AES



def md5(text):
	result = hashlib.md5(text.encode()).hexdigest()
	return result

# 对称加密:加密和解密的秘钥是一个
class AesEncrypt:
	"""
    AES加密
    	windows
		pip install pycryptodome -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
		找到site-package的包 然后把crypto 的c改成大写的即可
		mac下 pip install pycrypto -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
    """

	def __init__(self, key):
		self.key = key  # 初始化密钥 开发给的
		self.length = AES.block_size  # 初始化数据块大小
		self.aes = AES.new(self.key.encode("utf8"), AES.MODE_ECB)  # 初始化AES,ECB模式的实例
		# 截断函数，去除填充的字符
		self.unpad = lambda date: date[0:-ord(date[-1])]

	def pad(self, text):
		"""
        填充函数，使被加密数据的字节码长度是block_size的整数倍
        """
		count = len(text.encode('utf-8'))
		add = self.length - (count % self.length)
		entext = text + (chr(add) * add)
		return entext

	# 加密函数
	def encrypt(self, encrData):  # 加密函数
		'''

		:param encrData: 需要加密的数据
		:return:
		'''
		res = self.aes.encrypt(self.pad(encrData).encode("utf8"))
		msg = str(base64.b64encode(res), encoding="utf8")
		return msg

	# 解密函数
	def decrypt(self, decrData):  # 解密函数
		res = base64.decodebytes(decrData.encode("utf8"))
		msg = self.aes.decrypt(res).decode("utf8")
		return self.unpad(msg)


class RsaEncrypt():
	"""
    初始化时必须传递公钥和私钥存储的文件路径
    """

	def __init__(self, public_file, private_file):
		self.public_file = public_file  # 公钥  开发给的
		self.private_file = private_file  # 私钥  开发给的

	def generate_key(self):
		"""
        这个方法是生成公钥和私钥的，在实际企业测试过程中，开发会提供公钥和私钥，我们不用自己生成
        :return:
        """
		random_generator = Random.new().read
		rsa = RSA.generate(2048, random_generator)
		# 生成私钥
		private_key = rsa.exportKey()
		# print(private_key.decode('utf-8'))
		# 生成公钥
		public_key = rsa.publickey().exportKey()
		# print(public_key.decode('utf-8'))

		with open(self.private_file, 'wb')as f:
			f.write(private_key)

		with open(self.public_file, 'wb')as f:
			f.write(public_key)
			print('生成')

	# 从秘钥文件中获取密钥
	def get_key(self, key_file):
		with open(key_file) as f:
			data = f.read()
			key = RSA.importKey(data)
		return key

	# rsa 公钥加密数据
	def encrypt_data(self, msg):
		public_key = self.get_key(self.public_file)
		cipher = PKCS1_cipher.new(public_key)
		encrypt_text = base64.b64encode(cipher.encrypt(bytes(msg.encode("utf8"))))
		return encrypt_text.decode('utf-8')

	# rsa 私钥解密数据
	def decrypt_data(self, encrypt_msg):
		private_key = self.get_key(self.private_file)
		cipher = PKCS1_cipher.new(private_key)
		back_text = cipher.decrypt(base64.b64decode(encrypt_msg), 0)
		return back_text.decode('utf-8')

	# rsa 私钥签名数据
	def rsa_private_sign(self, data):
		private_key = self.get_key(self.private_file)
		signer = PKCS1_signature.new(private_key)
		digest = SHA.new()
		digest.update(data.encode("utf8"))
		sign = signer.sign(digest)
		signature = base64.b64encode(sign)
		signature = signature.decode('utf-8')
		return signature

	# rsa 公钥验证签名 sign也是开发给的
	# 客户端-发起请求
	def rsa_public_check_sign(self, text, sign):
		publick_key = self.get_key(self.public_file)
		verifier = PKCS1_signature.new(publick_key)
		digest = SHA.new()
		digest.update(text.encode("utf8"))
		return verifier.verify(digest, base64.b64decode(sign))


if __name__ == '__main__':
	# password = 'yaoyao123456'
	# pwd = md5(password)
	# print(pwd)
	##以下是aes的对称加密方法
	# 重点：这个key必须是16位
	# aes = AesEncrypt('abcdefghiaqwerty')
	# # 加密方法
	# aa = aes.encrypt('python自动化')
	# print(aa)
	# # 解密方法(验证)
	# bb = aes.decrypt(aa)
	# print(bb)

	## 以下是rsa的非对称算法
	# 两个参数是保存公钥和私钥的文件
	rsa = RsaEncrypt('public_key.keystore', 'private_key.keystore')
	## 生成公钥和私钥 并保存到两个文件中
	rsa.generate_key()  # 正常工作不需要调用这个方法
	## 进行加密
	aa = rsa.encrypt_data('python自动化')
	print(aa)
	## 进行解密
	bb = rsa.decrypt_data(aa)
	print(bb)
