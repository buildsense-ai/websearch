from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx
import json
import os
from typing import Optional, List, Dict, Any

router = APIRouter(
    prefix="/xfyun",
    tags=["websearch"]
)


class WebSearchRequest(BaseModel):
    sso_session_id: str
    jsession_id: str
    account_id: str
    query: str
    bot_id: Optional[str] = "3061845"
    work_flow_id: Optional[str] = "185607"



@router.post("/websearch", description="Websearch")
async def call_xfyun_debug_tool(search_keyword: str, limit: int = 3):
    """
    调用讯飞星火调试工具API - 封装curl命令
    
    Args:
        search_keyword: 搜索关键词
        limit: 返回网页数量，默认为3
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
        "webSchema": f'{{"toolRequestInput":[{{"default":{limit},"description":"返回网页数量","from":0,"id":"1a09969a-6736-4e35-8a81-c2cbe969494a","location":"body","name":"limit","open":true,"required":true,"type":"integer","defaultErrMsg":""}},{{"default":"{search_keyword}","description":"检索关键词","from":0,"id":"45a394ec-80fb-4a39-b000-24283046a7cf","location":"body","name":"name","open":true,"required":true,"type":"string","defaultErrMsg":""}},{{"default":"","description":"结果是否重排序","from":0,"id":"7e290057-f80d-41c2-8fc5-c376fb2ba70d","location":"body","name":"open_rerank","open":true,"required":true,"type":"boolean","defaultErrMsg":""}},{{"default":"","description":"是否开启全文内容","from":0,"id":"49304cac-84a1-4e03-99df-3170baac7a24","location":"body","name":"full_text","open":true,"required":true,"type":"boolean","defaultErrMsg":""}}],"toolRequestOutput":[{{"children":[{{"children":[{{"description":"分类","fatherType":"array","id":"72235f54-dc88-45ba-9577-37d0d0ad32dc","name":"[Array Item]","open":true,"type":"string"}}],"description":"分类名称","fatherType":"object","id":"427ce060-eecd-4d55-a9e1-0d22100d7232","name":"classify_domain","open":true,"type":"array"}},{{"children":[{{"children":[],"description":"网页","fatherType":"array","id":"62863b10-87e9-4b36-b6e6-7ace771ba7a0","name":"[Array Item]","open":true,"type":"object"}}],"description":"网页列表","fatherType":"object","id":"08f765bd-d032-47b1-bb5e-c226b51f0835","name":"documents","open":true,"type":"array"}},{{"children":[{{"children":[],"description":"网页","fatherType":"array","id":"ff1d545a-fdbf-46fe-b1ce-584f13429f31","name":"[Array Item]","open":true,"type":"object"}}],"description":"更多网页","fatherType":"object","id":"ed39ac18-ef4b-419c-b1d1-6377ec5ecb1f","name":"more_documents","open":true,"type":"array"}}],"description":"搜索结果","id":"43c042f9-796e-4430-b2f4-0983d86eb194","name":"data","open":true,"type":"object"}},{{"description":"是否成功","id":"34ef9814-1146-4957-ad86-d33c6f0e59ea","name":"success","open":true,"type":"boolean"}},{{"description":"状态码","id":"2850b64f-db79-4acc-a956-ef0bd38ca042","name":"err_code","open":true,"type":"string"}}]}}'
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


@router.post("/baidu-search", description="百度AI搜索")
async def baidu_search(
    content: str,  # 搜索内容，用户输入的查询关键词或问题
    search_source: str = "baidu_search_v2",  # 搜索源，指定使用的搜索引擎版本
    resource_type_filter: Optional[List[Dict[str, Any]]] = None,  # 资源类型过滤器，控制搜索结果类型和数量
    search_filter: Optional[Dict[str, Any]] = None,  # 搜索过滤器，用于精确控制搜索条件
    search_recency_filter: str = "year"  # 时间过滤器，控制搜索结果的时间范围（year/month/week/day）
):
    """
    调用百度AI搜索API
    
    Args:
        content: 搜索内容，用户输入的查询关键词或问题
        search_source: 搜索源，指定使用的搜索引擎版本，默认为baidu_search_v2
        resource_type_filter: 资源类型过滤器，控制搜索结果类型和数量，默认为网页搜索前10条
        search_filter: 搜索过滤器，用于精确控制搜索条件，可选参数
        search_recency_filter: 时间过滤器，控制搜索结果的时间范围，默认为一年内
         "resource_type_filter": [{"type": "web","top_k": 10}],
  "search_filter": {
    "match": {
      "site": [
        "www.weather.com.cn"
      ]
    }
    """
    # 从环境变量获取API Key
    api_key = os.getenv("BAIDU_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="未找到百度API Key，请在环境变量中设置BAIDU_API_KEY"
        )
    
    url = "https://qianfan.baidubce.com/v2/ai_search/chat/completions"
    
    headers = {
        "X-Appbuilder-Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # 设置默认的资源类型过滤器
    if resource_type_filter is None:
        resource_type_filter = [{"type": "web", "top_k": 10}]
    
    data = {
        "messages": [
            {
                "content": content,
                "role": "user"
            }
        ],
        "search_source": search_source,
        "resource_type_filter": resource_type_filter,
        "search_recency_filter": search_recency_filter
    }
    
    # 如果提供了搜索过滤器，则添加到请求中
    if search_filter:
        data["search_filter"] = search_filter
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"百度API请求失败: {e.response.status_code} - {e.response.text}"
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