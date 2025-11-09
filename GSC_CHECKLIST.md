# Google Search Console 配置检查清单

## ✅ 必须完成的步骤

### 1. 资源配置检查

**当前日期**: 2025-11-09

- [ ] **打开 Google Search Console**: https://search.google.com/search-console
- [ ] **点击左上角资源选择器**，确认显示的是：
  ```
  https://cjss-tech.github.io/hwtg/
  ```
  **不是**：`cjss-tech.github.io`

**如果显示错误**：
- [ ] 点击 "添加资源"
- [ ] 选择 "网址前缀"
- [ ] 输入：`https://cjss-tech.github.io/hwtg/`
- [ ] 选择 "HTML 标签" 验证方法
- [ ] 验证代码已在网站：`WZAZ1vMV-H4R6eVw3kAcO1v6A-cbGGP67oXt72LiZDY`
- [ ] 点击"验证"按钮 → 应该成功 ✅

---

### 2. Sitemap 提交检查

**在正确的资源下**（`https://cjss-tech.github.io/hwtg/`）：

- [ ] 左侧菜单 → 站点地图
- [ ] 查看是否已提交 `sitemap.xml`
  - **如果有旧的且状态为"错误"**：
    - [ ] 点击右侧三点菜单 → 删除
    - [ ] 等待几秒
  - **重新提交**：
    - [ ] 在输入框输入：`sitemap.xml`
    - [ ] 点击"提交"
    - [ ] 等待状态变为"成功"（可能需要几小时）

---

### 3. 手动请求索引

**在正确的资源下**：

- [ ] 点击顶部搜索框
- [ ] 输入：`https://cjss-tech.github.io/hwtg/`
- [ ] 按回车，等待检查（30秒-1分钟）
- [ ] 查看结果：
  - **如果显示"URL 已被 Google 编入索引"**：
    - ✅ 恭喜！已经成功了
  - **如果显示"URL 未被 Google 编入索引"**：
    - [ ] 点击"请求编入索引"按钮
    - [ ] 等待 1-2 分钟
    - [ ] 显示"已请求编入索引" → 成功

---

### 4. 验证文件可访问性

**打开浏览器，访问以下 URL，确认都能正常打开**：

- [ ] https://cjss-tech.github.io/hwtg/
  - 应该显示网站首页
  
- [ ] https://cjss-tech.github.io/hwtg/robots.txt
  - 应该显示 robots.txt 内容
  
- [ ] https://cjss-tech.github.io/hwtg/sitemap.xml
  - 应该显示 XML 格式的 sitemap

**查看网站源代码**：
- [ ] 右键 → 查看源代码
- [ ] 搜索 `google-site-verification`
- [ ] 确认存在：`content="WZAZ1vMV-H4R6eVw3kAcO1v6A-cbGGP67oXt72LiZDY"`

---

### 5. 检查索引状态

**24小时后检查**：

- [ ] Google 搜索框输入：`site:cjss-tech.github.io/hwtg`
- [ ] 查看是否有搜索结果

**3-7天后检查**：

- [ ] Google Search Console → 覆盖率
- [ ] 查看"有效"页面数量（应该至少有 1 个）

---

## 🚨 常见错误和解决方案

### 错误 1：资源配置错误

**症状**：
- 显示"未检测到引荐站点地图"
- 显示"Google 无法识别此网址"

**原因**：
- 在错误的资源（`cjss-tech.github.io`）中提交了 sitemap
- 验证代码在子路径（`/hwtg/`），但资源配置为根域名

**解决**：
- 必须在 `https://cjss-tech.github.io/hwtg/` 资源中操作
- 重新添加正确的资源

---

### 错误 2：Sitemap 路径错误

**症状**：
- Sitemap 状态显示"无法抓取"

**原因**：
- 提交了完整 URL：`https://cjss-tech.github.io/hwtg/sitemap.xml` ❌

**解决**：
- 只提交文件名：`sitemap.xml` ✅
- Google 会自动拼接为：`https://cjss-tech.github.io/hwtg/sitemap.xml`

---

### 错误 3：等待时间不够

**症状**：
- 提交后立即检查，显示"未编入索引"

**原因**：
- Google 需要时间抓取和索引

**解决**：
- 请求手动索引后，等待 **1-3 天**
- 正常情况下，**1-2 周**才会完全索引

---

## 📊 预期时间线

| 操作 | 预期时间 | 状态检查 |
|------|---------|---------|
| 提交 Sitemap | 立即 | GSC 中显示"已提交" |
| Sitemap 被读取 | 1-24 小时 | 状态变为"成功" |
| 请求手动索引 | 立即 | 显示"已请求" |
| Google 首次抓取 | 1-3 天 | URL 检查工具显示"已抓取" |
| 首次编入索引 | 3-7 天 | site: 搜索有结果 |
| 搜索结果出现 | 1-4 周 | 自然搜索能找到 |

---

## 🎯 最重要的提示

### ⚠️ 确保资源配置正确！

**这是最常见的错误原因**：

```
❌ 错误配置：
   资源：cjss-tech.github.io
   验证代码位置：/hwtg/index.html
   结果：Google 找不到验证代码

✅ 正确配置：
   资源：https://cjss-tech.github.io/hwtg/
   验证代码位置：/hwtg/index.html
   结果：验证成功，可以正常索引
```

---

## 📞 需要帮助？

**完成清单后，告诉我**：

1. ✅ 你在 Google Search Console 中看到的资源名称是什么？
2. ✅ Sitemap 提交后显示什么状态？
3. ✅ URL 检查工具显示什么信息？
4. ✅ 有没有任何错误提示？

**我会根据具体情况帮你诊断！**

---

**创建日期**: 2025-11-09  
**下次检查**: 2025-11-10（24小时后）
