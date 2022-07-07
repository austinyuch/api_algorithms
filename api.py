import asyncio
import os
from fastapi import FastAPI, Header, Request, Form, Cookie
from fastapi import Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
import confs as cfg

import loggingsys


log = loggingsys.generate_general_my_log(log_name=__name__,
                                        log_level=cfg.GLOBAL_LOG_LEVEL,
                                        interval="d")


import algo_pyramid

app = FastAPI()
origins = cfg.lst_origins
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def read_api_root():    
    return cfg.dic_api

@app.get("/api/pyramidArithmetic")
def get_pyramid_arithmetic(
                    fltBudget:float,
                    fltPriceInit:float, 
                    fltPriceFinal:float, 
                    intTransactionTimes:int, 
                    fltIncrementAmountMinimum:float, 
                    fltOrderAmountArithmeticParam:float, 
                    fltOrderAmountInit:float=1.0
                )->dict:    
    """
    等差金字塔
    :param fltBudget:下單總預算
    :param fltPriceInit:起始價格
    :param fltPriceFinal:終止價格
    :param intTransactionTimes:交易次數
    :param fltIncrementAmountMinimum:最小增量
    :param fltOrderAmountArithmeticParam:等差增量算式參數, e.g. 1
    :param fltOrderAmountInit=1.0:起始單位數
    :return:
    """
    try:
        dic_ret = algo_pyramid.get買入等差金字塔(fltBudget,
                                        fltPriceInit, 
                                        fltPriceFinal, 
                                        intTransactionTimes, 
                                        fltIncrementAmountMinimum, 
                                        fltOrderAmountArithmeticParam, 
                                        flt_起始單位數=fltOrderAmountInit)
        return dic_ret
    except Exception as e:
        log.error(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)

@app.get("/api/pyramidGeometric")
def get_pyramid_geometric(
                    fltBudget:float,
                    fltPriceInit:float, 
                    fltPriceFinal:float, 
                    intTransactionTimes:int, 
                    fltIncrementAmountMinimum:float, 
                    fltOrderAmountGeometicParam:float, 
                    fltOrderAmountInit:float=1.0
                )->dict:    
    """
    等比金字塔
    :param fltBudget:下單總預算
    :param fltPriceInit:起始價格
    :param fltPriceFinal:終止價格
    :param intTransactionTimes:交易次數
    :param fltIncrementAmountMinimum:最小增量
    :param fltOrderAmountGeometicParam:等比增量算式參數, e.g. 2倍
    :param fltOrderAmountInit=1.0:起始單位數
    :return:
    """
    try:
        dic_ret = algo_pyramid.get買入等比金字塔(fltBudget,
                                        fltPriceInit, 
                                        fltPriceFinal, 
                                        intTransactionTimes, 
                                        fltIncrementAmountMinimum, 
                                        fltOrderAmountGeometicParam, 
                                        flt_起始單位數=fltOrderAmountInit)
        return dic_ret 

    except Exception as e:
        log.error(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)
