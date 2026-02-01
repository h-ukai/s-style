#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Django → Jinja2 テンプレート構文変換スクリプト

Django: {{value|filter:"arg"}}
Jinja2: {{value|filter("arg")}}

Django: {% ifchanged var.attr %}...{% endifchanged %}
Jinja2: {% if loop.first or loop.previtem.attr != var.attr %}...{% endif %}
"""

import os
import re
import glob


def convert_ifchanged_tags(content):
    """
    Django の ifchanged タグを Jinja2 互換に変換

    {% ifchanged data.shikutyosonmei %}
    →
    {% if loop.first or loop.previtem.shikutyosonmei != data.shikutyosonmei %}

    {% endifchanged %}
    →
    {% endif %}
    """
    # {% ifchanged variable.attribute %} パターン
    # 例: {% ifchanged data.shikutyosonmei %}
    def replace_ifchanged(match):
        full_var = match.group(1).strip()  # data.shikutyosonmei
        # 最後の属性名を取得
        if '.' in full_var:
            attr = full_var.split('.')[-1]  # shikutyosonmei
        else:
            attr = full_var

        return f'{{% if loop.first or loop.previtem.{attr} != {full_var} %}}'

    content = re.sub(
        r'\{%\s*ifchanged\s+([^%]+?)\s*%\}',
        replace_ifchanged,
        content
    )

    # {% endifchanged %} → {% endif %}
    content = re.sub(
        r'\{%\s*endifchanged\s*%\}',
        '{% endif %}',
        content
    )

    return content


def convert_ifequal_tags(content):
    """
    Django の ifequal/ifnotequal タグを Jinja2 互換に変換

    {% ifequal var "value" %} → {% if var == "value" %}
    {% ifnotequal var "value" %} → {% if var != "value" %}
    {% endifequal %} / {% endifnotequal %} → {% endif %}
    """
    # {% ifequal var1 var2 %} or {% ifequal var "string" %}
    def replace_ifequal(match):
        var1 = match.group(1).strip()
        var2 = match.group(2).strip()
        return f'{{% if {var1} == {var2} %}}'

    def replace_ifnotequal(match):
        var1 = match.group(1).strip()
        var2 = match.group(2).strip()
        return f'{{% if {var1} != {var2} %}}'

    # {% ifequal var1 var2 %} - 変数またはクォート文字列
    content = re.sub(
        r'\{%\s*ifequal\s+(\S+)\s+("[^"]*"|\S+)\s*%\}',
        replace_ifequal,
        content
    )

    content = re.sub(
        r'\{%\s*ifnotequal\s+(\S+)\s+("[^"]*"|\S+)\s*%\}',
        replace_ifnotequal,
        content
    )

    # {% endifequal %} / {% endifnotequal %} → {% endif %}
    content = re.sub(
        r'\{%\s*endifequal\s*%\}',
        '{% endif %}',
        content
    )
    content = re.sub(
        r'\{%\s*endifnotequal\s*%\}',
        '{% endif %}',
        content
    )

    return content


def convert_filter_syntax(content):
    """
    Django フィルタ構文を Jinja2 構文に変換

    例:
    - |floatformat:"-2" → |floatformat("-2")
    - |default:"" → |default("")
    - |default_if_none:"" → |default_if_none("")
    - |slice:":10" → |slice(":10")
    """
    # パターン: |フィルタ名:"引数" または |フィルタ名:変数
    # 文字列引数（クォート付き）
    pattern_quoted = r'\|(\w+):"([^"]*)"'
    replacement_quoted = r'|\1("\2")'

    # 文字列引数（シングルクォート）
    pattern_single = r"\|(\w+):'([^']*)'"
    replacement_single = r"|\1('\2')"

    # 数値や変数引数（クォートなし、次のフィルタや}}まで）
    pattern_unquoted = r'\|(\w+):([^|}\s"\']+)'

    def replace_unquoted(match):
        filter_name = match.group(1)
        arg = match.group(2)
        # 数値の場合はそのまま、変数の場合も括弧で囲む
        return f'|{filter_name}({arg})'

    # 変換実行
    content = re.sub(pattern_quoted, replacement_quoted, content)
    content = re.sub(pattern_single, replacement_single, content)
    content = re.sub(pattern_unquoted, replace_unquoted, content)

    return content


def process_file(filepath):
    """ファイルを読み込み、変換して保存"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            original = f.read()
    except UnicodeDecodeError:
        # UTF-8で読めない場合はshift_jisを試す
        try:
            with open(filepath, 'r', encoding='shift_jis') as f:
                original = f.read()
        except:
            print(f'  スキップ（エンコーディングエラー）: {filepath}')
            return False

    converted = convert_filter_syntax(original)
    converted = convert_ifchanged_tags(converted)
    converted = convert_ifequal_tags(converted)

    if original != converted:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(converted)
        return True
    return False


def main():
    """テンプレートディレクトリ内の全HTMLファイルを変換"""
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')

    print(f'テンプレートディレクトリ: {template_dir}')
    print('変換開始...\n')

    converted_count = 0
    total_count = 0

    for filepath in glob.glob(os.path.join(template_dir, '**', '*.html'), recursive=True):
        total_count += 1
        filename = os.path.basename(filepath)

        if process_file(filepath):
            print(f'  変換: {filename}')
            converted_count += 1
        else:
            print(f'  変更なし: {filename}')

    print(f'\n完了: {converted_count}/{total_count} ファイルを変換しました')


if __name__ == '__main__':
    main()
