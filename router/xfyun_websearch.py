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
    
    # 构建完整的Cookie字符串 - 包含所有必要的认证和跟踪信息
    cookie_parts = [
        f"JSESSIONID={request.jsession_id}",
        f"account_id={request.account_id}",
        "di_c_mti=cfd4fd05-063c-6f6f-954c-442c5b6c7c8c",
        f"ui={request.account_id}",
        "d_d_app_ver=1.4.0",
        "d_d_ci=a3206419-51d8-6301-9dd5-2cd2304f27ab",
        "gr_user_id=cfa6e9e3-5f09-4eac-b1a4-8b6481130711",
        "_gcl_au=1.1.1295090135.1753774963",
        f"ssoSessionId={request.sso_session_id}",
        "Hm_lvt_83a57cc9e205b0add91afc6c4f0babcc=1753774962,1755069261,1755136197",
        "gt_local_id=0NP9sVJhr/u7OaEIkAG6334HGnhdKaQrThWLrDIbC0vd2a1UuNMIwA==",
        "Hm_lvt_fe740601c79b0c00b6d5458d146aa5ef=1755136198,1755220772,1755502448,1756102315",
        "Hm_lpvt_fe740601c79b0c00b6d5458d146aa5ef=1756102315",
        "HMACCOUNT=6710B071C556072B",
        "_ga_0KHV9JM0VW=GS2.1.s1756102314$o6$g0$t1756102314$j60$l0$h0",
        "_ga=GA1.2.970447496.1755069263",
        "_gid=GA1.2.439796559.1756102315",
        "_uetsid=663dd090817a11f0a8b36d7a1e92ad1c",
        "_uetvid=3e1aa9b06c4d11f0b6d015b345bc54c7",
        "_clck=1qdwafl%5E2%5Efyr%5E0%5E2036",
        "_clsk=12pezrk%5E1756111658518%5E5%5E1%5Ey.clarity.ms%2Fcollect",
        "daas_st={%22sdk_ver%22:%221.3.9%22%2C%22status%22:%220%22}",
        "appid=150b4dfebe"
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


@router.post("/debug-tool", description="调用讯飞星火调试工具API")
async def call_xfyun_debug_tool(search_keyword: str):
    """
    调用讯飞星火调试工具API - 封装curl命令
    
    Args:
        search_keyword: 搜索关键词，默认为"长沙理工"
    """
    url = "https://agent.xfyun.cn/xingchen-api/tool/debugTool"
    
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Cookie": "JSESSIONID=DTTdhbcluvqnJemyutsMXLaIJyqZXgfHt-jGTUMv; account_id=20580254926; di_c_mti=cfd4fd05-063c-6f6f-954c-442c5b6c7c8c; ui=20580254926; d_d_app_ver=1.4.0; d_d_ci=a3206419-51d8-6301-9dd5-2cd2304f27ab; gr_user_id=cfa6e9e3-5f09-4eac-b1a4-8b6481130711; _gcl_au=1.1.1295090135.1753774963; ssoSessionId=c2f41eb7-cef2-4e01-92ee-9c3b23eb18ef; Hm_lvt_83a57cc9e205b0add91afc6c4f0babcc=1753774962,1755069261,1755136197; gt_local_id=0NP9sVJhr/u7OaEIkAG6334HGnhdKaQrThWLrDIbC0vd2a1UuNMIwA==; Hm_lvt_fe740601c79b0c00b6d5458d146aa5ef=1755136198,1755220772,1755502448,1756102315; Hm_lpvt_fe740601c79b0c00b6d5458d146aa5ef=1756102315; HMACCOUNT=6710B071C556072B; _ga_0KHV9JM0VW=GS2.1.s1756102314$o6$g0$t1756102314$j60$l0$h0; _ga=GA1.2.970447496.1755069263; _gid=GA1.2.439796559.1756102315; _uetsid=663dd090817a11f0a8b36d7a1e92ad1c; _uetvid=3e1aa9b06c4d11f0b6d015b345bc54c7; _clck=1qdwafl%5E2%5Efyr%5E0%5E2036; _clsk=12pezrk%5E1756111658518%5E5%5E1%5Ey.clarity.ms%2Fcollect; daas_st={%22sdk_ver%22:%221.3.9%22%2C%22status%22:%220%22}; appid=150b4dfebe",
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
    
    data = {
        "id": 1668,
        "name": "聚合搜索",
        "description": "使用网络搜索公开信息",
        "endPoint": "http://dx-cbm-ocp-agg-search-inner.xf-yun.com/search",
        "authType": 1,
        "method": "post",
        "visibility": 0,
        "creationMethod": 1,
        "webSchema": f'{{"toolRequestInput":[{{"default":3,"description":"返回网页数量","from":0,"id":"1a09969a-6736-4e35-8a81-c2cbe969494a","location":"body","name":"limit","open":true,"required":true,"type":"integer","defaultErrMsg":""}},{{"default":"{search_keyword}","description":"检索关键词","from":0,"id":"45a394ec-80fb-4a39-b000-24283046a7cf","location":"body","name":"name","open":true,"required":true,"type":"string","defaultErrMsg":""}},{{"default":"","description":"结果是否重排序","from":0,"id":"7e290057-f80d-41c2-8fc5-c376fb2ba70d","location":"body","name":"open_rerank","open":true,"required":true,"type":"boolean","defaultErrMsg":""}},{{"default":"","description":"是否开启全文内容","from":0,"id":"49304cac-84a1-4e03-99df-3170baac7a24","location":"body","name":"full_text","open":true,"required":true,"type":"boolean","defaultErrMsg":""}}],"toolRequestOutput":[{{"children":[{{"children":[{{"description":"分类","fatherType":"array","id":"72235f54-dc88-45ba-9577-37d0d0ad32dc","name":"[Array Item]","open":true,"type":"string"}}],"description":"分类名称","fatherType":"object","id":"427ce060-eecd-4d55-a9e1-0d22100d7232","name":"classify_domain","open":true,"type":"array"}},{{"children":[{{"children":[],"description":"网页","fatherType":"array","id":"62863b10-87e9-4b36-b6e6-7ace771ba7a0","name":"[Array Item]","open":true,"type":"object"}}],"description":"网页列表","fatherType":"object","id":"08f765bd-d032-47b1-bb5e-c226b51f0835","name":"documents","open":true,"type":"array"}},{{"children":[{{"children":[],"description":"网页","fatherType":"array","id":"ff1d545a-fdbf-46fe-b1ce-584f13429f31","name":"[Array Item]","open":true,"type":"object"}}],"description":"更多网页","fatherType":"object","id":"ed39ac18-ef4b-419c-b1d1-6377ec5ecb1f","name":"more_documents","open":true,"type":"array"}}],"description":"搜索结果","id":"43c042f9-796e-4430-b2f4-0983d86eb194","name":"data","open":true,"type":"object"}},{{"description":"是否成功","id":"34ef9814-1146-4957-ad86-d33c6f0e59ea","name":"success","open":true,"type":"boolean"}},{{"description":"状态码","id":"2850b64f-db79-4acc-a956-ef0bd38ca042","name":"err_code","open":true,"type":"string"}}]}}'
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"HTTP错误: {e.response.status_code} - {e.response.text}"
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