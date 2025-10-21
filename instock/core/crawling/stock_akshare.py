#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2025/10/21
Desc: AKShare数据源接口封装
提供使用AKShare库获取股票数据的接口
"""
import pandas as pd
import logging

try:
    import akshare as ak
    AKSHARE_AVAILABLE = True
except ImportError:
    AKSHARE_AVAILABLE = False
    logging.warning("AKShare未安装，将使用备用数据源")


def stock_zh_a_spot_em_akshare() -> pd.DataFrame:
    """
    使用AKShare获取A股实时行情数据
    https://akshare.akfamily.xyz/data/stock/stock.html#id3
    :return: 实时行情
    :rtype: pandas.DataFrame
    """
    if not AKSHARE_AVAILABLE:
        return pd.DataFrame()
    
    try:
        # 使用akshare的stock_zh_a_spot_em接口
        df = ak.stock_zh_a_spot_em()
        if df is None or len(df) == 0:
            return pd.DataFrame()
        
        # 重命名列以匹配项目中的数据格式
        column_mapping = {
            '代码': '代码',
            '名称': '名称',
            '最新价': '最新价',
            '涨跌幅': '涨跌幅',
            '涨跌额': '涨跌额',
            '成交量': '成交量',
            '成交额': '成交额',
            '振幅': '振幅',
            '换手率': '换手率',
            '市盈率-动态': '市盈率动',
            '量比': '量比',
            '5分钟涨跌': '5分钟涨跌',
            '最高': '最高',
            '最低': '最低',
            '今开': '今开',
            '昨收': '昨收',
            '总市值': '总市值',
            '流通市值': '流通市值',
            '涨速': '涨速',
            '市净率': '市净率',
            '60日涨跌幅': '60日涨跌幅',
            '年初至今涨跌幅': '年初至今涨跌幅',
        }
        
        # 选择需要的列并重命名
        available_columns = [col for col in column_mapping.keys() if col in df.columns]
        df_selected = df[available_columns].copy()
        
        # 重命名列
        rename_map = {k: v for k, v in column_mapping.items() if k in available_columns}
        df_selected.rename(columns=rename_map, inplace=True)
        
        # 确保数值类型正确
        numeric_columns = ['最新价', '涨跌幅', '涨跌额', '成交量', '成交额', '振幅', 
                          '换手率', '量比', '最高', '最低', '今开', '昨收', 
                          '总市值', '流通市值', '涨速', '市净率']
        
        for col in numeric_columns:
            if col in df_selected.columns:
                df_selected[col] = pd.to_numeric(df_selected[col], errors='coerce')
        
        return df_selected
        
    except Exception as e:
        logging.error(f"stock_zh_a_spot_em_akshare处理异常：{e}")
        return pd.DataFrame()


def stock_zh_a_hist_akshare(
    symbol: str = "000001",
    period: str = "daily",
    start_date: str = "19700101",
    end_date: str = "20500101",
    adjust: str = "",
) -> pd.DataFrame:
    """
    使用AKShare获取A股历史行情数据
    https://akshare.akfamily.xyz/data/stock/stock.html#id5
    :param symbol: 股票代码
    :type symbol: str
    :param period: choice of {'daily', 'weekly', 'monthly'}
    :type period: str
    :param start_date: 开始日期
    :type start_date: str
    :param end_date: 结束日期
    :type end_date: str
    :param adjust: choice of {"qfq": "前复权", "hfq": "后复权", "": "不复权"}
    :type adjust: str
    :return: 历史行情
    :rtype: pandas.DataFrame
    """
    if not AKSHARE_AVAILABLE:
        return pd.DataFrame()
    
    try:
        # AKShare的调整参数映射
        adjust_map = {"qfq": "qfq", "hfq": "hfq", "": ""}
        period_map = {"daily": "daily", "weekly": "weekly", "monthly": "monthly"}
        
        # 使用akshare的stock_zh_a_hist接口
        df = ak.stock_zh_a_hist(
            symbol=symbol,
            period=period_map.get(period, "daily"),
            start_date=start_date,
            end_date=end_date,
            adjust=adjust_map.get(adjust, "")
        )
        
        if df is None or len(df) == 0:
            return pd.DataFrame()
        
        # 重命名列以匹配项目格式
        df.columns = [
            "日期",
            "开盘",
            "收盘",
            "最高",
            "最低",
            "成交量",
            "成交额",
            "振幅",
            "涨跌幅",
            "涨跌额",
            "换手率",
        ]
        
        # 设置日期索引
        df.index = pd.to_datetime(df["日期"])
        df.reset_index(inplace=True, drop=True)
        
        # 确保数值类型正确
        numeric_columns = ['开盘', '收盘', '最高', '最低', '成交量', '成交额', 
                          '振幅', '涨跌幅', '涨跌额', '换手率']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df
        
    except Exception as e:
        logging.error(f"stock_zh_a_hist_akshare处理异常：{symbol}代码{e}")
        return pd.DataFrame()


def fund_etf_spot_em_akshare() -> pd.DataFrame:
    """
    使用AKShare获取ETF实时行情数据
    https://akshare.akfamily.xyz/data/fund/fund.html
    :return: ETF实时行情
    :rtype: pandas.DataFrame
    """
    if not AKSHARE_AVAILABLE:
        return pd.DataFrame()
    
    try:
        # 使用akshare的fund_etf_spot_em接口
        df = ak.fund_etf_spot_em()
        
        if df is None or len(df) == 0:
            return pd.DataFrame()
        
        # 重命名列以匹配项目格式
        column_mapping = {
            '代码': '代码',
            '名称': '名称',
            '最新价': '最新价',
            '涨跌幅': '涨跌幅',
            '涨跌额': '涨跌额',
            '成交量': '成交量',
            '成交额': '成交额',
            '开盘价': '开盘价',
            '最高价': '最高价',
            '最低价': '最低价',
            '昨收': '昨收',
            '换手率': '换手率',
            '流通市值': '流通市值',
            '总市值': '总市值',
        }
        
        # 选择需要的列
        available_columns = [col for col in column_mapping.keys() if col in df.columns]
        df_selected = df[available_columns].copy()
        
        # 确保数值类型正确
        numeric_columns = ['最新价', '涨跌幅', '涨跌额', '成交量', '成交额', 
                          '开盘价', '最高价', '最低价', '昨收', '换手率', 
                          '流通市值', '总市值']
        
        for col in numeric_columns:
            if col in df_selected.columns:
                df_selected[col] = pd.to_numeric(df_selected[col], errors='coerce')
        
        return df_selected
        
    except Exception as e:
        logging.error(f"fund_etf_spot_em_akshare处理异常：{e}")
        return pd.DataFrame()


def fund_etf_hist_em_akshare(
    symbol: str = "159707",
    period: str = "daily",
    start_date: str = "19700101",
    end_date: str = "20500101",
    adjust: str = "",
) -> pd.DataFrame:
    """
    使用AKShare获取ETF历史行情数据
    https://akshare.akfamily.xyz/data/fund/fund.html
    :param symbol: ETF代码
    :type symbol: str
    :param period: choice of {'daily', 'weekly', 'monthly'}
    :type period: str
    :param start_date: 开始日期
    :type start_date: str
    :param end_date: 结束日期
    :type end_date: str
    :param adjust: choice of {"qfq": "前复权", "hfq": "后复权", "": "不复权"}
    :type adjust: str
    :return: ETF历史行情
    :rtype: pandas.DataFrame
    """
    if not AKSHARE_AVAILABLE:
        return pd.DataFrame()
    
    try:
        # AKShare的调整参数映射
        adjust_map = {"qfq": "qfq", "hfq": "hfq", "": ""}
        period_map = {"daily": "daily", "weekly": "weekly", "monthly": "monthly"}
        
        # 使用akshare的fund_etf_hist_em接口
        df = ak.fund_etf_hist_em(
            symbol=symbol,
            period=period_map.get(period, "daily"),
            start_date=start_date,
            end_date=end_date,
            adjust=adjust_map.get(adjust, "")
        )
        
        if df is None or len(df) == 0:
            return pd.DataFrame()
        
        # 重命名列以匹配项目格式
        df.columns = [
            "日期",
            "开盘",
            "收盘",
            "最高",
            "最低",
            "成交量",
            "成交额",
            "振幅",
            "涨跌幅",
            "涨跌额",
            "换手率",
        ]
        
        # 设置日期索引
        df.index = pd.to_datetime(df["日期"])
        df.reset_index(inplace=True, drop=True)
        
        # 确保数值类型正确
        numeric_columns = ['开盘', '收盘', '最高', '最低', '成交量', '成交额', 
                          '振幅', '涨跌幅', '涨跌额', '换手率']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df
        
    except Exception as e:
        logging.error(f"fund_etf_hist_em_akshare处理异常：{symbol}代码{e}")
        return pd.DataFrame()


if __name__ == "__main__":
    # 测试代码
    print("测试AKShare数据接口...")
    
    if AKSHARE_AVAILABLE:
        print("\n1. 测试获取A股实时行情...")
        df_spot = stock_zh_a_spot_em_akshare()
        if not df_spot.empty:
            print(f"成功获取 {len(df_spot)} 条A股数据")
            print(df_spot.head())
        else:
            print("获取A股实时行情失败")
        
        print("\n2. 测试获取A股历史行情...")
        df_hist = stock_zh_a_hist_akshare(
            symbol="000001",
            period="daily",
            start_date="20240101",
            end_date="20241231",
            adjust="qfq"
        )
        if not df_hist.empty:
            print(f"成功获取 {len(df_hist)} 条历史数据")
            print(df_hist.head())
        else:
            print("获取A股历史行情失败")
        
        print("\n3. 测试获取ETF实时行情...")
        df_etf = fund_etf_spot_em_akshare()
        if not df_etf.empty:
            print(f"成功获取 {len(df_etf)} 条ETF数据")
            print(df_etf.head())
        else:
            print("获取ETF实时行情失败")
    else:
        print("AKShare未安装，无法进行测试")
