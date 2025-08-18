import mariadb
import sys

# 1. 강사님 DB (원본 DB) 연결 설정
try:
    conn_src = mariadb.connect(
        user="lguplus7",
        password="lg7p@ssw0rd~!",
        host="192.168.14.38",
        port=3310,
        database="cp_data"
    )
except mariadb.Error as e:
    print(f"강사님 DB 연결 오류: {e}")
    sys.exit(1)

src_cur = conn_src.cursor()

# 2. 여러분의 DB (타겟 DB) 연결 설정
try:
    conn_tar = mariadb.connect(
        user="lguplus7",
        password="lg7p@ssw0rd~!",
        host="localhost",
        port=3310,
        database="cp_data"
    )
except mariadb.Error as e:
    print(f"여러분의 DB 연결 오류: {e}")
    conn_src.close()
    sys.exit(1)

tar_cur = conn_tar.cursor()

try:
    # 3. 여러분의 DB에서 기존 데이터 삭제
    print("여러분의 DB에서 기존 'tb_weather_tcn' 테이블 데이터 삭제 중...")
    tar_cur.execute("TRUNCATE TABLE tb_weather_tcn")
    conn_tar.commit()
    print("기존 데이터 삭제 완료.")

    # 4. 강사님 DB에서 데이터 가져올 컬럼 이름 확인
    print("강사님 DB의 컬럼 정보를 가져오는 중...")
    src_cur.execute("DESCRIBE tb_weather_tcn")
    src_columns = [col[0] for col in src_cur.fetchall()]
    print(f"강사님 DB의 컬럼: {src_columns}")
    
    # 5. 강사님 DB에서 모든 컬럼의 데이터 가져오기
    print("강사님 DB에서 모든 데이터를 가져오는 중...")
    select_query = f"SELECT {', '.join(src_columns)} FROM tb_weather_tcn"
    src_cur.execute(select_query)
    data_list = src_cur.fetchall()
    print(f"총 {len(data_list)}개의 데이터 가져옴.")

    # 6. 여러분의 DB에 데이터 적재
    print("여러분의 DB에 데이터 새로 적재 중...")
    
    # INSERT 쿼리를 동적으로 생성
    insert_query = f"INSERT INTO tb_weather_tcn ({', '.join(src_columns)}) VALUES ({', '.join(['%s'] * len(src_columns))})"
    
    for data in data_list:
        tar_cur.execute(insert_query, data)
    
    conn_tar.commit()
    print("데이터 적재 완료.")

except Exception as e:
    conn_tar.rollback()
    print(f"데이터 처리 중 오류 발생: {e}")
    
finally:
    conn_src.close()
    conn_tar.close()
    print("모든 데이터베이스 연결 종료.")