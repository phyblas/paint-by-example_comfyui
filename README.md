# paint-by-example_comfyui

（→ [English Description](https://github-com.translate.goog/phyblas/paint-by-example_comfyui/blob/master/README.md?_x_tr_sl=zh-CN&_x_tr_tl=en&_x_tr_hl=zh-CN&_x_tr_pto=wapp)）
（→ [日本語説明はQiitaで](https://qiita.com/phyblas/items/43446cd2c06761c37a93)）

这个包提供了在 ComfyUI 中运行 [Paint by Example](https://github.com/Fantasy-Studio/Paint-by-Example) 功能的节点。

该方法类似于图像修复（inpaint），可以将示例图片插入到原图的指定区域中。无需编写任何提示词，但生成的结果可能不会与示例图片完全相似。尽管如此，有时仍能产生非常有趣的效果。

无需提前手动下载任何模型，但在首次运行节点时，系统会自动从 Hugging Face 下载 [Paint-by-Example 模型](https://huggingface.co/Fantasy-Studio/Paint-by-Example)，因此需要等待一段时间，并且会占用超过 5GB 的硬盘空间。

使用示例工作流可参考：  
https://github.com/phyblas/ironna_comfyui_workflow/tree/master/stable_diffusion/paint-by-example

## 安装

将此仓库放置在 ComfyUI 的 `ComfyUI/custom_nodes/` 文件夹中即可使用。也可以通过 [ComfyUI Manager](https://github.com/ltdrdata/ComfyUI-Manager) 进行安装。

## 节点

这个包提供了 3 个节点。

### PaintbyExampleSimple

最简单基础的用法。需要准备原图、遮罩图和示例图片。可以指定步数和随机种子。

![workflow1.jpg](https://github.com/phyblas/ironna_comfyui_workflow/blob/master/stable_diffusion/paint-by-example/workflow1.jpg)

当然也支持使用遮罩编辑器（mask editor）。

![workflow2.jpg](https://github.com/phyblas/ironna_comfyui_workflow/blob/master/stable_diffusion/paint-by-example/workflow2.jpg)

还支持批量生成多张图片。

![workflow3.jpg](https://github.com/phyblas/ironna_comfyui_workflow/blob/master/stable_diffusion/paint-by-example/workflow3.jpg)

### PaintbyExampleAdvanced

用法与 Simple 版本类似，但提供了更多选项，例如可以添加负面提示词，并支持调整图片尺寸。

![workflow4.jpg](https://github.com/phyblas/ironna_comfyui_workflow/blob/master/stable_diffusion/paint-by-example/workflow4.jpg)

### PaintbyExampleGen

这个节点较为复杂，会先生成一张图片，再将其作为示例图片使用。其输入方式与一般的文生图类似，最终效果可类比于常规的图像修复（inpaint）。

![workflow5.jpg](https://github.com/phyblas/ironna_comfyui_workflow/blob/master/stable_diffusion/paint-by-example/workflow5.jpg)

## BRIA

也可以尝试使用 [BRIA](https://github.com/ZHO-ZHO-ZHO/ComfyUI-BRIA_AI-RMBG) 区隔背景，再进行图像修复以替换其中的内容。

![workflow6.jpg](https://github.com/phyblas/ironna_comfyui_workflow/blob/master/stable_diffusion/paint-by-example/workflow6.jpg)
