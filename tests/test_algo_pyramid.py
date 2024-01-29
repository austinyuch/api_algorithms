import sys
import pytest
from pathlib import Path

PATH_SRC = Path(__file__).resolve().parents[1]
if str(PATH_SRC) not in sys.path:
    sys.path.append(str(PATH_SRC))
from invest_algorithms.algo_pyramid import (
    get單位價格差,
    getLst買入價格,
    get本階投入資金百分比,
    get累計下跌百分比,
    etl_percentage,
    get本階下單資料,
    get一組等差金字塔下單資料,
    get買入等差金字塔,
    get一組等比金字塔下單資料,
    get買入等比金字塔,
)


@pytest.mark.parametrize(
    "flt_起始價格, flt最終價格, int_交易次數, expected",
    [
        (100.0, 50.0, 10, 5.0),
        (200.0, 100.0, 20, 5.0),
        (300.0, 200.0, 10, 10.0),
        (400.0, 300.0, 20, 5.0),
    ],
)
def test_get單位價格差(flt_起始價格, flt最終價格, int_交易次數, expected):
    assert get單位價格差(flt_起始價格, flt最終價格, int_交易次數) == expected


@pytest.mark.parametrize(
    "flt_起始價格, flt_單位價格差, int_交易次數, expected",
    [
        (100.0, 5.0, 10, [95.0, 90.0, 85.0, 80.0, 75.0, 70.0, 65.0, 60.0, 55.0, 50.0]),
        (200.0, 10.0, 5, [190.0, 180.0, 170.0, 160.0, 150.0]),
        (300.0, 15.0, 3, [285.0, 270.0, 255.0]),
        (400.0, 20.0, 2, [380.0, 360.0]),
    ],
)
def test_getLst買入價格(flt_起始價格, flt_單位價格差, int_交易次數, expected):
    assert getLst買入價格(flt_起始價格, flt_單位價格差, int_交易次數) == expected


@pytest.mark.parametrize(
    "flt_一組金字塔的加總金額, flt_下單金額, expected",
    [
        (1000.0, 100.0, 10.0),
        (2000.0, 400.0, 20.0),
        (3000.0, 600.0, 20.0),
        (4000.0, 800.0, 20.0),
    ],
)
def test_get本階投入資金百分比(flt_一組金字塔的加總金額, flt_下單金額, expected):
    assert get本階投入資金百分比(flt_一組金字塔的加總金額, flt_下單金額) == expected


@pytest.mark.parametrize(
    "flt_起始價格, flt_當前價格, expected",
    [
        (100.0, 90.0, 10.0),
        (200.0, 180.0, 10.0),
        (300.0, 270.0, 10.0),
        (400.0, 360.0, 10.0),
    ],
)
def test_get累計下跌百分比(flt_起始價格, flt_當前價格, expected):
    assert get累計下跌百分比(flt_起始價格, flt_當前價格) == expected


@pytest.mark.parametrize(
    "dic_金字塔下單資料, flt_一組金字塔的加總金額, flt_起始價格, expected",
    [
        (
            {
                "各階資料": [
                    {"當次投資金額": 100.0, "價格": 90.0, "單位數": 1.0},
                    {"當次投資金額": 200.0, "價格": 80.0, "單位數": 2.0},
                ]
            },
            300.0,
            100.0,
            {
                "各階資料": [
                    {
                        "當次投資金額": 100.0,
                        "價格": 90.0,
                        "單位數": 1.0,
                        "投入百分比": 33.33,
                        "累計投入百分比": 33.33,
                        "累計投資金額": 100.0,
                        "股價跌幅(%)": 10.0,
                    },
                    {
                        "當次投資金額": 200.0,
                        "價格": 80.0,
                        "單位數": 2.0,
                        "投入百分比": 66.67,
                        "累計投入百分比": 100.0,
                        "累計投資金額": 300.0,
                        "股價跌幅(%)": 20.0,
                    },
                ],
                "起始價格": 100.0,
                "最終價格": 80.0,
                "股價跌幅(%)": 20.0,
                "總投入金額": 300.0,
                "累計數量": 3.0,
                "平均成本": 100.0,
            },
        ),
    ],
)
def test_etl_percentage(
    dic_金字塔下單資料, flt_一組金字塔的加總金額, flt_起始價格, expected
):
    assert (
        etl_percentage(dic_金字塔下單資料, flt_一組金字塔的加總金額, flt_起始價格)
        == expected
    )


@pytest.mark.parametrize(
    "lst_買入價格, flt_最小增加數量, round單位數, i, flt_本階單位數, expected",
    [
        (
            [100.0, 90.0, 80.0],
            1.0,
            True,
            0,
            1.0,
            {"階": 1, "價格": 100.0, "單位數": 1.0, "當次投資金額": 100.0},
        ),
        (
            [100.0, 90.0, 80.0],
            1.0,
            True,
            1,
            2.0,
            {"階": 2, "價格": 90.0, "單位數": 2.0, "當次投資金額": 180.0},
        ),
        (
            [100.0, 90.0, 80.0],
            1.0,
            True,
            2,
            3.0,
            {"階": 3, "價格": 80.0, "單位數": 3.0, "當次投資金額": 240.0},
        ),
    ],
)
def test_get本階下單資料(
    lst_買入價格, flt_最小增加數量, round單位數, i, flt_本階單位數, expected
):
    assert (
        get本階下單資料(lst_買入價格, flt_最小增加數量, round單位數, i, flt_本階單位數)
        == expected
    )


