import os
import csv
import mariadb
import sys

# 1. 파일 경로 설정
# 압축이 해제된 CSV 파일들이 있는 폴더 경로를 지정합니다.
extract_dir = 'C:/data/소상공인시장진흥공단_상가(상권)정보_20250630'  # '소상공인시장진흥공단_상가(상권)정보.zip' 파일을 압축 푼 폴더명

# 2. MariaDB 연결 설정
try:
    conn = mariadb.connect(
        user="lguplus7",
        password="lg7p@ssw0rd~!",
        host="localhost",
        port=3310,
        database="cp_data"
    )
except mariadb.Error as e:
    print(f"MariaDB 연결 오류: {e}")
    sys.exit(1)

cur = conn.cursor()

# 3. CSV 파일을 읽고 DB에 적재
try:
    print("CSV 파일 데이터를 DB에 적재 중...")
    
    # 39개의 컬럼을 정의
    columns = [f"col{i}" for i in range(1, 40)]
    insert_sql = f"INSERT INTO tb_smb_ods ({', '.join(columns)}) VALUES ({', '.join(['?'] * 39)})"
    
    # 압축 해제된 디렉토리의 파일 목록을 가져옵니다.
    for filename in os.listdir(extract_dir):
        if filename.endswith('.csv'):
            file_path = os.path.join(extract_dir, filename)
            print(f"\n파일 처리 중: {filename}")
            
            with open(file_path, 'r', encoding='utf-8') as csvfile:
                # 첫 번째 줄(헤더)을 건너뜁니다.
                reader = csv.reader(csvfile)
                next(reader, None)
                
                # CSV 데이터 읽기 및 DB 삽입
                row_count = 0
                for row in reader:
                    # 행의 컬럼 개수가 39개인지 확인합니다.
                    if len(row) == 39:
                        try:
                            cur.execute(insert_sql, tuple(row))
                            row_count += 1
                        except mariadb.Error as e:
                            print(f"DB 삽입 오류 (파일: {filename}, 행: {row_count+1}): {e}")
                            conn.rollback()
                            sys.exit(1)
                conn.commit()
                print(f"  -> {row_count}개의 행 적재 완료.")
    
    print("\n모든 CSV 파일 적재 완료.")

except FileNotFoundError:
    print(f"오류: '{extract_dir}' 디렉토리를 찾을 수 없습니다. 경로를 확인해주세요.")
    sys.exit(1)
except Exception as e:
    conn.rollback()
    print(f"데이터 처리 중 오류 발생: {e}")

finally:
    conn.close()
    print("데이터베이스 연결 종료.")