from servicemon import query


def test_truth():
    result_list = query.get_data()
    assert len(result_list) == 1
    assert len(result_list[0]) == 27
