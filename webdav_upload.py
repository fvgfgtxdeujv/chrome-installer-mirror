#!/usr/bin/env python3
"""
WebDAV 上传工具 - 自动检测 exe 文件
上传带版本号的文件到 WebDAV
"""

import os
import sys
import logging
import glob

try:
    from webdav3.client import Client
    from webdav3.exceptions import WebDAVException
except ImportError:
    print("❌ 错误: 请安装 webdavclient3 库")
    print("运行: pip install webdavclient3")
    sys.exit(1)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def upload_to_webdav(url, username, password, local_file, remote_file):
    """上传文件到 WebDAV 服务器"""
    if not os.path.exists(local_file):
        logger.error(f"❌ 本地文件不存在: {local_file}")
        return False
    
    if not os.path.isfile(local_file):
        logger.error(f"❌ 不是文件: {local_file}")
        return False
    
    file_size = os.path.getsize(local_file)
    file_name = os.path.basename(local_file)
    
    logger.info(f"📤 上传: {file_name} ({file_size} 字节) -> {remote_file}")
    
    try:
        options = {
            'webdav_hostname': url.rstrip('/'),
            'webdav_login': username,
            'webdav_password': password,
            'disable_ssl_certificate_validation': False,
            'timeout': 300,
        }
        
        client = Client(options)
        
        if client.check(remote_file):
            logger.warning(f"⚠️ 远程文件已存在，将覆盖: {remote_file}")
        
        client.upload_sync(
            remote_path=remote_file,
            local_path=local_file
        )
        
        if client.check(remote_file):
            info = client.info(remote_file)
            remote_size = info.get('size', 0)
            logger.info(f"✅ 上传成功: {remote_file} (远程大小: {remote_size} 字节)")
            return True
        else:
            logger.error(f"❌ 上传后文件不存在: {remote_file}")
            return False
            
    except WebDAVException as e:
        logger.error(f"❌ WebDAV 异常: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ 上传异常: {str(e)}")
        return False


def main():
    """主函数"""
    # 从环境变量读取 WebDAV 配置
    webdav_url = os.environ.get('WEBDAV_URL')
    webdav_username = os.environ.get('WEBDAV_USERNAME')
    webdav_password = os.environ.get('WEBDAV_PASSWORD')
    
    # 检查 WebDAV 配置
    if not all([webdav_url, webdav_username, webdav_password]):
        logger.error("❌ WebDAV 配置不完整")
        logger.info("请设置环境变量: WEBDAV_URL, WEBDAV_USERNAME, WEBDAV_PASSWORD")
        sys.exit(1)
    
    logger.info(f"🚀 开始上传到 WebDAV")
    logger.info(f"📡 服务器: {webdav_url}")
    
    # 查找当前目录下的 chrome_*.exe 文件
    exe_files = glob.glob('chrome_*.exe')
    
    if not exe_files:
        logger.error("❌ 未找到 chrome_*.exe 文件")
        sys.exit(1)
    
    # 取第一个找到的 exe 文件
    exe_file = exe_files[0]
    logger.info(f"✅ 找到文件: {exe_file}")
    
    # 查找对应的 sha256 文件（同名的 .sha256）
    sha256_file = exe_file + '.sha256'
    
    if not os.path.exists(sha256_file):
        logger.error(f"❌ 未找到对应的 SHA256 文件: {sha256_file}")
        sys.exit(1)
    
    # 上传文件
    files_to_upload = [
        (exe_file, exe_file),
        (sha256_file, sha256_file),
    ]
    
    success_count = 0
    total_count = len(files_to_upload)
    
    for local_path, remote_path in files_to_upload:
        logger.info(f"\n{'='*60}")
        if upload_to_webdav(webdav_url, webdav_username, webdav_password, 
                           local_path, remote_path):
            success_count += 1
    
    # 输出统计结果
    logger.info(f"\n{'='*60}")
    logger.info(f"📊 上传完成: {success_count}/{total_count} 成功")
    
    if success_count == total_count:
        logger.info("✅ 所有文件上传成功！")
        logger.info(f"📦 上传文件: {exe_file}")
        logger.info(f"🔐 校验文件: {sha256_file}")
        sys.exit(0)
    else:
        logger.error(f"❌ {total_count - success_count} 个文件上传失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
