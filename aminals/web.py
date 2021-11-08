from google_images_download import google_images_download

response = google_images_download.googleimagesdownload()
arguments = {"keywords": "곰",      # 검색 키워드
             "limit" : 40,          # 크롤링 이미지 갯수 (최대 100개)
             "print_urls" : True,   # 이미지 url출력
             "format":"jpg"}        # 크롤링할 파일 형식

paths = response.download(arguments)
print(paths)