# AKShare数据源集成说明

## 概述

本项目已集成 [AKShare](https://akshare.akfamily.xyz/) 数据源，提供更加稳定和可靠的A股市场数据获取能力。

## 功能特性

1. **多数据源支持**：支持东方财富（EastMoney）和AKShare两种数据源
2. **自动容错切换**：当主数据源失败时，自动尝试备用数据源
3. **无缝集成**：对现有代码完全透明，无需修改业务逻辑
4. **灵活配置**：可以轻松切换主数据源和配置容错行为

## 文件说明

### 新增文件

1. **instock/core/crawling/stock_akshare.py**
   - AKShare数据源的封装模块
   - 提供与东方财富接口兼容的数据格式
   - 支持A股实时行情、历史行情、ETF数据等

2. **instock/lib/data_source_config.py**
   - 数据源配置文件
   - 可配置默认数据源和容错行为

### 修改文件

1. **requirements.txt**
   - 添加了 `akshare>=1.14.0` 依赖

2. **instock/core/stockfetch.py**
   - 更新了数据获取函数，集成了多数据源支持
   - 添加了自动容错切换逻辑

## 使用说明

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置数据源

编辑 `instock/lib/data_source_config.py` 文件：

```python
# 数据源类型
DATA_SOURCE_EASTMONEY = "eastmoney"  # 东方财富（默认）
DATA_SOURCE_AKSHARE = "akshare"      # AKShare

# 默认数据源（可以在这里修改首选数据源）
DEFAULT_DATA_SOURCE = DATA_SOURCE_EASTMONEY

# 是否启用数据源自动切换
ENABLE_AUTO_FALLBACK = True

# 备用数据源顺序
FALLBACK_ORDER = [DATA_SOURCE_EASTMONEY, DATA_SOURCE_AKSHARE]
```

#### 配置选项说明

- **DEFAULT_DATA_SOURCE**: 设置主数据源
  - `DATA_SOURCE_EASTMONEY`: 使用东方财富数据源（默认）
  - `DATA_SOURCE_AKSHARE`: 使用AKShare数据源

- **ENABLE_AUTO_FALLBACK**: 是否启用自动切换
  - `True`: 当主数据源失败时，自动尝试备用数据源
  - `False`: 仅使用主数据源

- **FALLBACK_ORDER**: 数据源尝试顺序
  - 按列表顺序依次尝试数据源

### 3. 使用示例

#### 场景一：使用默认配置（东方财富为主，AKShare为备用）

不需要修改任何代码，系统会自动使用东方财富数据源，失败时自动切换到AKShare。

#### 场景二：切换到AKShare作为主数据源

修改 `data_source_config.py`：

```python
DEFAULT_DATA_SOURCE = DATA_SOURCE_AKSHARE
```

#### 场景三：仅使用AKShare，不使用容错

修改 `data_source_config.py`：

```python
DEFAULT_DATA_SOURCE = DATA_SOURCE_AKSHARE
ENABLE_AUTO_FALLBACK = False
```

## API接口

### stock_akshare.py 提供的接口

#### 1. stock_zh_a_spot_em_akshare()
获取A股实时行情数据

```python
import instock.core.crawling.stock_akshare as sak
df = sak.stock_zh_a_spot_em_akshare()
```

#### 2. stock_zh_a_hist_akshare()
获取A股历史行情数据

```python
df = sak.stock_zh_a_hist_akshare(
    symbol="000001",
    period="daily",
    start_date="20240101",
    end_date="20241231",
    adjust="qfq"
)
```

#### 3. fund_etf_spot_em_akshare()
获取ETF实时行情数据

```python
df = sak.fund_etf_spot_em_akshare()
```

#### 4. fund_etf_hist_em_akshare()
获取ETF历史行情数据

```python
df = sak.fund_etf_hist_em_akshare(
    symbol="513500",
    period="daily",
    start_date="20240101",
    end_date="20241231",
    adjust="qfq"
)
```

## 测试

### 测试AKShare模块

```bash
cd /home/runner/work/stock/stock
python3 instock/core/crawling/stock_akshare.py
```

### 测试数据获取功能

```python
import instock.core.stockfetch as sf
import datetime

# 获取今日股票数据
stocks = sf.fetch_stocks(datetime.datetime.now().date())
print(f"获取到 {len(stocks)} 只股票")

# 获取ETF数据
etfs = sf.fetch_etfs(datetime.datetime.now().date())
print(f"获取到 {len(etfs)} 只ETF")
```

## 优势

1. **数据源可靠性提升**：通过多数据源支持，提高了数据获取的成功率
2. **容错能力增强**：自动切换机制保证了系统的稳定运行
3. **维护性好**：配置简单，易于调整
4. **兼容性强**：完全兼容现有代码，无需修改业务逻辑

## 注意事项

1. AKShare依赖网络连接，请确保网络畅通
2. 首次使用AKShare可能需要较长时间初始化
3. 建议在生产环境启用容错机制（`ENABLE_AUTO_FALLBACK = True`）
4. 数据格式已经过统一处理，两种数据源返回格式一致

## 技术支持

如有问题，请参考：
- AKShare官方文档：https://akshare.akfamily.xyz/
- 项目README：../README.md

## 版本历史

- 2025-10-21: 初始版本，集成AKShare数据源支持
