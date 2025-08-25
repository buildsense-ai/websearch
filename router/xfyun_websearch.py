from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx
import json
from typing import Optional

router = APIRouter(
    prefix="/xfyun",
    tags=["xfyun_websearch"]
)


class WebSearchRequest(BaseModel):
    sso_session_id: str
    jsession_id: str
    account_id: str
    query: str
    bot_id: Optional[str] = "3061845"
    work_flow_id: Optional[str] = "185607"


@router.post("/websearch", description="Websearch")
async def xfyun_websearch(request: WebSearchRequest):
    """
    讯飞Web搜索API
    
    Args:
        request: 包含搜索参数和认证信息的请求体
    
    Returns:
        搜索结果
    """
    url = "https://agent.xfyun.cn/xingchen-api/tool/debugTool"
    
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Host": "agent.xfyun.cn",
        "Lang-Code": "zh",
        "Origin": "https://agent.xfyun.cn",
        "Referer": "https://agent.xfyun.cn/work_flow/185607/arrange?botId=3061845",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": '"Not;A=Brand";v="99", "Microsoft Edge";v="139", "Chromium";v="139"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "space-id": "",
        "web-v": "0.0.0"
    }
    
    # 构建Cookie字符串
    cookie_parts = [
        f"JSESSIONID={request.jsession_id}",
        f"account_id={request.account_id}",
        f"ssoSessionId={request.sso_session_id}"
    ]
    headers["Cookie"] = "; ".join(cookie_parts)
    
    # 构建请求体 - 根据实际API要求调整
    data_payload = {
        "id": 1668,
        "name": "聚合搜索",
        "description": "使用网络搜索公开信息",
        "authType": 1,
        "query": request.query,
        "botId": request.bot_id,
        "workFlowId": request.work_flow_id
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url, 
                headers=headers, 
                json=data_payload,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
            
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"讯飞API请求失败: {e.response.text}"
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=500,
            detail=f"网络请求错误: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"未知错误: {str(e)}"
        )

