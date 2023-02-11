#!/usr/bin/env python

import argparse
import sys
import math

ERROR_MESSAGE = "Incorrect parameters"
MIN_PARAMETERS = 5


def validate_args(arguments):
    if arguments.type is None:
        return ERROR_MESSAGE
    elif arguments.type == "diff" and arguments.payment:
        return ERROR_MESSAGE
    elif not arguments.interest:
        return ERROR_MESSAGE
    elif len(sys.argv) < MIN_PARAMETERS:
        return ERROR_MESSAGE
    elif (arguments.payment or arguments.principal or arguments.periods or arguments.interest) < 0:
        return ERROR_MESSAGE
    else:
        return arguments


def calculate_i(interest_input_arg) -> float:
    """
    i = nominal (monthly) interest rate.
    Usually, it is 1/12 of the annual interest rate and is a floating value, not a percentage.
    For example, if your annual interest rate = 12%, then i = 0.01;
    The user inputs the interest rate as a percentage, for example, 11.7
    You should divide this value by 12 and 100 to use it as i in the formula.
    :return: float
    """
    nominal_rate = (1 / 12) * (interest_input_arg / 100)
    return nominal_rate


def calculate_n(principal_input_arg, annuity_input_arg, value_i_arg):
    """
    n = number of payments. This is usually the number of months in which repayments will be made.
    :return:
    """
    number_payments = math.log((annuity_input_arg / (annuity_input_arg - value_i_arg * principal_input_arg)),
                               (1 + value_i_arg))
    return number_payments


def calculate_a(principal_input_arg, value_i_arg, periods_input_arg) -> float:
    """
    A = annuity payment
    :return: float
    """
    ordinary_annuity = principal_input_arg * (
            (value_i_arg * (1 + value_i_arg) ** periods_input_arg)
            / (((1 + value_i_arg) ** periods_input_arg) - 1)
    )
    return ordinary_annuity


def calculate_p(annuity_input, value_i, periods_input) -> float:
    """
    P = loan principal
    :return: float
    """
    loan_principal = annuity_input / (
            (value_i * (1 + value_i) ** periods_input)
            / (((1 + value_i) ** periods_input) - 1)
    )
    return loan_principal


def months_conversion(value) -> None:
    """
    Convert number of months to year & month combination for a human-readable format
    :return: string
    """
    if ((value / 12) - (math.ceil(value / 12))) == 0:
        output = int(value) // 12
        print(f"It will take {output} years to repay this loan!")
    elif (value / 12) - (math.floor(value / 12)) > 0:
        val01 = value // 12
        val02 = value % 12
        print(f"It will take {val01} years and {val02} months to repay this loan!")
    else:
        print("Please check the value_n")


def main():
    parser = argparse.ArgumentParser(description="Loan Calculator for differentiated payments")
    parser.add_argument("--type", choices=["diff", "annuity"],
                        help="Please select either diff or annuity",
                        type=str, required=True)
    parser.add_argument("--payment", type=int)
    parser.add_argument("--principal", type=int)
    parser.add_argument("--periods", type=int)
    parser.add_argument("--interest", type=float)

    args = parser.parse_args()

    args = validate_args(args)

    args_dict = {}
    if args == ERROR_MESSAGE:
        print(args)
        sys.exit()
    else:
        args_dict = vars(args)

    # Calculate differentiated payments
    if args_dict['type'] == "diff":
        value_i = calculate_i(args_dict['interest'])
        value_p = args_dict['principal']
        value_n = args_dict['periods']

        list_ = []
        for i in range(1, value_n + 1):
            value_d = math.ceil((value_p / value_n) + value_i * (value_p - ((value_p * (i - 1)) / value_n)))
            list_.append(value_d)
            print(f"Month {i}: payment is {value_d}")
        overpayment = int(math.fabs(sum(list_) - value_p))
        print(f"\nOverpayment = {overpayment}")

    elif args_dict['type'] == "annuity":
        if args_dict.get('payment') is None:
            value_p = args_dict['principal']
            value_n = args_dict['periods']
            value_i = calculate_i(args_dict['interest'])
            value_a = math.ceil(calculate_a(value_p, value_i, value_n))
            print(f"Your annuity payment = {value_a}!")
            overpayment = int(math.fabs((value_a * value_n) - value_p))
            print(f"Overpayment = {overpayment}")
        elif args_dict.get('principal') is None:
            value_a = args_dict['payment']
            value_n = args_dict['periods']
            value_i = calculate_i(args_dict['interest'])
            value_p = math.floor(calculate_p(value_a, value_i, value_n))
            print(f"Your loan principal = {value_p}!")
            overpayment = int(math.fabs((value_a * value_n) - value_p))
            print(f"Overpayment = {overpayment}")
        elif args_dict.get('periods') is None:
            value_p = args_dict['principal']
            value_a = args_dict['payment']
            value_i = calculate_i(args_dict['interest'])
            value_n = math.ceil(calculate_n(value_p, value_a, value_i))
            months_conversion(value_n)
            overpayment = int(math.fabs((value_a * value_n) - value_p))
            print(f"Overpayment = {overpayment}")
    else:
        print(ERROR_MESSAGE)


if __name__ == "__main__":
    main()
