from aiogram.fsm.state import StatesGroup, State


class ExpenseStates(StatesGroup):
    choosing_category = State()
    entering_amount = State()
