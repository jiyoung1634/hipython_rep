import main_func as ma
import sub_module.alarm as al


def add_qty():
    while True:
        qty = input('\t수량을 입력하세요(취소: x): ')
        if qty.lower() =="x":
            return qty
        try:
            qty = int(qty)
            if qty > 0:
                return qty
            al.prt_alarm()
        except ValueError:
            al.prt_alarm()


def yesno():
    while True:
        a=input('더 주문하시겠습니까?(y/n):')
        if a.lower() not in ['y','n']:
            al.prt_alarm()
            continue
        else:
            return a
