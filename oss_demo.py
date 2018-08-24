import oss2

sight_id = "1149160"
country_code = "thailand"
city_code = "bangkok"
pic_url = "https://pic.qyer.com/album/user/1785/42/QE5dRx4FYE0/index/225x150"
m = int(sight_id)%9
path = 'qyer/'


# 链接OSS 配置参数
config_oss2={
    'AccessKeyId': 'LTAIgZxQ3TtshmAB',
    'AccessKeySecret': '0F6juS5boKfbARqiJR6kBfRPHKBYTf',
     # 公网地址，用于本地测试
    'Endpoint': 'http://oss-cn-beijing.aliyuncs.com',
    'Host': 'http://x-pic.oss-cn-beijing.aliyuncs.com/',
     # 内网地址，用于服务器上运行
     #'Endpoint': 'http://oss-cn-beijing-internal.aliyuncs.com',
     #'Host': 'http://x-pic.oss-cn-beijing-internal.aliyuncs.com/',
    'BucketName': 'x-pic'
}
# 链接OSS 认证
auth = oss2.Auth(config_oss2['AccessKeyId'], config_oss2['AccessKeySecret'])
bucket = oss2.Bucket(auth, config_oss2['Endpoint'], config_oss2['BucketName'], connect_timeout=30)

bucket_info = bucket.get_bucket_info()
bucket.put_object_from_file(path,path)
