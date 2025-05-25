# 구글 뉴스 검색 애플리케이션

FastAPI와 React를 사용한 구글 뉴스 검색 웹 애플리케이션입니다.

## 기능

- 구글 뉴스 검색
- 실시간 검색 결과 표시
- 뉴스 제목과 URL 제공
- 반응형 웹 디자인

## 기술 스택

### 백엔드
- FastAPI
- Selenium
- Python 3.8+

### 프론트엔드
- React
- Material-UI
- Axios

## 설치 및 실행

### 백엔드
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### 프론트엔드
```bash
cd frontend
npm install
npm start
```

## 배포

이 프로젝트는 Railway를 통해 배포됩니다.

### 백엔드 배포
- Railway 프로젝트 생성
- GitHub 저장소 연결
- `backend` 디렉토리를 루트 디렉토리로 설정

### 프론트엔드 배포
- Railway 프로젝트 생성
- GitHub 저장소 연결
- `frontend` 디렉토리를 루트 디렉토리로 설정
- 환경 변수 `REACT_APP_API_URL` 설정

## 라이선스

MIT 