<유입, 유츨 분석>
1. 현재 코드상에는 램프 간섭 영향률과 진출원활률에서 input_ramp와 out_ramp 를 쌍으로 지어서 계산하고 있음
2. 이것으로 인해 input 과 output 램프의 갯수가 안 맞으면 데이터가 삭제됨
3. 유출을 할 경우, input_ramp는 그대로
4. 유입을 할 경우, out_ramp는 그대로 설정해야 정상적으로 출력됨


<수정 부분>
1. before_ramp , after_ramp 네트워크 상황에 맞게 수정
2. 유입램프만 있으면 input_ramp, input_main_ramp만 수정
    input_ramp는 유입 램프의 교통량 측정 목적
    input_main_ramp는 계산 후 rfr 값 적용할 검지기 찾기 위함