import requests
import mariadb
import sys
import time

try:
    conn_tar = mariadb.connect(
        user="lguplus7",
        password="lg7p@ssw0rd~!",
        host="localhost",
        port=3310,
        database="cp_data"
    )
except mariadb.Error as e:
    print(f"MariaDB 연결 오류: {e}")
    sys.exit(1)

tar_cur = conn_tar.cursor()

# 지점 정보 API URL과 인증키(authKey)를 설정합니다.
# YOUR_AUTHKEY_HERE를 본인의 유효한 키로 교체해야 합니다.
req_url = 'https://apihub.kma.go.kr/api/typ01/url/stn_inf.php?inf=AWS&stn=&tm=202211300900&help=1&authKey=QVfjYfNJRHaX42HzSVR2NQ'

# 지점정보는 1회만 수집하므로, while True 루프를 사용하지 않습니다.
try:
    response = requests.get(req_url)
    
    # 응답이 정상적으로 오지 않았을 경우 오류 메시지를 확인합니다.
    if response.status_code != 200:
        print(f"API 요청 오류: 상태 코드 {response.status_code}")
        print(f"오류 메시지: {response.text}")
        sys.exit(1)

    org_data = response.text

    # 공백을 하나로 통일하고 줄바꿈으로 나눕니다.
    # 강사님 코드의 공백 처리 로직을 그대로 사용합니다.
    split_data = org_data.strip().replace('  ', ' ').replace(' ', ' ').split('\n')

    print("지점 정보 데이터베이스에 적재 시작...")
    
    for line in split_data:
        # 주석, 헤더, 빈 줄은 건너뜁니다.
        if line.startswith('#') or line.strip() == '' or line.startswith('STN'):
            continue

        try:
            line_arr = line.strip().split()
            
            # 데이터 추출
            stn_id = line_arr[0]
            lon = line_arr[1]
            lat = line_arr[2]
            stn_sp = line_arr[3]
            ht = line_arr[4]
            ht_wd = line_arr[5]
            stn_ad = line_arr[7]
            stn_ko = line_arr[8]
            stn_en = line_arr[9]
            fct_id = line_arr[10]
            law_id = line_arr[11]
            basin = line_arr[12]

            # 중복 데이터가 있는지 확인합니다.
            # tb_weather_tcn 테이블과 STN_ID 컬럼으로 수정했습니다.
            tar_cur.execute("SELECT seq_no FROM tb_weather_tcn WHERE STN_ID = ?", (stn_id,))
            exist_list = tar_cur.fetchall()
            
            if exist_list:
                print(f"[debug] 중복 데이터: STN_ID={stn_id}")
            else:
                # 데이터를 tb_weather_tcn 테이블에 삽입합니다.
                # 컬럼 이름이 tb_weather_tcn에 맞게 수정되었습니다.
                tar_cur.execute(
                    """
                    INSERT INTO tb_weather_tcn(
                        STN_ID, LON, LAT, STN_SP, HT, HT_WD, STN_AD, STN_KO, STN_EN, FCT_ID, LAW_ID, BASIN, org_addr, create_dt
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, now())
                    """,
                    (stn_id, lon, lat, stn_sp, ht, ht_wd, stn_ad, stn_ko, stn_en, fct_id, law_id, basin, org_data)
                )
                conn_tar.commit()
                print(f"새로운 지점 정보 삽입: STN_ID={stn_id}, STN_KO={stn_ko}")

        except IndexError as e:
            print(f"데이터 파싱 오류: {line.strip()} - {e}")
            continue

    print("데이터 적재 완료.")
    
except Exception as e:
    conn_tar.rollback()
    print(f"데이터 처리 중 오류 발생: {e}")
    
finally:
    conn_tar.close()
    print("데이터베이스 연결 종료.")