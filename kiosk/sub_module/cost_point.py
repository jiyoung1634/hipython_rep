import main_func as ma
import sub_module.menu_pencil_time as mepeti
import sub_module.alarm as al



def calc_cost(order_list):
    total = 0   
    print('='*44)
    print(f'\t\t{"주문 내역"}')
    print('-'*44)

    for order in order_list:
        item_total = order['qty'] * order['price']
        total += item_total

        print(f'{order["name"]}\t{order["qty"]}개\t-\t{item_total:,}원')

    print('-'*44)
    print(f'총 결제 금액: {total:,}원')
    print('='*44)
    return total



def prt_points(total, points):
    while True:
        ab = input('포인트를 적립하시겠습니까? (y/n): ')
        if ab.lower() not in ['y', 'n']:
            al.prt_alarm()
            continue
        elif ab.lower()=='n':
            return        
        else:
            while True:
                phone = input('전화번호를 입력해 주세요: ')
                if not phone.isdigit() or len(phone) < 11 or phone == "x":
                    al.prt_alarm()
                    continue                       
                user_id = f'user_{phone[-4:]}'
                point = int(total * 0.05)                 
                if user_id in points :
                    points[user_id] += point
                else :
                    points[user_id] = point
                print('='*44)
                print(f'🎁{user_id}고객님, {point}점 적립 되었습니다!🎁')
                print(f' 고객님의 총 적립포인트는 {points[user_id]:,}점 입니다!')
                print('='*44)
                return
  