#!/usr/bin/env python
"""Django 的命令行管理工具。"""
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studyroom_system.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "无法导入 Django。确认已激活虚拟环境并安装了依赖。"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
