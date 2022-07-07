import copy
import math


交易方法 = {
    "1":"等差",
    "2":"等比",
}

# 下單價格, 下單數量

def get單位價格差(flt_起始價格:float,
                flt最終價格:float,
                int_交易次數:int)->float:
    flt總價格差 = flt_起始價格 - flt最終價格
    print(f'{flt總價格差=}')
    flt_單位價格差 = abs(flt總價格差) / (int_交易次數 - 1)
    print(f'{flt_單位價格差=}')
    return flt_單位價格差

def getLst買入價格(flt_起始價格:float,
                flt_單位價格差:float,
                int_交易次數:int)->list:
    # 計算買入價格
    lst_買入價格=[]
    for i in range(int_交易次數 - 1):
        flt買入價格 = flt_起始價格 - (flt_單位價格差 * i)
        lst_買入價格.append(flt買入價格)

    print(f'{lst_買入價格=}')
    return lst_買入價格


def etl_percentage(dic_金字塔下單資料:dict,flt_一組金字塔的加總金額:float)->dict:
    
    dic_金字塔下單資料_ret = copy.deepcopy(dic_金字塔下單資料)
    dic_金字塔下單資料_ret["總金額"] = flt_一組金字塔的加總金額
    for key,value in dic_金字塔下單資料.items():        
        dic_金字塔下單資料_ret[key]["百分比"]= (dic_金字塔下單資料_ret[key]["金額"]/dic_金字塔下單資料_ret["總金額"])*100

    return dic_金字塔下單資料_ret


def get本階下單資料(lst_買入價格, flt_最小增加數量, round單位數, i, flt_本階單位數):
    dic_本階下單資料={} 
    if round單位數:
        if flt_本階單位數 < flt_最小增加數量:
            flt_本階單位數 = flt_最小增加數量        
        flt_本階單位數 = round(flt_本階單位數,-int(math.log10(flt_最小增加數量)))

    flt_本階下單金額 = lst_買入價格[i] *  flt_本階單位數        
        
    dic_本階下單資料 = {
            "價格":lst_買入價格[i],
            "單位數":flt_本階單位數,
            "金額":flt_本階下單金額,
        }
    
    return dic_本階下單資料

#====等差金字塔====

def get一組等差金字塔下單資料(int_交易次數:int, 
                            flt_下單數量等差參數:float, 
                            flt_起始單位數:float, 
                            lst_買入價格:list,
                            flt_最小增加數量:float,
                            flt_金字塔放大倍數:float=1.0,
                            round單位數:bool=False)->dict:
    flt_一組金字塔的加總金額 = 0
    dic_單位等差金字塔下單資料 ={}
    for i in range(int_交易次數 - 1):
        
        # 本階金額 = 本階買入價格 * 本階單位數  
        flt_本階單位數 = (flt_起始單位數 + (flt_下單數量等差參數 * i) ) * flt_金字塔放大倍數
       
        dic_本階下單資料 = get本階下單資料(lst_買入價格, flt_最小增加數量, round單位數, i, flt_本階單位數)

        階層數 = str(i + 1)
        dic_單位等差金字塔下單資料[階層數] = dic_本階下單資料
        flt_一組金字塔的加總金額 += dic_本階下單資料["金額"]
    
    # 處理各階層佔比    
    dic_單位等差金字塔下單資料 = etl_percentage(dic_單位等差金字塔下單資料,flt_一組金字塔的加總金額)

    print(f'{dic_單位等差金字塔下單資料=}')

    return dic_單位等差金字塔下單資料



def get買入等差金字塔(flt_總預算:float,
                    flt_起始價格:float, 
                    flt最終價格:float, 
                    int_交易次數:int, 
                    flt_最小增加數量:float, 
                    flt_下單數量等差參數:float, 
                    flt_起始單位數:float=1.0)->dict:    

    flt_單位價格差 = get單位價格差(flt_起始價格,flt最終價格,int_交易次數)
    
    lst_買入價格 = getLst買入價格(flt_起始價格,flt_單位價格差,int_交易次數)
    
    dic_單位等差金字塔下單資料 = get一組等差金字塔下單資料(int_交易次數, flt_下單數量等差參數, flt_起始單位數, lst_買入價格,flt_最小增加數量)

    flt_金字塔放大倍數 = flt_總預算 / dic_單位等差金字塔下單資料["總金額"] 

    dic_等差金字塔下單資料 = get一組等差金字塔下單資料(int_交易次數, 
                                                flt_下單數量等差參數, 
                                                flt_起始單位數, 
                                                lst_買入價格,
                                                flt_最小增加數量,
                                                flt_金字塔放大倍數=flt_金字塔放大倍數,
                                                round單位數=True)

    
    return dic_等差金字塔下單資料

