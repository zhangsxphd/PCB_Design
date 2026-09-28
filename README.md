# Irrigation-C3 Mainboard V1

唯一主项目文件：`easyeda_source/Irrigation-C3_Mainboard_V1.epro2`。

当前状态：

| 页面 | 状态 |
| --- | --- |
| `01_POWER_CLEAN` | 电气基线 PASS；视觉清理待完成，保持不变 |
| `02_ESP32_USB` | 电气快照 PASS；分区与 DRC warning 待处理，原理图发布 FAIL |
| `03_RS485_SCALE` | 未开始 |
| `04_PUMP_DRIVER` | 未开始 |
| `05_IO_EXPANSION` | 未开始 |

PCB 发布仍为 BLOCKED；未进行 PCB 同步、布局或布线。

验证入口：

```bash
python3 scripts/verify_all.py
```

`01_POWER_Handover/` 与 `02_ESP32_USB_Handover/` 分别保存各页的回读快照、黄金网络表、渲染图和发布阻塞说明。
