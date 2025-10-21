#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AKShare数据源使用示例

本示例展示如何使用AKShare集成功能
"""
import sys
import os

# 添加项目路径
cpath_current = os.path.dirname(os.path.dirname(__file__))
cpath = os.path.abspath(os.path.join(cpath_current, os.pardir))
sys.path.append(cpath)

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def example1_direct_akshare_usage():
    """
    示例1: 直接使用AKShare包装模块
    """
    print("\n" + "=" * 60)
    print("示例1: 直接使用AKShare包装模块")
    print("=" * 60)
    
    import instock.core.crawling.stock_akshare as sak
    
    if not sak.AKSHARE_AVAILABLE:
        print("AKShare未安装，无法运行此示例")
        return
    
    # 获取A股实时行情
    print("\n1. 获取A股实时行情数据...")
    df_stocks = sak.stock_zh_a_spot_em_akshare()
    if not df_stocks.empty:
        print(f"成功获取 {len(df_stocks)} 只股票数据")
        print("前5条数据:")
        print(df_stocks.head())
    else:
        print("获取数据失败（可能是网络问题）")
    
    # 获取ETF实时行情
    print("\n2. 获取ETF实时行情数据...")
    df_etf = sak.fund_etf_spot_em_akshare()
    if not df_etf.empty:
        print(f"成功获取 {len(df_etf)} 只ETF数据")
        print("前5条数据:")
        print(df_etf.head())
    else:
        print("获取数据失败（可能是网络问题）")

def example2_switch_to_akshare():
    """
    示例2: 切换默认数据源到AKShare
    """
    print("\n" + "=" * 60)
    print("示例2: 切换默认数据源到AKShare")
    print("=" * 60)
    
    import instock.lib.data_source_config as dsc
    
    # 显示当前配置
    print(f"\n当前默认数据源: {dsc.DEFAULT_DATA_SOURCE}")
    print(f"自动切换功能: {'启用' if dsc.ENABLE_AUTO_FALLBACK else '禁用'}")
    
    # 切换到AKShare
    original_source = dsc.DEFAULT_DATA_SOURCE
    dsc.DEFAULT_DATA_SOURCE = dsc.DATA_SOURCE_AKSHARE
    
    print(f"\n已切换默认数据源到: {dsc.DEFAULT_DATA_SOURCE}")
    print("现在所有数据获取将优先使用AKShare")
    
    # 注意: 在实际使用中，应该修改data_source_config.py文件而不是动态修改
    print("\n提示: 在生产环境中，应该修改 instock/lib/data_source_config.py 文件")
    print("      而不是在代码中动态修改配置")
    
    # 恢复原始配置
    dsc.DEFAULT_DATA_SOURCE = original_source
    print(f"\n已恢复默认数据源到: {dsc.DEFAULT_DATA_SOURCE}")

def example3_auto_fallback():
    """
    示例3: 演示自动容错切换
    """
    print("\n" + "=" * 60)
    print("示例3: 自动容错切换机制")
    print("=" * 60)
    
    import instock.lib.data_source_config as dsc
    
    print(f"\n自动容错切换: {'启用' if dsc.ENABLE_AUTO_FALLBACK else '禁用'}")
    print(f"数据源顺序: {dsc.FALLBACK_ORDER}")
    
    print("\n工作原理:")
    print("1. 首先尝试使用默认数据源获取数据")
    print("2. 如果失败且启用了自动切换，按顺序尝试备用数据源")
    print("3. 使用第一个成功的数据源返回数据")
    
    print("\n配置建议:")
    print("- 生产环境建议启用自动切换 (ENABLE_AUTO_FALLBACK = True)")
    print("- 根据实际情况调整数据源顺序 (FALLBACK_ORDER)")
    
    # 示例：如何配置不同的场景
    print("\n场景配置示例:")
    print("\n场景1: 仅使用AKShare，不使用容错")
    print("  DEFAULT_DATA_SOURCE = DATA_SOURCE_AKSHARE")
    print("  ENABLE_AUTO_FALLBACK = False")
    
    print("\n场景2: 优先AKShare，东方财富作为备用")
    print("  DEFAULT_DATA_SOURCE = DATA_SOURCE_AKSHARE")
    print("  ENABLE_AUTO_FALLBACK = True")
    print("  FALLBACK_ORDER = [DATA_SOURCE_AKSHARE, DATA_SOURCE_EASTMONEY]")
    
    print("\n场景3: 优先东方财富，AKShare作为备用（默认配置）")
    print("  DEFAULT_DATA_SOURCE = DATA_SOURCE_EASTMONEY")
    print("  ENABLE_AUTO_FALLBACK = True")
    print("  FALLBACK_ORDER = [DATA_SOURCE_EASTMONEY, DATA_SOURCE_AKSHARE]")

def example4_get_historical_data():
    """
    示例4: 获取历史数据
    """
    print("\n" + "=" * 60)
    print("示例4: 获取历史数据")
    print("=" * 60)
    
    import instock.core.crawling.stock_akshare as sak
    
    if not sak.AKSHARE_AVAILABLE:
        print("AKShare未安装，无法运行此示例")
        return
    
    # 获取股票历史数据
    print("\n1. 获取股票历史数据（000001 平安银行）...")
    df_hist = sak.stock_zh_a_hist_akshare(
        symbol="000001",
        period="daily",
        start_date="20240101",
        end_date="20241231",
        adjust="qfq"  # 前复权
    )
    
    if not df_hist.empty:
        print(f"成功获取 {len(df_hist)} 天的历史数据")
        print("最近5天数据:")
        print(df_hist.tail())
    else:
        print("获取数据失败（可能是网络问题）")
    
    # 获取ETF历史数据
    print("\n2. 获取ETF历史数据（513500 标普500ETF）...")
    df_etf_hist = sak.fund_etf_hist_em_akshare(
        symbol="513500",
        period="daily",
        start_date="20240101",
        end_date="20241231",
        adjust="qfq"
    )
    
    if not df_etf_hist.empty:
        print(f"成功获取 {len(df_etf_hist)} 天的历史数据")
        print("最近5天数据:")
        print(df_etf_hist.tail())
    else:
        print("获取数据失败（可能是网络问题）")

def main():
    """
    主函数
    """
    print("=" * 60)
    print("AKShare数据源使用示例")
    print("=" * 60)
    
    print("\n提示: 由于网络限制，某些数据获取可能失败")
    print("      这是正常现象，不影响功能演示")
    
    # 运行所有示例
    example1_direct_akshare_usage()
    example2_switch_to_akshare()
    example3_auto_fallback()
    example4_get_historical_data()
    
    print("\n" + "=" * 60)
    print("示例结束")
    print("=" * 60)
    
    print("\n更多信息请参考:")
    print("- instock/core/crawling/AKSHARE_README.md")
    print("- https://akshare.akfamily.xyz/")

if __name__ == "__main__":
    main()
