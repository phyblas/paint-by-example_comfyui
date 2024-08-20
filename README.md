# paint-by-example_comfyui

（[english description](https://github-com.translate.goog/phyblas/paint-by-example_comfyui/blob/master/README.md?_x_tr_sl=zh-CN&_x_tr_tl=en&_x_tr_hl=zh-CN&_x_tr_pto=wapp)）

这个包是提供用来在comfyui执行[paint by example](https://github.com/Fantasy-Studio/Paint-by-Example)的节点。

这个方法可以把作为例子的图片插入到原本图片中所要的地方。不必须要写任何提示词。但被画的图也可能不太像例子的图。虽然如此有时候会导出很有意思的结果。

没必须要提前手动下载任何模型，但首次执行节点的时候会自动下载paint by example模型，所以要等一段时间并且会占用大于5GB的硬盘。

使用这个的工作流例子可以看 https://github.com/phyblas/stadif_comfyui_workflow/tree/master/paint-by-example


## install

把这个repo放在comfyui`ComfyUI/custom_nodes/`文件夹里的就能用了。


## PaintbyExampleSimple

最简单最基本的节点。要准备原本图片和遮罩和例子图片。可以指定步数的种子。

![workflow1.jpg](https://github.com/phyblas/stadif_comfyui_workflow/blob/master/paint-by-example/workflow1.jpg)

当然也可以用maskeditor。

![workflow2.jpg](https://github.com/phyblas/stadif_comfyui_workflow/blob/master/paint-by-example/workflow2.jpg)

也支持同时生成几张。

![workflow3.jpg](https://github.com/phyblas/stadif_comfyui_workflow/blob/master/paint-by-example/workflow3.jpg)


## PaintbyExampleAdvanced

跟simple的用法差不多。只是多家了几个选项。例如可以写负面提示词。

![workflow4.jpg](https://github.com/phyblas/stadif_comfyui_workflow/blob/master/paint-by-example/workflow4.jpg)

## PaintbyExampleGen

这个节点有点复杂。是先生成图片，再拿来做例子图片。生成需要用的输入是跟一般文生图差不多。结果可以说是像一般的inpaint的。

![workflow5.jpg](https://github.com/phyblas/stadif_comfyui_workflow/blob/master/paint-by-example/workflow5.jpg)