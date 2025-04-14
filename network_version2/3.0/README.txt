실행순서
1. 2.0 버전에 있는 파일들 실행 후 시뮬레이션 결과 파일 생성
2. time_average_iteration(시간별) 파일 실행    => 1_time_output.xlsx
3. vehicle_average_iterataion(차종별) 파일 실행    => 1_vehicle_output.xlsx
4. 양식폴더에 해당 결과 파일들 정리 -> 600pcp(1~24), 1350pcp(25~48), 1750pcp(49~72) 한번에 정리
5. Cycle별로 정리된 폴더에서 vehicle_type_test 실행    => 100_output, 300_output, 630_output, 640_output, 650_output.xlsx
6. vehicle_output 파일이 있는 기존 경로에서 vehicle_weights_iteration 파일 실행 => 1_weights_output.xlsx
7. 모아둔 weights_output 파일이 있는 경로에서 weights_output 파일 실행 => weights_output.xlsx

vehicle_type_test, volume_output, weights_output 파일의 경우 Cycle별로 실행 시켜야 하기 때문에 파일을 한 곳에 모아둬야함


