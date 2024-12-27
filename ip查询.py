import requests


def get_ip_info(ip_address, lang='zh-CN'):
    # 使用 ipapi.co 的 IP 查询 API，并指定返回中文结果
    url = f"https://ipapi.co/{ip_address}/json/"
    headers = {'Accept-Language': lang}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
        ip_info = response.json()

        return ip_info
    except requests.RequestException as e:
        print(f"请求失败: {e}")
        return None


def main():
    # 示例 IP 地址
    ip_address = "60.190.231.242"

    # 获取 IP 信息（中文）
    ip_info = get_ip_info(ip_address, lang='zh-CN')

    if ip_info:
        print(f"IP 地址: {ip_info.get('ip', '未知')}")
        print(
            f"所在地理位置: {ip_info.get('city', '未知')}, {ip_info.get('region', '未知')}, {ip_info.get('country_name', '未知')}")
        print(f"组织: {ip_info.get('organization', '未知')}")
        print(f"邮政编码: {ip_info.get('postal', '未知')}")
        print(f"时区: {ip_info.get('timezone', '未知')}")


if __name__ == "__main__":
    main()
