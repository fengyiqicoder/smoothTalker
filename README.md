# smoothTalker

一个纯静态的 Muse connector。没有服务器，只有一份 OpenAPI 文档和一组 JSON 文件，托管在 GitHub Pages 上。

- 托管地址：https://fengyiqicoder.github.io/smoothTalker/
- OpenAPI：https://fengyiqicoder.github.io/smoothTalker/openapi.json
- 数据索引：https://fengyiqicoder.github.io/smoothTalker/data/index.json

## 接入 Muse

把 `MUSE_PROMPT.md` 里的那段话发给 Muse，它会读 OpenAPI 文档、在自己的 VM 里搭好桥接、保存成 skill。不需要 API key。

## 数据结构

每条内容是 `data/entries/<id>.json`：

```json
{
  "id": "sample-001",
  "title": "条目标题",
  "tags": ["标签1", "标签2"],
  "summary": "一句话摘要，给 Agent 判断是否相关用",
  "body": "正文，Markdown 或纯文本",
  "updated": "2026-09-24"
}
```

`data/index.json` 是所有条目的 id / title / tags / summary 汇总，由脚本生成，不要手改。

## 添加内容

1. 在 `data/entries/` 下新建一个 JSON 文件，文件名就是 id
2. 运行 `python3 scripts/build_index.py`，它会校验字段并重新生成 `data/index.json`
3. commit 并 push，GitHub Pages 一两分钟后生效

## 为什么这样设计

Muse 自己有浏览器，公开小文档它直接读。静态 connector 只在"结构化、体量大、需要检索、权威一致"时才值得做。index.json 让 Agent 一次调用拿到全部摘要自行筛选，再按 id 取正文，两次请求完成检索。详见 `../research/03-社区聚合现状.md` 和聊天记录里关于静态 connector 的讨论。
