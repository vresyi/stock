#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据源配置模块
支持多数据源配置和切换
"""

# 数据源类型
DATA_SOURCE_EASTMONEY = "eastmoney"  # 东方财富（默认）
DATA_SOURCE_AKSHARE = "akshare"      # AKShare

# 默认数据源（可以在这里修改首选数据源）
DEFAULT_DATA_SOURCE = DATA_SOURCE_EASTMONEY

# 是否启用数据源自动切换（当主数据源失败时自动尝试备用数据源）
ENABLE_AUTO_FALLBACK = True

# 备用数据源顺序
FALLBACK_ORDER = [DATA_SOURCE_EASTMONEY, DATA_SOURCE_AKSHARE]
