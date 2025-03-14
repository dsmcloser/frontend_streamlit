import os

import streamlit.components.v1 as components


def custom_radio_button(label, options, default, key=None):
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "radio_button/build")
    _radio_button = components.declare_component(
        "radio_button", path=build_dir)
    return _radio_button(label=label, options=options, default=default, key=key)


def list_job_display(itens_information, selected_id=None):
    # "PROD"
    # parent_dir = os.path.dirname(os.path.abspath(__file__))
    # build_dir = os.path.join(parent_dir, "list_job_display/build")
    # _list_job_display = components.declare_component(
    #     "list_job_display", path=build_dir)

    # DEV
    _list_job_display = components.declare_component("list_job_display",
                                                     url="http://localhost:3001",)

    return _list_job_display(items_information=itens_information, selected_id=selected_id)


def test():
    _test = components.declare_component("list_job_display",
                                         url="http://localhost:3001",)
    return _test()
