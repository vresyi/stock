# AKShare数据源快速参考

## 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 使用默认配置（推荐）
无需任何配置，系统会自动使用东方财富作为主数据源，AKShare作为备用。

### 3. 切换到AKShare
编辑 `instock/lib/data_source_config.py`:
```python
DEFAULT_DATA_SOURCE = DATA_SOURCE_AKSHARE
```

## 配置选项

| 配置项 | 说明 | 默认值 |
|-------|------|--------|
| DEFAULT_DATA_SOURCE | 主数据源 | eastmoney |
| ENABLE_AUTO_FALLBACK | 自动切换 | True |
| FALLBACK_ORDER | 切换顺序 | [eastmoney, akshare] |

## 使用场景

### 场景1: 默认配置（东方财富为主）
```python
# 不需要修改配置
import instock.core.stockfetch as sf
stocks = sf.fetch_stocks(date)
```

### 场景2: AKShare为主
修改配置文件:
```python
DEFAULT_DATA_SOURCE = DATA_SOURCE_AKSHARE
ENABLE_AUTO_FALLBACK = True
```

### 场景3: 仅用AKShare
修改配置文件:
```python
DEFAULT_DATA_SOURCE = DATA_SOURCE_AKSHARE
ENABLE_AUTO_FALLBACK = False
```

## 测试

### 运行集成测试
```bash
python3 test_akshare_integration.py
```

### 运行示例代码
```bash
python3 example_akshare_usage.py
```

## API快速参考

### 直接使用AKShare模块

```python
import instock.core.crawling.stock_akshare as sak

# A股实时行情
df = sak.stock_zh_a_spot_em_akshare()

# A股历史行情
df = sak.stock_zh_a_hist_akshare(
    symbol="000001",
    period="daily",
    start_date="20240101",
    end_date="20241231",
    adjust="qfq"
)

# ETF实时行情
df = sak.fund_etf_spot_em_akshare()

# ETF历史行情
df = sak.fund_etf_hist_em_akshare(
    symbol="513500",
    period="daily",
    start_date="20240101",
    end_date="20241231",
    adjust="qfq"
)
```

## 故障排查

### 问题1: 数据获取失败
**原因**: 网络连接问题或数据源不可用  
**解决**: 
1. 检查网络连接
2. 启用自动切换: `ENABLE_AUTO_FALLBACK = True`
3. 查看日志: `instock/log/stock_execute_job.log`

### 问题2: AKShare未安装
**原因**: 依赖未安装  
**解决**: 
```bash
pip install akshare
```

### 问题3: 配置不生效
**原因**: 配置文件未修改或修改错误  
**解决**: 
1. 确认修改了 `instock/lib/data_source_config.py`
2. 重启应用

## 性能建议

1. **首次使用**: 缓存数据后速度会提升
2. **网络**: 确保网络连接稳定
3. **容错**: 生产环境启用自动切换
4. **日志**: 定期清理日志文件

## 更多资源

- 详细文档: `instock/core/crawling/AKSHARE_README.md`
- 集成总结: `INTEGRATION_SUMMARY.md`
- AKShare官网: https://akshare.akfamily.xyz/
- 项目README: `README.md`

## 技术支持

如遇问题，请参考:
1. 日志文件: `instock/log/stock_execute_job.log`
2. 测试文件: `test_akshare_integration.py`
3. 示例代码: `example_akshare_usage.py`

---
版本: 1.0.0 | 日期: 2025-10-21
