import json, requests
import settings


def send_to_wecom(text, wecom_cid, wecom_aid, wecom_secret, wecom_touid="@all"):
    get_token_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={wecom_cid}&corpsecret={wecom_secret}"
    response = requests.get(get_token_url).content
    access_token = json.loads(response).get("access_token")
    if access_token and len(access_token) > 0:
        send_msg_url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}"
        data = {
            "touser": wecom_touid,
            "agentid": wecom_aid,
            "msgtype": "text",
            "text": {"content": text},
            "duplicate_check_interval": 600,
        }
        response = requests.post(send_msg_url, data=json.dumps(data)).content
        return response
    else:
        return False


def send_notify(text, ID):
    send_to_wecom(
        text, settings.WECOM_CID, settings.WECOM_AID, settings.WECOM_SECRET, ID
    )
