import re
#正则清洗user_data_re
def user_data_re(temp):
    temp=str(temp)
    result_re = re.findall(r"[1-9]\d*|0",temp)
    return result_re


#正则清洗源文件内容
def replace_tag(html, completely=True):
    """替换HTML标签"""
    # 独立元素
    html = re.sub('<img[^>]*>', '', html)  # 图片
    html = re.sub('<br/?>|<br [^<>]*>|<hr/?>|<hr [^<>]*>', '\n', html)  # 换行、水平线
    html = re.sub('&(nbsp|e[mn]sp|thinsp|zwn?j|#13);', ' ', html)  # 空格
    html = re.sub(r'\xa0|\\xa0|\u3000|\\u3000', ' ', html)  # 空格
    html = re.sub(r'<!--[\s\S]*?-->', '', html)  # 注释
    html = re.sub(r'<head>[\s\S]*?</head>', '', html)
    html = re.sub(r'<meta[^<>]*>[\s\S]*?</meta>', '', html)  # 元数据
    html = re.sub(r'<style[^<>]*>[\s\S]*?</style>', '', html)  # 样式
    html = re.sub(r'<script[^<>]*>[\s\S]*?</script>', '', html)  # JavaScript
    html = re.sub(r'<s>[\s\S]*?</s>', '', html)  # 删除线（内容也清除）
    html = re.sub('<input>|<input [^>]*>', '', html)  # 输入框（表单中元素）
    # 行内元素
    html = re.sub('<u>|<u [^>]*>|</u>', '', html)  # 下划线 underline
    html = re.sub('<i>|<i [^>]*>|</i>', '', html)  # 斜体 italic
    html = re.sub('<b>|<b [^>]*>|</b>', '', html)  # 粗体
    html = re.sub('<em>|<em [^>]*>|</em>', '', html)  # 强调 emphasize
    html = re.sub('<strong>|<strong [^>]*>|</strong>', '', html)  # 粗体
    html = re.sub('<mark>|<mark [^>]*>|</mark>', '', html)  # 黄色背景填充标记
    html = re.sub('<font>|<font [^>]*>|</font>', '', html)  # 字体
    html = re.sub('<a>|<a [^>]*>|</a>', '', html)  # 超链接
    html = re.sub('<span>|<span [^>]*>|</span>', '', html)  # span
    # 块级元素
    html = re.sub('<p>|<p [^>]*>|</p>', '\n', html)  # 段落
    html = re.sub('<h[1-6][^>]*>|</h[1-6]>', '\n', html)  # 标题
    html = re.sub('<li>|<li [^>]*>|</li>', '\n', html)  # 列表 list
    html = re.sub('<ol>|<ol [^>]*>|</ol>', '\n', html)  # 有序列表 ordered list
    html = re.sub('<ul>|<ul [^>]*>|</ul>', '\n', html)  # 无序列表 unordered list
    html = re.sub('<pre>|<pre [^>]*>|</pre>', '\n', html)  # 预格化，可保留连续空白符
    html = re.sub('<div>|<div [^>]*>|</div>', '\n', html)  # 分割 division
    html = re.sub('<section[^>]*>|</section>', '\n', html)  # 章节
    html = re.sub('<form>|<form [^>]*>|</form>', '\n', html)  # 表单（用于向服务器传输数据）
    html = re.sub('<o:p>|<o:p [^>]*>|</o:p>', '\n', html)  # OFFICE微软WORD段落
    html = re.sub(r'<td[^>]*>([\s\S]*?)</td>', lambda x: ' %s ' % x.group(1), html)  # 表格
    html = re.sub(r'<tr[^>]*>([\s\S]*?)</tr>', lambda x: '%s\n' % x.group(1), html)  # 表格
    html = re.sub(r'<th[^>]*>([\s\S]*?)</th>', lambda x: '%s\n' % x.group(1), html)  # 表格
    html = re.sub(r'<tbody[^>]*>([\s\S]*?)</tbody>', lambda x: '%s\n' % x.group(1), html)  # 表格
    html = re.sub(r'<table[^>]*>([\s\S]*?)</table>', lambda x: '%s\n' % x.group(1), html)  # 表格
    # 剩余标签
    if completely is True:
        html = re.sub(r'<canvas[^<>]*>[\s\S]*?</canvas>', '', html)  # 画布
        html = re.sub(r'<iframe[^<>]*>[\s\S]*?</iframe>', '', html)  # 内框架
        html = re.sub('<([^<>\u4e00-\u9fa5]|微软雅黑|宋体|仿宋)+>', '', html)
    # 转义字符
    html = html.replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&amp;', '&')
    return replace_space(html)
#清除连续空白符
def replace_space(text):
    """清除连续空白"""
    text = re.sub(r'\s*\n\s*', '\n', text.strip())
    text = re.sub('[ \f\r\t　]+', ' ', text)
    text = re.sub('([\u4e00-\u9fa5]) ([^\u4e00-\u9fa5])', lambda x: x.group(1)+x.group(2), text)
    text = re.sub('([^\u4e00-\u9fa5]) ([\u4e00-\u9fa5])', lambda x: x.group(1)+x.group(2), text)
    return text


