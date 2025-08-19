from django.db import models


class TypeChoices(models.TextChoices):
    INPUT = "input", "Input"
    OUTPUT = "output", "Output"


class ConceptChoices(models.TextChoices):
    INITIAL_CAPITAL = "input", "Input"
    LOAN = "loan", "Loan granted"
    CAPITAL_PAYMENT = "capital_payment", "Capital payment"
    INTEREST_PAYMENT = "interest_payment", "Interest payment"
    EXPENSE = "expense", "Expense"
    OTHER = "other", "Other"
