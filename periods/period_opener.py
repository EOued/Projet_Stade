from PyQt6.QtWidgets import QComboBox, QSpinBox
from utils.utils import Type
from periods.periods import PeriodsUI


def retrieve_data_teams(dict, uuid):
    if uuid not in dict:
        dict[uuid] = [[], [], [], [], [], [], []]
    return dict[uuid]


def retrieve_data_fields(dict, uuid):
    if uuid not in dict:
        dict[uuid] = [0, 0, 0, 0, 0, 0, 0]
    return dict[uuid]


def reset_data_teams(dict, uuid):
    dict[uuid] = [[], [], [], [], [], [], []]
    return dict[uuid]


def reset_data_fields(dict, uuid):
    dict[uuid] = [0, 0, 0, 0, 0, 0, 0]
    return dict[uuid]


def xor_period(start_hour, end_hour, ftype, day, saved_data):

    if not ftype in [0, 1]:
        saved_data[day] ^= 2**end_hour - 2**start_hour
        return
    saved_data[day][0] ^= 2**end_hour - 2**start_hour
    if ftype == 1:
        saved_data[day][1] |= 2**end_hour - 2**start_hour


def teams_data_parsing(displayed_data, saved_data):
    days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    for day, elements in displayed_data.items():
        for element in elements:
            duration = int(element[1].split("h")[0])
            ftype = ["Naturel", "Synthétique"].index(element[2])
            saved_data[days.index(day)].append([duration, ftype])


def fields_data_parsing(displayed_data, saved_data):
    for day, elements in displayed_data.items():
        for element in elements:
            start = int(element[1].split("h")[0])
            end = int(element[2].split("h")[0])
            xor_period(
                start,
                end,
                -1,
                [
                    "Lundi",
                    "Mardi",
                    "Mercredi",
                    "Jeudi",
                    "Vendredi",
                    "Samedi",
                    "Dimanche",
                ].index(day),
                saved_data,
            )


def teams_data_loading(data):
    ret_data = {}
    days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    for day, elements in enumerate(data):
        for element in elements:
            if element == []:
                continue
            if days[day] not in ret_data:
                ret_data[days[day]] = []
            ret_data[days[day]].append(
                [
                    "",
                    f"{element[0]}h",
                    ["Naturel", "Synthétique"][element[1]],
                ]
            )
    return ret_data


def fields_data_loading(data):
    ret_data = {}
    days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    for day, elements in enumerate(data):
        for element in int_to_time_periods(elements):
            if element == []:
                continue
            if days[day] not in ret_data:
                ret_data[days[day]] = []
            ret_data[days[day]].append(
                [
                    "",
                    f"{element[0]}h",
                    f"{element[1]}h",
                ]
            )
    return ret_data


def int_to_time_periods(x: int, ftype: int = 0) -> list[list[int]]:
    periods = []
    start = None
    _ftype = ftype & 1
    for i in range(24):
        if (x >> i) & 1:
            if start is None:
                start = i
            # ftype shifted at point
            if start is not None and _ftype != (ftype >> i) & 1:
                periods.append([start, i, _ftype])
                start = i
        else:
            if start is not None:
                periods.append([start, i, (ftype >> i - 1) & 1])
                start = None

        _ftype = (ftype >> i) & 1

    if start is not None:
        periods.append([start, 0, (ftype >> 23) & 1])

    return periods


def periods_fields_adder(days, elements):
    checkboxes = [
        day.isChecked()
        for day in days
        if day.objectName() in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    ]

    start = [
        elem.value()
        for elem in elements
        if isinstance(elem, QSpinBox) and elem.objectName() == "start"
    ][0]

    end = [
        elem.value()
        for elem in elements
        if isinstance(elem, QSpinBox) and elem.objectName() == "end"
    ][0]

    _days = [
        "Lundi",
        "Mardi",
        "Mercredi",
        "Jeudi",
        "Vendredi",
        "Samedi",
        "Dimanche",
    ]
    days = []
    for index, day in enumerate(_days):
        if checkboxes[index]:
            days.append(day)

    return days, [f"{start}h", f"{end}h"]


def periods_teams_adder(days, elements):
    checkboxes = [
        day.isChecked()
        for day in days
        if day.objectName() in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    ]

    duration = [
        elem.value()
        for elem in elements
        if isinstance(elem, QSpinBox) and elem.objectName() == "start"
    ][0]

    ftype = [
        elem.currentText()
        for elem in elements
        if isinstance(elem, QComboBox) and elem.objectName() == "type_combo"
    ][0]

    _days = [
        "Lundi",
        "Mardi",
        "Mercredi",
        "Jeudi",
        "Vendredi",
        "Samedi",
        "Dimanche",
    ]
    days = []
    for index, day in enumerate(_days):
        if checkboxes[index]:
            days.append(day)

    return days, [f"{duration}h", ftype]


def fields_check_function(root, items, displayed_data):
    start = int(items[0].split("h")[0])
    end = int(items[1].split("h")[0])
    if end <= start:
        return f"{root}: La période {items[0]}-{items[1]} est invalide."
    for period in displayed_data[root]:
        _start = int(period[1].split("h")[0])
        _end = int(period[2].split("h")[0])
        if _start == start and _end == end:
            return f"{root}: Duplicata de la période {items[0]}-{items[1]}."
        if _start <= start < _end or _start < end <= _end:
            return f"{root}: La période {items[0]}-{items[1]} interfère avec la période {period[1]}-{period[2]}."
    return ""


def teams_check_function(_, _2, _3):
    return ""


def periods_popup(uuid, data, type: Type):
    __data = [retrieve_data_fields, retrieve_data_teams][type.value](data, uuid)
    popup = PeriodsUI(
        [fields_data_loading, teams_data_loading][type.value](__data),
        [periods_fields_adder, periods_teams_adder][type.value],
        [fields_check_function, teams_check_function][type.value],
        [["type_combo"], ["end"]][type.value],
        [["Début", "Fin"], ["Durée", "Type"]][type.value],
    )
    if popup.window is None:
        return
    if popup.window.exec():
        _data = [reset_data_fields, reset_data_teams][type.value](data, uuid)
        [fields_data_parsing, teams_data_parsing][type.value](
            popup.displayed_data, _data
        )
