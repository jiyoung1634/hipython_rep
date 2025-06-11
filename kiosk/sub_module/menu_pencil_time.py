import time
import main_func as ma
import sub_module.alarm as al


def prt_menu(menu):
    print('╔' + '═' * 40 + '╗')
    print(f'빵꾸똥꾸 문구야'.center(34))
    print(f"에 오신 것을 환영합니다!💥".center(34))
    print('╚' + '═' * 40 + '╝') 
    print(f'{"번호"}\t\t{"제품명"}\t\t{"가격"}')
    print('-'*44)

    for i, m in enumerate(menu):
        print(f'{i+1}\t\t{m["name"]}\t\t{m["price"]:,}원')
    print('-'*44)



def draw_pencil_ascii():
    pencil_art = r"""
        .================ooooooo
 ___   ,'    \_________________________________
/   /-/       /                   ////////////  ''--..._
\___\-\       \                   \\\\\\\\\\\\  __..--'
       `--------------------------''''''''''''''
"""
    print(pencil_art)


def prt_time():
    for i in range(3, 0, -1):
        print('=' * 44)
        print(f'{i}초 뒤에 시작화면으로 돌아갑니다.'.center(34))
        time.sleep(1)



def add_lst(order_list, ord_num, qty):
    item = ma.menu[ord_num]
    for i in order_list:
        if i['name'] == item['name']:
            i['qty'] += qty
            return order_list 
    order_list.append({
        'name': item['name'],
        'qty': qty,
        'price': item['price']
    })
    return order_list
  



def add_ord():
    while True:        
        try:
            ord_num = int(input('주문하실 제품 번호를 선택하세요: ')) -1
            if not (0 <= ord_num < len(ma.menu)):
                al.prt_alarm()
                continue
            return ord_num
        except ValueError:
            al.prt_alarm()
            continue