# ====等差金字塔====


def get一組等差金字塔下單資料(
    flt_起始價格: float,
    int_交易次數: int,
    flt_下單數量等差參數: float,
    flt_起始單位數: float,
    lst_買入價格: list,
    flt_最小增加數量: float,
    flt_金字塔放大倍數: float = 1.0,
    round單位數: bool = False,
) -> dict:
    flt_一組金字塔的加總金額 = 0
    dic_單位等差金字塔下單資料 = {}
    lst_results = []
    for i in range(int_交易次數):
        # 本階金額 = 本階買入價格 * 本階單位數
        flt_本階單位數 = (
            flt_起始單位數 + (flt_下單數量等差參數 * i)
        ) * flt_金字塔放大倍數

        dic_本階下單資料 = get本階下單資料(
            lst_買入價格, flt_最小增加數量, round單位數, i, flt_本階單位數
        )

        # 階層數 = str(i + 1)
        # dic_單位等差金字塔下單資料[階層數] = dic_本階下單資料
        lst_results.append(dic_本階下單資料)
        flt_一組金字塔的加總金額 += dic_本階下單資料["當次投資金額"]

    # 處理各階層佔比
    dic_單位等差金字塔下單資料["各階資料"] = lst_results
    dic_單位等差金字塔下單資料 = etl_percentage(
        dic_單位等差金字塔下單資料, flt_一組金字塔的加總金額, flt_起始價格
    )

    print(f"{dic_單位等差金字塔下單資料=}")

    return dic_單位等差金字塔下單資料


@pytest.mark.parametrize(
    "flt_總預算, flt_起始價格, flt最終價格, int_交易次數, flt_最小增加數量, flt_下單數量等差參數, flt_起始單位數, expected",
    [
        (
            1000.0,
            100.0,
            80.0,
            3,
            1.0,
            1.0,
            1.0,
            {
                "各階資料": [
                    {
                        "階": 1,
                        "價格": 93.33333333333333,
                        "單位數": 2.0,
                        "當次投資金額": 186.66666666666666,
                        "投入百分比": 18.42,
                        "累計投入百分比": 18.42,
                        "累計投資金額": 186.67,
                        "股價跌幅(%)": 6.67,
                    },
                    {
                        "階": 2,
                        "價格": 86.66666666666667,
                        "單位數": 4.0,
                        "當次投資金額": 346.6666666666667,
                        "投入百分比": 34.21,
                        "累計投入百分比": 52.63,
                        "累計投資金額": 533.33,
                        "股價跌幅(%)": 13.33,
                    },
                    {
                        "階": 3,
                        "價格": 80.0,
                        "單位數": 6.0,
                        "當次投資金額": 480.0,
                        "投入百分比": 47.37,
                        "累計投入百分比": 100.0,
                        "累計投資金額": 1013.33,
                        "股價跌幅(%)": 20.0,
                    },
                ],
                "起始價格": 100.0,
                "最終價格": 80.0,
                "股價跌幅(%)": 20.0,
                "總投入金額": 1013.3333333333334,
                "累計數量": 12.0,
                "平均成本": 84.44,
            },
        ),
    ],
)
def test_get買入等差金字塔(
    flt_總預算,
    flt_起始價格,
    flt最終價格,
    int_交易次數,
    flt_最小增加數量,
    flt_下單數量等差參數,
    flt_起始單位數,
    expected,
):
    dic_result = get買入等差金字塔(
        flt_總預算,
        flt_起始價格,
        flt最終價格,
        int_交易次數,
        flt_最小增加數量,
        flt_下單數量等差參數,
        flt_起始單位數,
    )
    assert dic_result == expected


# ====等比金字塔====


