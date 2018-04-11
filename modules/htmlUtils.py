#!/usr/bin/python
# -*- coding: utf-8 -*-


def table_to_html(table):
    """
    format a matrix-like table to html style
    :param table: <2-dim List>
    :return: html style table
    """
    html = [''.join(['<td>{}</td>'.format(item) for item in row]) for row in table]  # add <td></td> environment out of table item
    html = ''.join(['<tr>{}</tr>'.format(row) for row in html])  # add <tr></tr> environment out of table row
    return '<table border="1" bordercolor="#999999" border="1" style="background-color:#F0F0E8;\
    border-color:#999999;font-size:X-Small;width:100%;border-collapse:collapse;">{}</table>'.format(html)