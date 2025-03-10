"""시뮬레이션 결과파일에서 데이터 가져오기"""
import sqlite3
import pandas as pd
import win32com.client  # Windows COM 인터페이스 사용
import os
import xml.etree.ElementTree as ET

# 폴더 경로 설정
folder_path = r"C:\VISSIM_Workspace\test3"  # 폴더 경로 입력 받아야함 추후에 함수에 파라미터로 처리 예정

def vissim_simulation(path, link1, link2):
    link_no = "4" # 파라미터 처리
    link_no2 = "6"

    # 폴더 내 파일 목록 가져오기
    file_list = os.listdir(folder_path)
    inpx_files = [file for file in file_list if file.endswith(".inpx")]

    # VISSIM 실행 및 연결
    Vissim = win32com.client.Dispatch("Vissim.Vissim")  # Vissim 인스턴스 생성

    for i in range(len(inpx_files)):
        file_name = inpx_files[i]
        file_path = folder_path + "\\" +file_name
        print("file_path : ", file_path)

        for r in range(5,31,5): # 중차량 비율 5~30%
            a = int(r/5-1)

            # 소형차, 버스, 소형화물, 중형화물, 대형화물 비율 설정
            vehicle1 = [86.24, 81.70, 77.16, 72.62, 68.09, 63.55]
            vehicle2 = [8.76, 8.30, 7.84, 7.38, 6.91, 6.45]
            vehicle3 = [3.56, 7.13, 10.69, 14.26, 17.82, 21.38]
            vehicle4 = [1.27, 2.53, 3.80, 5.07, 6.34, 7.60]
            vehicle5 = [0.17, 0.34, 0.51, 0.68, 0.84, 1.01]
            veh = [vehicle1[a], vehicle2[a], vehicle3[a], vehicle4[a], vehicle5[a]]

            for g in range(2,10): # 종단경사 2~9%
                # 종단경사 설정
                new_gradient = g * -0.01
                new_gradient2 = g * 0.01


                # XML 파일 파싱
                tree = ET.parse(file_path)
                root = tree.getroot()

                # <link> 태그 찾기
                for link in root.findall(".//link"):
                    if link.get("no") == str(link_no):  # 특정 no 값을 가진 <link> 찾기
                        link.set("gradient", str(new_gradient))  # gradient 속성 변경
                    if link.get("no") == str(link_no2):  # 특정 no 값을 가진 <link> 찾기
                        link.set("gradient", str(new_gradient2))  # gradient 속성 변경

                    # <vehicleCompositions> 태그 내 <vehicleComposition name="Default"> 찾기
                for vehicle_comp in root.findall(".//vehicleComposition"):
                    if vehicle_comp.get("name") == "test":

                        # <vehCompRelFlows> 태그 찾기
                        vehCompRelFlows = vehicle_comp.find("vehCompRelFlows")
                        if vehCompRelFlows is not None:
                            # <vehicleCompositionRelativeFlow> 태그 찾기
                            for relflow in vehCompRelFlows.findall("vehicleCompositionRelativeFlow"):
                                vehType = relflow.get("vehType")
                                if(vehType == "100"): # 승용차
                                    relflow.set("relFlow", str(round(veh[0],4)))
                                if(vehType == "200"): # 버스
                                    relflow.set("relFlow", str(round(veh[1],4)))
                                if(vehType == "300"): # 소형화물
                                    relflow.set("relFlow", str(round(veh[2],4)))
                                if(vehType == "400"): # 중형화물
                                    relflow.set("relFlow", str(round(veh[3],4)))
                                if(vehType == "500"): # 대형화물
                                    relflow.set("relFlow", str(round(veh[4],4)))

                # 변경된 XML을 원본 파일에 덮어쓰기
                tree.write(file_path, encoding="utf-8", xml_declaration=True)

                print("new_gradient : ", new_gradient, "new_gradient2 : ", new_gradient2)
                print("100rel: ", round(veh[0],4), "200rel : ", round(veh[1],4), "300rel : ", round(veh[2],4), "400rel : ", round(veh[3],4), "500rel : ", round(veh[4],4))

                # VISSIM 네트워크 파일 (.inpx) 로드
                # C:\VISSIM_Workspace\test\test.inpx"
                Vissim.LoadNet(file_path)

                print("VISSIM 시뮬레이션 실행 중...")
                Vissim.Simulation.RunContinuous()

                Vissim.Simulation.Stop()
                print("VISSIM 시뮬레이션 종료")

                interval_value = 0

                # dataColl 태그에서 interval 속성 값 찾기
                for elem in root.iter("dataColl"):
                    interval_value = int(elem.get("interval"))  # "interval" 속성 값 가져오기
                    if interval_value:
                        print(f"추출된 interval 값: {interval_value}") # 60
                    else:
                        print("추출된 interval 값이 없습니다.")

                # 데이터베이스 파일 경로
                # "C:/VISSIM_Workspace/test/test.results/3.db"
                # 확장자 제거
                results_path = folder_path + "\\" +os.path.splitext(file_name)[0] + ".results"
                results_file = [f for f in os.listdir(results_path) if f.endswith(".db")][-1]

                db_path = os.path.join(folder_path, os.path.splitext(file_name)[0] + ".results",  results_file)
                # 파일명 추출
                simrun = db_path.split("\\")[-1].split(".")[0]


                # 데이터베이스 연결
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()

                # 특정 테이블의 데이터 조회
                table_name = "DATACOLLECTIONMEASUREMENT_EvaluationTimeIntervalClass"
                query = f"SELECT * FROM {table_name};"  # 전체 데이터 조회

                # 데이터 읽기
                df = pd.read_sql_query(query, conn)

                # TIMEINT 변환
                df["ARG_TIMEINTERVAL"] = df["ARG_TIMEINTERVAL"].astype(int) * interval_value - interval_value  # 변환 시작점 보정
                df["ARG_TIMEINTERVAL"] = df["ARG_TIMEINTERVAL"].apply(lambda x: f"{x}-{x+interval_value}")

                # OCCUPRATE 보정
                df["OCCUPRATE"] = df["OCCUPRATE"].astype(float)*100
                df["OCCUPRATE"] = df["OCCUPRATE"].apply(lambda x: f"{x:.2f}")  # 항상 소수점 둘째 자리까지 유지
                df = df.round(2)
                df["OCCUPRATE"] = df["OCCUPRATE"].astype(str) + "%"

                # SIMRUN 설정
                df["SIMRUN"] =simrun

                # 컬럼명 변경
                df.rename(columns={
                    "ARG_TIMEINTERVAL": "TIMEINT",
                    "OBJECT_ID": "DATACOLLECTIONMEASUREMENT",
                    "ACCELERATION" : "ACCELERATION(ALL)",
                    "DIST" : "DIST(ALL)",
                    "LENGTH" : "LENGTH(ALL)",
                    "VEHS" : "VEHS(ALL)",
                    "PERS" : "PERS(ALL)",
                    "QUEUEDELAY" : "QUEUEDELAY(ALL)",
                    "SPEEDAVGARITH" : "SPEEDAVGARITH(ALL)",
                    "SPEEDAVGHARM" : "SPEEDAVGHARM(ALL)",
                    "OCCUPRATE" : "OCCUPRATE(ALL)"
                }, inplace=True)

                # 순서 재정의
                df = df[["SIMRUN", "TIMEINT", "DATACOLLECTIONMEASUREMENT", "ACCELERATION(ALL)", "DIST(ALL)",
                         "LENGTH(ALL)", "VEHS(ALL)", "PERS(ALL)", "QUEUEDELAY(ALL)", "SPEEDAVGARITH(ALL)", "SPEEDAVGHARM(ALL)", "OCCUPRATE(ALL)"]]

                excel_dr  = os.path.join(folder_path + "\\" + os.path.splitext(file_name)[0] + "_output")
                results_file = os.path.splitext(results_file)[0]
                excel_path = excel_dr +"\\" + results_file + "_output" +".xlsx"
                if not os.path.exists(excel_dr):
                    os.makedirs(excel_dr)
                df.to_excel(excel_path, index=False)

                # 연결 종료
                conn.close()
