from fastapi import FastAPI
import akshare as ak
import json
import uvicorn

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/connect")
async def connect(code: str):
    df = ak.fund_open_fund_info_em(fund=code)

    res = df.to_json(orient="records", force_ascii=False)

    return json.loads(res)


@app.get("/open")
async def open():
    df = ak.fund_open_fund_rank_em(symbol="全部")
    res = df.to_json(orient="records", force_ascii=False)

    return res


@app.get("/changnei")
async def changnei():
    df = ak.fund_exchange_rank_em()
    res = df.to_json(orient="records", force_ascii=False)

    return res


@app.get("/huobi")
async def huobi():
    df = ak.fund_money_rank_em()
    res = df.to_json(orient="records", force_ascii=False)
    return res


@app.get("/licai")
async def licai():
    df = ak.fund_lcx_rank_em()
    res = df.to_json(orient="records", force_ascii=False)

    return res

@app.get("/rili")
async def rili():
    df = ak.tool_trade_date_hist_sina()
    # print("df:", df)
    # res = df.to_json(orient="records", force_ascii=False)

    return df


@app.get("/shishi")
async def shishi(code: str):
    df = ak.fund_value_estimation_em(symbol="全部")
    res = df.to_json(orient="records", force_ascii=False)
    # s1 = json.loads(res)
    return_obj = {}
    parsed_array = json.loads(res)

    for item in parsed_array:
        if item['基金代码'] == code:
            return_obj = item
            break

    if return_obj == {}:
        df = ak.fund_value_estimation_em(symbol="场内交易基金")
        res = df.to_json(orient="records", force_ascii=False)
        parsed_array = json.loads(res)
        for item in parsed_array:
            if item['基金代码'] == code:
                return_obj = item
                break

    return return_obj


@app.get("/shishi/many")
async def shishi_many(code: str):
    df = ak.fund_value_estimation_em(symbol="全部")

    res = df.to_json(orient="records", force_ascii=False)
    return_obj = json.dumps({})
    parsed_array = json.loads(res)
    code_list = code.split(",")
    # print("code_list", code_list)
    code_dict = {}

    for item in parsed_array:
        if item['基金代码'] in code_list:
            code_dict[item['基金代码']] = item
            if len(code_dict) == len(code_list):
                break

    # print(len(code_dict), len(code_list))
    if len(code_dict) != len(code_list):
        internal = ak.fund_value_estimation_em(symbol="场内交易基金")
        internal_res = internal.to_json(orient="records", force_ascii=False)
        parsed_array = json.loads(internal_res)
        for item in parsed_array:
            if item['基金代码'] in code_list:
                code_dict[item['基金代码']] = item
                if len(code_dict) == len(code_list):
                    break

    return_list = []

    for v in code_list:
        for value in code_dict.values():
            if value['基金代码'] == v:
                return_list.append(value)

    return return_list


@app.get("/history/profit")
async def profit():
    df = ak.fund_open_fund_rank_em("全部")
    res = df.to_json(orient="records", force_ascii=False)
    parsed_array = json.loads(res)
    return parsed_array


if __name__ == '__main__':
    uvicorn.run(
        app='main:app',
        host="0.0.0.0",
        port=8083,
        workers=2,
        reload=False)
