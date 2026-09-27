# Irrigation-C3 Mainboard V1

唯一主项目文件：`easyeda_source/Irrigation-C3_Mainboard_V1.epro2`。

当前只维护 `01_POWER_CLEAN` 原理图页；本次交付不包含 PCB，也不包含 `02_ESP32_USB`。

验证入口：

```bash
python3 01_POWER_Handover/01_03_POWER_Verification_Script.py
```

`01_POWER_Handover/` 保存本次回读快照、黄金网络表、渲染图和发布阻塞说明。
