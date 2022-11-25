# -*- coding: utf-8 -*-
'''Cung cấp các công cụ hay dùng trong hệ thống.
Module gồm các công cụ:
    - get_locale: Lấy thông tin locale hiện tại của request (i18n)
    - get_timezone: Lấy thông tin timezone hiện tại của request (i18n)
'''
from flask import g, request


def get_locale():
    '''Lấy thông tin locale hiện tại của request
    Dùng cho i18n, mỗi request sẽ chứa thông tin accept_languages trong header
    để phân định ngôn ngữ trả ra của API.
    Hiện tại chỉ hỗ trợ tiếng anh (en) và tiếng việt (vi)

    Args:
    Returns:
        Trả ra ngôn ngữ hiện tại của request
    Raises:
    '''
    # if a user is logged in, use the locale from the user settings
    user = getattr(g, 'user', None)
    if user is not None:
        return user.locale
    # otherwise try to guess the language from the user accept
    # header the browser transmits.  We support de/fr/en in this
    # example.  The best match wins.
    return request.accept_languages.best_match(['vi', 'en'])


def get_timezone():
    '''Lấy thông tin timezone của user
    Dùng cho i18n tương tự hàm get_locale.

    Args:
    Returns:
        Trả ra timezone tương ứng với khu vực hiện tại
    Raises:
    '''
    user = getattr(g, 'user', None)
    if user is not None:
        return user.timezone
    return None
