import requests  # requests 모듈 임포트

def download_file(file_url, save_path):
    with open(save_path, 'wb') as f: # 저장할 파일을 바이너리 쓰기 모드로 열기
        response = requests.get(file_url) # 파일 URL에 GET 요청 보내기
        f.write(response.content) # 응답의 내용을 파일에 쓰기

# URL과 저장 경로 변수를 지정합니다.
url = 'https://apihub.kma.go.kr/api/typ01/cgi-bin/url/nph-aws2_min?stn=0&disp=0&help=1&authKey=QVfjYfNJRHaX42HzSVR2NQ'
save_file_path = 'output_file.zip'

# 파일 다운로드 함수를 호출합니다.
download_file(url, save_file_path)





import mariadb
import sys
import time

# MariaDB 연결 설정 (이전 예제 코드를 사용)
try:
    conn = mariadb.connect(
        user="lguplus7",
        password="lg7p@ssw0rd~!",
        host="localhost",
        port=3310,
        database="cp_data"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)
cur = conn.cursor()

# 파일 다운로드 후 처리
try:
    # 다운로드한 파일을 텍스트 모드로 엽니다.
    with open(save_file_path, 'r', encoding='euc-kr') as f:
        # 파일 내용을 한 줄씩 읽습니다.
        for line in f:
            # 주석, 헤더, 빈 줄은 건너뜁니다.
            if line.startswith('#') or line.strip() == '' or line.startswith('YYMMDDHHMI'):
                continue

            # 원본 데이터를 org_data 컬럼에 저장하기 위해 변수에 담습니다.
            org_data = line.strip()
            
            # 공백을 기준으로 데이터를 분리합니다.
            parts = line.split()

            # yyyymmddhhmi와 stn 값을 추출합니다.
            yyyymmddhhmi = parts[0]
            stn = parts[1]

            # 중복 데이터가 있는지 확인합니다.
            cur.execute(
                "SELECT COUNT(*) FROM tb_weather_aws1 WHERE yyyymmddhhmi = ? AND stn = ?",
                (yyyymmddhhmi, stn)
            )
            count = cur.fetchone()[0]

            # 중복이 아니면 데이터를 삽입합니다.
            if count == 0:
                # 파일 구조에 맞게 모든 컬럼 값을 추출합니다.
                wd1 = parts[2]
                ws1 = parts[3]
                wds = parts[4]
                wss = parts[5]
                wd10 = parts[6]
                ws10 = parts[7]
                ta = parts[8]
                re = parts[9]
                rn_15m = parts[10]
                rn_60m = parts[11]
                rn_12h = parts[12]
                rn_day = parts[13]
                hm = parts[14]
                pa = parts[15]
                ps = parts[16]
                td = parts[17]

                # INSERT 쿼리문을 모든 컬럼에 맞게 수정합니다.
                insert_sql = """
                INSERT INTO tb_weather_aws1 (
                    yyyymmddhhmi, stn, wd1, ws1, wds, wss, wd10, ws10, ta, re, rn_15m, rn_60m, rn_12h, rn_day, hm, pa, ps, td, org_data
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                cur.execute(
                    insert_sql,
                    (yyyymmddhhmi, stn, wd1, ws1, wds, wss, wd10, ws10, ta, re, rn_15m, rn_60m, rn_12h, rn_day, hm, pa, ps, td, org_data)
                )
                print(f"새로운 데이터 삽입: yyyymmddhhmi={yyyymmddhhmi}, stn={stn}")
            else:
                print(f"중복 데이터 건너뛰기: yyyymmddhhmi={yyyymmddhhmi}, stn={stn}")

    # 모든 삽입 작업이 끝나면 변경사항을 커밋합니다.
    conn.commit()
    print("데이터베이스 커밋 완료.")

except FileNotFoundError:
    print(f"Error: 파일 '{save_file_path}'을(를) 찾을 수 없습니다.")
except Exception as e:
    # 예외 발생 시 롤백하고 오류 메시지를 출력합니다.
    conn.rollback()
    print(f"데이터 처리 중 오류 발생: {e}")

finally:
    # 최종적으로 데이터베이스 연결을 닫습니다.
    conn.close()
    print("데이터베이스 연결 종료.")
    