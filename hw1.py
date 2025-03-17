import cv2 as cv

def main():
    # 1. 카메라 및 기본 설정
    # (1) 0번 장치를 열어서 사용
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("카메라를 열 수 없습니다.")  
        return  

    # (2) 동영상 저장을 위한 FourCC(코덱), FPS, 해상도 등 설정
    fourcc = cv.VideoWriter_fourcc(*'XVID')
    fps = 20.0
    width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    
   
    # 2. 초기 모드 및 변수 설정
    #   record_mode: 현재 Record(녹화) 중인지 아닌지 나타내는 플래그
    #   - False -> Preview 모드(녹화 안 함)
    #   - True  -> Record 모드(녹화 중)
    record_mode = False
    
    # out: VideoWriter 객체, Record 모드일 때만 생성하여 파일에 기록
    out = None

    # flip_enabled: 좌우 반전(Flip) 기능을 켜고 끄는 플래그
    flip_enabled = False
    
    # 실행 시 안내 메시지 출력
    print("=== My Awesome Video Recorder ===")
    print("[Space] : Preview/Record 모드 전환")
    print("[F]     : Flip(좌우 반전) 토글")
    print("[ESC]   : 프로그램 종료")
    
    while True:
        # 3. 카메라 프레임 읽기
        ret, frame = cap.read()
        if not ret:
            print("프레임을 가져올 수 없습니다.")
            break  # 프레임을 더 이상 못 읽으면 반복 종료
        
        # 4. 추가 기능: Flip(좌우 반전)
        # flip_enabled == True일 때만 cv.flip(frame, 1) 적용
        # (1)는 좌우 반전, (0)은 상하 반전
        if flip_enabled:
            frame = cv.flip(frame, 1)
        
        # 5. Record 모드 처리
        # record_mode가 True이고 out이 정상적으로 열려 있다면, 해당 프레임을 녹화
        if record_mode and out is not None:
            out.write(frame)
            # 화면에 빨간 원 그려서 "녹화 중"임을 표시
            # 원을 그릴 좌표: (width-30, 30), 반지름: 15
            # 색상: (0, 0, 255) (BGR, 빨간색)
            # 두께: -1(채워진 원)
            cv.circle(frame, (width - 30, 30), 15, (0, 0, 255), -1)
        
        # 6. 화면에 현재 프레임 표시
        cv.imshow('My Awesome Video Recorder', frame)
        
        # 7. 키 입력 처리
        # ESC, Space, F 키 등을 처리하기 위해 waitKey 사용
        key = cv.waitKey(30) & 0xFF
        if key == 27:  # ESC 키
            print("프로그램을 종료합니다.")
            break
        elif key == 32:  # Space 키 
            # Preview <-> Record 모드 전환
            record_mode = not record_mode
            if record_mode:
                print("Record 모드로 전환 (녹화 시작)")
                # 모드가 Record로 바뀌면 VideoWriter 객체 생성
                out = cv.VideoWriter('output.avi', fourcc, fps, (width, height))
            else:
                print("Preview 모드로 전환 (녹화 중지)")
                # 모드가 Preview가 되면 더 이상 녹화하지 않으므로 out 해제
                if out is not None:
                    out.release()
                    out = None
        elif key == ord('f') or key == ord('F'):
            # 좌우 반전(Flip) 기능을 토글
            flip_enabled = not flip_enabled
            print(f"Flip 모드 {'활성화' if flip_enabled else '비활성화'}")
    
    # 8. 종료 시 자원 정리
    cap.release()      # 카메라 장치 해제
    if out is not None:
        out.release()  # 동영상 파일 리소스 해제
    cv.destroyAllWindows()  # 모든 OpenCV 윈도우 닫기

if __name__ == "__main__":
    main()