#====等比金字塔====


def get一組等比金字塔下單資料(int_交易次數:int, 
                            flt_下單數量等比參數:float, 
                            flt_起始單位數:float, 
                            lst_買入價格:list,
                            flt_最小增加數量:float,
                            flt_金字塔放大倍數:float=1.0,
                            round單位數:bool=False)->dict:
    flt_一組金字塔的加總金額 = 0
    dic_單位等比金字塔下單資料 ={}
    for i in range(int_交易次數 - 1):
        
        # 本階金額 = 本階買入價格 * 本階單位數  
        flt_本階單位數 = (flt_起始單位數 * (flt_下單數量等比參數 ** i) ) * flt_金字塔放大倍數
        
        dic_本階下單資料 = get本階下單資料(lst_買入價格, flt_最小增加數量, round單位數, i, flt_本階單位數)

        階層數 = str(i + 1)  
        dic_單位等比金字塔下單資料[階層數] = dic_本階下單資料            
        flt_一組金字塔的加總金額 += dic_本階下單資料["金額"]
    # 處理各階層佔比
    
    
    dic_單位等比金字塔下單資料= etl_percentage(dic_單位等比金字塔下單資料,flt_一組金字塔的加總金額)

    print(f'{dic_單位等比金字塔下單資料=}')

    return dic_單位等比金字塔下單資料


def get買入等比金字塔(flt_總預算:float,
                    flt_起始價格:float, 
                    flt最終價格:float, 
                    int_交易次數:int, 
                    flt_最小增加數量:float, 
                    flt_下單數量等比參數:float, 
                    flt_起始單位數:float=1.0)->dict:    

    flt_單位價格差 = get單位價格差(flt_起始價格,flt最終價格,int_交易次數)
    
    lst_買入價格 = getLst買入價格(flt_起始價格,flt_單位價格差,int_交易次數)
    
    dic_單位等比金字塔下單資料 = get一組等比金字塔下單資料(int_交易次數, flt_下單數量等比參數, flt_起始單位數, lst_買入價格,flt_最小增加數量)

    flt_金字塔放大倍數 = flt_總預算 / dic_單位等比金字塔下單資料["總金額"] 

    dic_等比金字塔下單資料 = get一組等比金字塔下單資料(int_交易次數, 
                                                flt_下單數量等比參數, 
                                                flt_起始單位數, 
                                                lst_買入價格,
                                                flt_最小增加數量,
                                                flt_金字塔放大倍數=flt_金字塔放大倍數,
                                                round單位數=True)

    
    return dic_等比金字塔下單資料

if __name__ == "__main__":

    flt_總預算 = float(100000) #float(input("請輸入總預算："))
    flt_起始價格 = float(440) #float(input("請輸入起始金額："))
    flt最終價格 = float(380) #float(input("請輸入最終金額："))
    flt_最小增加數量 = float(1) #float(input("請輸入最小增加單位："))
    flt_下單數量等差參數 = float(1) #float(input("請輸入下單數量等差參數：")) #前一階單位數 + 本接單位數 = 此階單位數  
    flt_下單數量等比參數 = float(1.5) # float(input("請輸入下單數量等比參數：")) ＃前一階單位數*等比參數 = 此階單位數
    int_交易次數 = int(6) # int(input("請輸入交易次數："))
    dic_等差金字塔下單資料 = get買入等差金字塔(flt_總預算,flt_起始價格, flt最終價格, int_交易次數, flt_最小增加數量, flt_下單數量等差參數, flt_起始單位數=1)
    dic_等比金字塔下單資料 = get買入等比金字塔(flt_總預算,flt_起始價格, flt最終價格, int_交易次數, flt_最小增加數量, flt_下單數量等比參數, flt_起始單位數=1)