@pytest.mark.parametrize(
    "flt_起始價格, int_交易次數, flt_下單數量等比參數, flt_起始單位數, lst_買入價格, flt_最小增加數量, flt_金字塔放大倍數, round單位數, expected",
    [
        (
            100.0,
            3,
            1.0,
            1.0,
            [100.0, 90.0, 80.0],
            1.0,
            1.0,
            False,
            {
                "各階資料": [
                    {
                        "階": 1,
                        "價格": 100.0,
                        "單位數": 1.0,
                        "當次投資金額": 100.0,
                        "投入百分比": 37.04,
                        "累計投入百分比": 37.04,
                        "累計投資金額": 100.0,
                        "股價跌幅(%)": 0.0,
                    },
                    {
                        "階": 2,
                        "價格": 90.0,
                        "單位數": 1.0,
                        "當次投資金額": 90.0,
                        "投入百分比": 33.33,
                        "累計投入百分比": 70.37,
                        "累計投資金額": 190.0,
                        "股價跌幅(%)": 10.0,
                    },
                    {
                        "階": 3,
                        "價格": 80.0,
                        "單位數": 1.0,
                        "當次投資金額": 80.0,
                        "投入百分比": 29.63,
                        "累計投入百分比": 100.0,
                        "累計投資金額": 270.0,
                        "股價跌幅(%)": 20.0,
                    },
                ],
                "起始價格": 100.0,
                "最終價格": 80.0,
                "股價跌幅(%)": 20.0,
                "總投入金額": 270.0,
                "累計數量": 3.0,
                "平均成本": 90.0,
            },
        ),
    ],
)
def test_get一組等比金字塔下單資料(
    flt_起始價格,
    int_交易次數,
    flt_下單數量等比參數,
    flt_起始單位數,
    lst_買入價格,
    flt_最小增加數量,
    flt_金字塔放大倍數,
    round單位數,
    expected,
):
    dic_result = get一組等比金字塔下單資料(
        flt_起始價格,
        int_交易次數,
        flt_下單數量等比參數,
        flt_起始單位數,
        lst_買入價格,
        flt_最小增加數量,
        flt_金字塔放大倍數,
        round單位數,
    )
    assert dic_result == expected


@pytest.mark.parametrize(
    "flt_總預算, flt_起始價格, flt最終價格, int_交易次數, flt_最小增加數量, flt_下單數量等比參數, flt_起始單位數, expected",
    [
        (
            10000.0,
            100.0,
            80.0,
            4,
            1.0,
            2.0,
            1.0,
            {
                "各階資料": [
                    {
                        "階": 1,
                        "價格": 95.0,
                        "單位數": 8.0,
                        "當次投資金額": 760.0,
                        "投入百分比": 7.57,
                        "累計投入百分比": 7.57,
                        "累計投資金額": 760.0,
                        "股價跌幅(%)": 5.0,
                    },
                    {
                        "階": 2,
                        "價格": 90.0,
                        "單位數": 16.0,
                        "當次投資金額": 1440.0,
                        "投入百分比": 14.34,
                        "累計投入百分比": 21.91,
                        "累計投資金額": 2200.0,
                        "股價跌幅(%)": 10.0,
                    },
                    {
                        "階": 3,
                        "價格": 85.0,
                        "單位數": 32.0,
                        "當次投資金額": 2720.0,
                        "投入百分比": 27.09,
                        "累計投入百分比": 49.0,
                        "累計投資金額": 4920.0,
                        "股價跌幅(%)": 15.0,
                    },
                    {
                        "階": 4,
                        "價格": 80.0,
                        "單位數": 64.0,
                        "當次投資金額": 5120.0,
                        "投入百分比": 51.0,
                        "累計投入百分比": 100.0,
                        "累計投資金額": 10040.0,
                        "股價跌幅(%)": 20.0,
                    },
                ],
                "起始價格": 100.0,
                "最終價格": 80.0,
                "股價跌幅(%)": 20.0,
                "總投入金額": 10040.0,
                "累計數量": 120.0,
                "平均成本": 83.67,
            },
        ),
        (
            1000.0,
            100.0,
            80.0,
            3,
            1.0,
            1.0,
            1.0,
            {
                "各階資料": [
                    {
                        "階": 1,
                        "價格": 93.33333333333333,
                        "單位數": 4.0,
                        "當次投資金額": 373.3333333333333,
                        "投入百分比": 35.9,
                        "累計投入百分比": 35.9,
                        "累計投資金額": 373.33,
                        "股價跌幅(%)": 6.67,
                    },
                    {
                        "階": 2,
                        "價格": 86.66666666666667,
                        "單位數": 4.0,
                        "當次投資金額": 346.6666666666667,
                        "投入百分比": 33.33,
                        "累計投入百分比": 69.23,
                        "累計投資金額": 720.0,
                        "股價跌幅(%)": 13.33,
                    },
                    {
                        "階": 3,
                        "價格": 80.0,
                        "單位數": 4.0,
                        "當次投資金額": 320.0,
                        "投入百分比": 30.77,
                        "累計投入百分比": 100.0,
                        "累計投資金額": 1040.0,
                        "股價跌幅(%)": 20.0,
                    },
                ],
                "起始價格": 100.0,
                "最終價格": 80.0,
                "股價跌幅(%)": 20.0,
                "總投入金額": 1040.0,
                "累計數量": 12.0,
                "平均成本": 86.67,
            },
        ),
    ],
)
def test_get買入等比金字塔(
    flt_總預算,
    flt_起始價格,
    flt最終價格,
    int_交易次數,
    flt_最小增加數量,
    flt_下單數量等比參數,
    flt_起始單位數,
    expected,
):
    dic_result = get買入等比金字塔(
        flt_總預算,
        flt_起始價格,
        flt最終價格,
        int_交易次數,
        flt_最小增加數量,
        flt_下單數量等比參數,
        flt_起始單位數,
    )
    assert dic_result == expected


if __name__ == "__main__":
    pytest.main([__file__])
