import sub_module.alarm as al
import sub_module.cost_point as copo
import sub_module.inputt as i
import sub_module.menu_pencil_time as mepeti



menu = [
    {'name':'샤프', 'price': 6000},
    {'name':'볼펜', 'price': 3000},
    {'name':'지우개', 'price': 1000},
    {'name':'화이트', 'price': 3000},
    {'name':'공책', 'price': 3500}
]

points = {}

mepeti.draw_pencil_ascii()


while True:
    mepeti.prt_menu(menu)
    # 다중 주문 저장 리스트
    order_list = []

    while True: 
        
        ord_num = mepeti.add_ord()         
        menut = menu[ord_num]['name']
        
        print('='*44)
        print(f'{"고객님이 선택하신 제품은":^33}')
        print(f'{menut + " 입니다.":^33}')
        print(f'{"몇 개를 드릴까요?":^33}')
        
        
        qty = i.add_qty()
        if qty in ('x','X'):
            break
             
        mepeti.add_lst(order_list, ord_num, qty)
        
        answer = i.yesno()
        if answer == 'n':
            break
        print('-'*44)

    if qty not in ('x','X'):
        
        total = copo.calc_cost(order_list)
        
        copo.prt_points(total, points)
        
        print(f'{"결제가 완료되었습니다.":^37}')
        print(f'{"잠시만 기다려주세요. 😊":^37}')

        mepeti.prt_time()

