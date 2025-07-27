import pytest
import fun_transactions as ft

def test_filter_transaction_income():
    expected_list =[

        {"id": 1, "type": "income", "amount": 1000, "currency": "USD"},

        {"id": 3, "type": "income", "amount": 500, "currency": "USD"},

        {"id": 5, "type": "income", "amount": 700, "currency": "USD"},

        {"id": 7, "type": "income", "amount": 100, "currency": "EUR"},
    ]

    assert ft.filter_transactions(ft.transactions, "income") == expected_list


def test_map_ransactions_usd():
    result = [1000, 200, 500, 300, 700, 0, 0]
    assert ft.map_transactions(ft.transactions, "USD") == result

def test_reduce_transactions():
    assert ft.reduce_transactions([1000, 500, 700, 0]) == 2200

def test_process_transactions_expense_eur():
    assert ft.proces_transactions(ft.transactions, "expense", "EUR")
